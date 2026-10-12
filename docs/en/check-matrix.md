# Verification matrix

R1: loader/schema/type/redaction/date/size/depth tests. R2: four states, empty scope, duplicate identity, summary/coverage contradictions. R3: missing-after, explicit pass, coverage loss and incompatible context. R4: HTML escaped script/image sentinels, CSP/no-network. R5: actual AD producer fixture, unknown mapping, Guard no-pass inference, source contradictions. R6: CLI codes and exclusive output; clean installed smoke verified separately. R7: paired docs/links and executable synthetic examples.

Sixteen unittest methods currently pass locally on Linux/Python 3.12 with pinned validation dependencies. The supplied CI matrix covers Linux/Windows/macOS/Python 3.13 when run; its execution is not claimed here. Minimal source fixtures are not Windows AD verification. Static HTML escaping tests are not a complete browser-security proof. This package has not been published as a GitHub release or PyPI package.

Producer reference: AD commit 6c5687f7ffe0f57825bb29ff86453c6b4e9a914e, publication core response-0.2 from Guard 0.3.0a1. These identify inspected structures, not signatures or real environment state.

---

[Documentation index](index.md) · [Русский](../ru/check-matrix.md)
