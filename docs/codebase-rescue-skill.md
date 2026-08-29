---
name: codebase-rescue
description: Use when a codebase contains multiple overlapping generations of the same subsystems (e.g. v1/v2 packages, duplicate UIs, several LLM entry points) and no longer runs end-to-end. Guides Bob through inspect, fix, and verify phases.
metadata:
  disable-model-invocation: true
---

# Codebase Rescue

Use this skill when a codebase contains multiple overlapping generations of the same subsystems
(e.g. v1/v2 packages, duplicate UIs, several LLM entry points) and no longer runs end-to-end.

---

## Phase 1 — Inspect (read-only, make no changes)

1. **Identify the entry point and trace the runtime flow.**
   - Read top-level files (`main.py`, any `.pyw` launcher, `__main__` blocks) using `read_file`.
   - Determine what the codebase does and identify the single intended entry point.
   - Trace the full end-to-end runtime flow from that entry point through every layer it touches.

2. **Inventory every subsystem.**
   - Use `list_files` (recursive) and `GetSymbolsOverview` to map all packages and modules.
   - For every duplicate or parallel implementation, label it:
     - **CANONICAL** — newest version, on the active runtime path.
     - **DEAD** — older, superseded, or orphaned (not reachable from the entry point).
   - Present this as a table: `Module | File | Label | Reason`.
   - Cover at minimum: brain/logic layers, core/service layers, plugin systems, UI front-ends, LLM entry points.

3. **Produce a run-blocker list.**
   - Use `grep` and `read_file` to check every import in every canonical file.
   - List every concrete blocker with file + line:
     - Missing or misspelled module names (including filename typos).
     - Phantom references — functions, classes, or enum members that are called but never defined anywhere.
     - Duplicate definitions that silently override a working version.
     - Malformed data structures (e.g. raw enum values where typed dataclass instances are required).
     - Actions/routes emitted by the planner or router that have no registered handler.
     - Gaps between real runtime dependencies and the dependency manifest (`requirements.txt`, `pyproject.toml`, etc.).
     - A corrupted or unreadable dependency manifest.

4. **Generate a Mermaid architecture diagram.**
   - Show the canonical runtime spine as the main flowchart.
   - Show all dead/orphaned modules in a separate `subgraph` labelled "Quarantined — Dead Code".
   - Include the diagram in the chat response (do not save it yet — that comes after confirmation).

5. **Present findings and STOP.**
   - Output: the CANONICAL/DEAD table, the numbered blocker list, and the Mermaid diagram.
   - Ask the user to confirm the map is correct before proceeding to Phase 2.
   - Do not edit, create, or delete any file until the user explicitly confirms.

---

## Phase 2 — Fix (only after Phase 1 is confirmed)

6. **Fix independent blockers first** (no mutual dependencies — parallelisable):
   - Rebuild the dependency manifest as a clean, correctly-encoded UTF-8 file listing all real runtime dependencies.
   - Fix filename typos and update every import that references the old name.
   - Correct invalid model names, API identifiers, or configuration values.
   - Create missing runtime directories (e.g. `plugins/installed/`, `plugins/staged/`) with a `.gitkeep`.
   - Remove copy-pasted duplicate code blocks (keep the first, delete the verbatim repeat).
   - Convert every malformed data structure to its correct typed form (e.g. replace raw enum values in a `steps` list with proper typed dataclass instances).

7. **Fix dependent blockers in order:**
   - Register any actions or routes that the canonical path emits — but only after the code that emits them is correct.
   - Verify the dependency manifest is clean before running an install command.
   - Fix any other blocker whose fix depends on a prior step being complete.

8. **Quarantine dead code — never delete.**
   - Move every DEAD file and directory into a top-level `_quarantine/` folder, preserving relative paths inside it.
   - Before moving anything, verify the file is not imported by any canonical module (watch for single "bridge" files that straddle both worlds — keep those in place).
   - Use `apply_diff` or `search_and_replace` to update any canonical import that pointed at a file being moved.

---

## Phase 3 — Verify

9. **Confirm the canonical entry point imports cleanly.**
   - Run `python -c "from <entry_module> import <MainClass>"` (or equivalent) using `execute_command`.
   - There must be zero `ImportError`, `ModuleNotFoundError`, or `AttributeError` on import.

10. **Run the test suite and get it green.**
    - If a test suite exists, run it with `execute_command` and fix any failures caused by the Phase 2 changes.
    - If no tests exist for the canonical spine, add minimal smoke tests that exercise the main runtime path end-to-end.

11. **Open a pull request / write a summary.**
    - Describe what was quarantined, what was fixed, and the before/after state:
      - Does it run? (Yes/No before → Yes after)
      - Tests passing? (count before → count after)
      - Blockers closed (list each one by number from Phase 1).

---

## Rules

- Treat all pre-existing subsystems as the target codebase — never as something this skill created.
- Prefer the **newest coherent implementation** as canonical when generations conflict.
- **Never delete; always quarantine.** Every removal is reversible.
- **Always present the CANONICAL/DEAD map and wait for explicit confirmation before Phase 2.**
- Do not infer that a file is dead based on its name alone — verify it is not reachable from the entry point.
- A file used by both a canonical and a dead module is canonical; quarantine only the dead module that references it.
