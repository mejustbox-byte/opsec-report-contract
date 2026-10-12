# Comparison semantics

Both reports are validated before comparison. Different producer name, version, ruleset, scope or synthetic provenance class produce comparable=false and reasons, with no changes. Time and run ID may differ. Matching identity pairs are compared deterministically; field differences can appear as changed even when status is unchanged.

Transition labels: added, not_observed, explicitly_passed, coverage_lost, changed. Only fail→pass yields explicitly_passed. Missing-after is not_observed, never resolved. Pass/fail→not_tested is coverage_lost. Global coverage flags remain visible on a comparable diff. The comparison does not establish that a remediation action happened or that the environment was otherwise unchanged.

Asset renaming appears as disappearance/addition. There is no heuristic identity matching, merging across organizations or version override. A Guard source exposing only findings cannot prove an explicit later pass; its missing finding remains not_observed. This conservative behavior is intentional.

---

[Documentation index](index.md) · [Русский](../ru/comparison.md)
