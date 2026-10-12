# Purpose and acceptance

The product defines a shared result language and local consumer tools, not an infrastructure collector. Every record has a stable check/asset identity, one of four statuses, severity, human message, remediation and redacted evidence references. Unknown schema, malformed JSON and contradictory declarations fail closed. Empty reports remain incomplete.

Acceptance gates: R1 strict shape/loader; R2 derived summary and coverage; R3 conservative diff; R4 escaped self-contained HTML; R5 adapters checked against actual producer structures; R6 installable CLI with schema data; R7 bilingual executable examples. Sources remain unmodified and outputs use exclusive creation. No remediation commands, remote services or dynamic plugins are executed.

The alpha covers core Publication Guard response-0.2 and AD report_schema_version=1. Guard bundles/documents/secrets and the remaining auditors require future explicit adapters. This does not retrofit or alter those producers. HTML/reports can contain identifying asset/scope/message metadata and need an independent publication review.

---

[Documentation index](index.md) · [Русский](../ru/requirements.md)
