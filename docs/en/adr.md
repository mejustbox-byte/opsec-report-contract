# Architecture decisions

ADR-001 accepted: Python 3.12+ and pinned jsonschema, rather than a home-grown complete schema interpreter. The published Draft 2020-12 schema is structural authority; additional cross-field checks address counts/coverage/identity. Version pins are not hash-locked supply-chain verification.

ADR-002 accepted: keep all four statuses and conservative identity matching. No inferred pass from absent finding. Diff requires unchanged producer/rules/scope/provenance class; override flags would make findings misleading and are not shipped.

ADR-003 accepted: static escaped HTML rather than an interactive server. No document transfer or dependency on CDN assets. ADR-004 accepted: lossy, explicitly named adapters preserve state and discard raw source narrative by default. Upstream contracts do not change. Full producer-specific source validation and cryptographic provenance are future work.

---

[Documentation index](index.md) · [Русский](../ru/adr.md)
