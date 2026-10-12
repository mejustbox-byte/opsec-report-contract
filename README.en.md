# OPSEC Report Contract

**Versioned JSON · Four honest statuses · Coverage-aware diff · Static HTML**

A local result contract and consumer toolkit for OPSEC auditors. Explicit pass/fail/not_tested/not_applicable, strict validation and comparisons that never label a missing finding as fixed. Two inspected adapters preserve source uncertainty rather than inventing passes.

**0.1.0a1 local candidate.** Hosted CI and release are pending. Producer authenticity and real infrastructure safety are not established by normalized reports.

[Русский](README.ru.md) · [Handbook](docs/en/index.md) · [Install/examples](docs/en/user-guide.md) · [Contract](docs/en/contract.md) · [Adapters](docs/en/adapters.md)

```bash
python3 -m pip install .
opsec-report validate examples/after.json
opsec-report diff examples/before.json examples/after.json --output comparison.json
opsec-report html examples/before.json --output report.html
```

Codes: 0 completed declared scope, 1 findings, 2 incomplete scope/incomparable diff, 3 invalid input/output/runtime. Diff 0 means compatible, not risk-free. HTML generation retains assessment status. Existing output files are never overwritten.

Sixteen local unittest methods verify status/coverage, strict parsing, conservative diff, HTML escaping, adapters and CLI codes. Source examples are synthetic. Guard adapter supports core response-0.2; AD supports report schema 1. Other envelopes/auditors remain planned. No network collector, automatic remediation or privacy sanitizer.

[MIT license](LICENSE). Reports may retain identifying metadata; a valid schema is not publication authorization.
