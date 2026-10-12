# CLI and exit codes

Commands: validate INPUT; diff BEFORE AFTER [--output NEW_FILE]; html INPUT --output NEW_FILE; normalize guard INPUT --scope LABEL --observed-at UTC [--synthetic] --output NEW_FILE; normalize ad INPUT --output NEW_FILE. No filename guessing or auto source detection. Python module invocation is equivalent to the installed opsec-report command.

Validation/normalization/HTML return the normalized assessment code: 0 no fail and complete declared coverage, 1 any fail, 2 incomplete coverage without fail, 3 invalid input/output/runtime. A successfully written fail HTML still exits 1. Diff returns 0 for comparable reports, 2 for incompatible context, 3 on invalid input/output. Diff 0 does not mean no changes or no risk. Output files must not exist. Standard JSON diagnostics use static codes, never exception text/source paths.

For Guard, context is required because source response-0.2 has no scope label/time/synthetic provenance field suitable for automatic inference. --synthetic sets true; without it provenance is declared non-synthetic, not independently verified. For AD that class comes from the source. Input uses strict UTF-8 without BOM; non-JSON constants and duplicate keys are rejected.

---

[Documentation index](index.md) · [Русский](../ru/cli-reference.md)
