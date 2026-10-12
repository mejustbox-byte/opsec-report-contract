# Architecture and data flow

CLI → bounded UTF-8 loader → optional explicit producer adapter → bundled schema validator → cross-field invariants → normalized JSON/diff/static HTML. Core functions operate on dictionaries; file loading and exclusive output creation are separate. No network collector, remote API, database or background service is present.

Limits: 8,000,000 input bytes; nesting depth 64 before JSON parse; 10,000 results and gaps; bounded field lengths and 128 refs per record. These bound declared input and output shapes, not hard total RAM/CPU. Validation uses pinned jsonschema/referencing with network retrieval denied. Invalid loader/schema/data never downgrade to success.

HTML is static text plus local CSS, with escaped text and CSP default-src none, base-uri none and form-action none. No user-controlled links/images/scripts are emitted. Output writes use exclusive creation and reject symlink targets. Existing files are not overwritten. Paths and text may remain sensitive even when executable markup is neutralized.

---

[Documentation index](index.md) · [Русский](../ru/architecture.md)
