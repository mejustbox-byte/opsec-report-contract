# Threat model and trust boundaries

Assets: private input reports, normalized identifiers/evidence refs, local output files and reviewer interpretation. Attacker controls input JSON and source narrative. Relevant threats: malformed/deep/large input, duplicate keys, fake complete coverage, silent status loss, HTML/script injection, remote schema retrieval and output overwrite.

Controls: bounded regular-file loader, strict JSON, schema/no extra fields, consistency checks, identity uniqueness, conservative adapters/diff, escaped HTML+CSP, network-denied references and exclusive writes. A fabricated but internally consistent pass can still validate: this is not evidence authentication. Arbitrary messages can still disclose secrets; redacted=true is not a sanitizer. Local code/dependencies and the OS are trusted.

Residual risks: source authenticity, TOCTOU/ancestor replacement, hardlinks, parser/runtime defects, no hard RAM/CPU quota, identifier reidentification, stale evidence and incomplete producer validation. Do not publish real source fixtures. Test isolation and runtime patching are independent operator responsibilities; no remediation or credential/network probing occurs.

---

[Documentation index](index.md) · [Русский](../ru/threat-model.md)
