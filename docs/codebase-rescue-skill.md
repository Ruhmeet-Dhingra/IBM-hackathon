---
name: codebase-rescue
description: Use this skill when a codebase contains multiple overlapping generations of the same subsystems (e.g. v1/v2 packages, duplicate UIs, several LLM entry points) and no longer runs, OR when you want a focused check on part of a codebase (a single file, only imports, only dead code, or a review pass).
metadata:
  disable-model-invocation: true
  argument-hint: "[inspect only | <path/to/file> | --imports | --dead-code | --review]"
---

# Codebase Rescue

## Usage / Scope modes

Read the argument after the command and choose the matching scope. If no argument is given, run the full rescue.

| Invocation | Scope |
|---|---|
| `/codebase-rescue` | Full rescue of the whole open codebase (all phases below). |
| `/codebase-rescue inspect only` | Phase 1 only — read-only analysis, produce the report and diagram, make NO changes. |
| `/codebase-rescue <path/to/file>` | Restrict all analysis and fixes to the single named file (and its direct imports). |
| `/codebase-rescue --imports` | Only detect and report broken imports, misspelled packages, and phantom references (symbols called but never defined). Read-only unless asked to fix. |
| `/codebase-rescue --dead-code` | Only identify unreachable / superseded / orphaned code and propose what to quarantine. Read-only; do not move anything without confirmation. |
| `/codebase-rescue --review` | Run a security and code-quality review of the target (secrets, unsafe calls, overly permissive settings, duplication) and produce a findings report. Read-only. |

For any read-only mode, never edit files — produce the report only. For scoped modes, keep the output limited to the requested scope; do not expand into a full rescue unless asked.

---

## Phase 1 — Inspect (read-only, make no changes)

1. Identify the single intended entry point and trace the end-to-end runtime flow from it. (For a single-file scope, treat that file as the target and trace only its imports/uses.)
2. Inventory every subsystem in scope. For each duplicate/parallel implementation, label it **CANONICAL** (newest, on the runtime path) or **DEAD** (older, superseded, or orphaned). Output a table with file + reason.
3. Produce a "run-blocker" list: broken/wrong imports, misspelled packages, phantom references (functions, classes, or enum members called but never defined), duplicate definitions, and gaps between the real dependencies and the dependency manifest. Give file + line.
4. Generate an architecture diagram (Mermaid) showing the canonical spine, with dead/orphaned modules in a separate "quarantined" subgraph. (Skip for single-file or `--imports` scope.)
5. Present the canonical/dead map and the plan, and **STOP for confirmation** before making any changes. For any read-only scope (`inspect only`, `--imports`, `--dead-code`, `--review`), stop here and do not proceed to Phase 2.

---

## Phase 2 — Fix (only after the map is confirmed)

### Independent blockers (may be done in parallel)
- Rebuild the dependency manifest.
- Fix filename/import typos.
- Correct invalid model/config names.
- Create missing runtime directories.
- Deduplicate copy-pasted blocks.
- Convert malformed data structures to their correct typed form.

### Dependent blockers (fix in order)
- Register any actions the canonical path emits only after the code that emits them is correct.
- Verify the manifest before running an install.

### Quarantine (never delete)
- Move every DEAD file/directory into a top-level `_quarantine/` folder, preserving relative paths, so the change is reversible and reviewable.
- Never quarantine a file that the canonical spine still imports — a file used by both a canonical and a dead module is **canonical**. Watch for single "bridge" files.

---

## Phase 3 — Verify

1. Confirm the canonical entry point imports with no `ImportError`.
2. Run the test suite and get it green. If no tests exist for the spine, add minimal smoke tests that exercise the main runtime path.
3. Open a pull request (or produce a summary) describing what was quarantined, what was fixed, and the before/after state (does-it-run, tests passing, blockers closed).

---

## Rules

- Treat all pre-existing subsystems as the target codebase, never as something newly created by this skill.
- Do not infer a file is dead based on its name alone — verify it is not reachable from the entry point before quarantining.
- Prefer the newest coherent implementation as canonical.
- Never delete; always quarantine.
- Always propose the CANONICAL/DEAD map and wait for confirmation before Phase 2.
- Respect the requested scope: a scoped or read-only invocation must not silently turn into a full rescue.
