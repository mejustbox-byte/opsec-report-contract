# Installation and reproducible examples

Use Python 3.12+ with current patches. From the unpacked source root, create a private environment and install the package. Exact runtime pins are supplied; installation may download packages, report processing does not. On Windows use python/py -3 and .venv\Scripts paths.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/opsec-report validate examples/after.json
.venv/bin/opsec-report diff examples/before.json examples/after.json --output comparison.json
.venv/bin/opsec-report html examples/before.json --output report.html
```
The first example validates explicit synthetic passes (0), diff produces explicitly_passed (0), and HTML is written but returns finding status 1. All output paths must be new. To rerun, choose different output names; never overwrite evidence merely to make a command succeed.

Normalize the inspected AD producer fixture (0); normalize Guard findings (1) with explicit context:

```bash
.venv/bin/opsec-report normalize ad examples/ad-source.synthetic.json --output normalized-ad.json
.venv/bin/opsec-report normalize guard examples/guard-source.synthetic.json --scope synthetic-materials --observed-at 2026-10-12T00:00:00Z --synthetic --output normalized-guard.json
```
Guide examples do not establish real infrastructure safety. Keep identifying sources private and inspect normalized scope/asset strings before sharing. HTML has no JavaScript/network assets and can be opened locally; arbitrary report text is not automatically redacted.

---

[Documentation index](index.md)
