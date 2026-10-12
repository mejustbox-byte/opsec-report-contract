# Contract opsec-1.0

Required top-level fields: schema_version, producer(name/version/ruleset), run(id/scope/observed_at/synthetic), coverage_complete, summary, results and coverage_gaps. UTC timestamps use an ISO date/time ending Z; calendar validity is checked. Additional fields are rejected. Schema is bundled in the package and never retrieved remotely.

Statuses: pass means an explicit declared successful check; fail a declared finding; not_tested unavailable/unknown/not-run; not_applicable an explicit scope decision. Summary counts all four states exactly. Coverage is complete only for a nonempty result list, no coverage gaps and no not_tested results. A set entirely not_applicable is complete within its declaration, not evidence of a performed check. Absence never manufactures a pass.

The pair (check_id,asset_id) is unique. One record may have up to 128 distinct evidence refs. redacted must be true; refs are opaque strings and are never dereferenced. Redacted is an assertion, not automatic sanitization of arbitrary messages. Producer version and ruleset determine comparison compatibility. Source identity, signatures, hashes and underlying evidence truth are not authenticated.

---

[Documentation index](index.md) · [Русский](../ru/contract.md)
