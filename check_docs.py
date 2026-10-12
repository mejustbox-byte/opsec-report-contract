"""Paired docs, links and actual synthetic command outcomes."""
import json,re,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).parent
ru={p.name for p in (ROOT/'docs/ru').glob('*.md')};en={p.name for p in (ROOT/'docs/en').glob('*.md')}
assert ru==en
for p in [*ROOT.glob('README*.md'),*ROOT.glob('docs/*/*.md')]:
 text=p.read_text(encoding='utf-8');assert text.count('```')%2==0
 for link in re.findall(r'\]\(([^)]+)\)',text):
  if not link.startswith(('http://','https://','#')):assert (p.parent/link).is_file(),(p,link)
for name in ru:
 blocks=lambda lang:re.findall(r'```\w*\n(.*?)```',(ROOT/'docs'/lang/name).read_text(encoding='utf-8'),re.S)
 assert blocks('ru')==blocks('en'),name
with tempfile.TemporaryDirectory() as tmp:
 def run(args,code):
  r=subprocess.run([sys.executable,'-m','opsec_reports',*args],cwd=ROOT,capture_output=True,text=True,timeout=20)
  assert r.returncode==code,r.stdout+r.stderr
 run(['validate','examples/after.json'],0)
 out=Path(tmp)/'diff.json';run(['diff','examples/before.json','examples/after.json','--output',str(out)],0)
 assert json.loads(out.read_text(encoding='utf-8'))['changes'][0]['change']=='explicitly_passed'
 run(['html','examples/before.json','--output',str(Path(tmp)/'report.html')],1)
 run(['normalize','ad','examples/ad-source.synthetic.json','--output',str(Path(tmp)/'ad.json')],0)
 run(['normalize','guard','examples/guard-source.synthetic.json','--scope','synthetic-materials','--observed-at','2026-10-12T00:00:00Z','--synthetic','--output',str(Path(tmp)/'guard.json')],1)
print(f'OK: {len(ru)} RU/EN page pairs, links and executable guide examples')
