"""Build and exercise the installed distribution outside the checkout."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import venv

ROOT = Path(__file__).resolve().parent

def run(args, cwd, expected=0):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if result.returncode != expected:
        raise RuntimeError(f'{args[0]} exited {result.returncode}, expected {expected}\n{result.stdout}\n{result.stderr}')

with tempfile.TemporaryDirectory() as temporary:
    work = Path(temporary)
    wheel_dir = work / 'wheels'
    run([sys.executable, '-m', 'pip', 'wheel', '--no-build-isolation', '--no-deps', '--wheel-dir', str(wheel_dir), str(ROOT)], work)
    wheels = list(wheel_dir.glob('*.whl'))
    assert len(wheels) == 1
    environment = work / 'env'
    venv.EnvBuilder(with_pip=True).create(environment)
    python = environment / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    run([str(python), '-m', 'pip', 'install', str(wheels[0])], work)
    run([str(python), '-m', 'pip', 'check'], work)
    for name, status in [('after.json', 0), ('before.json', 1), ('guard-normalized.json', 1)]:
        run([str(python), '-m', 'opsec_reports', 'validate', str(ROOT / 'examples' / name)], work, status)
    run([str(python), '-m', 'opsec_reports', 'html', str(ROOT / 'examples' / 'before.json'), '--output', str(work / 'report.html')], work, 1)
    assert (work / 'report.html').is_file()
print('Clean wheel installation and CLI checks passed.')
