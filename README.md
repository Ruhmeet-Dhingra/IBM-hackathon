# ROV Codebase Rescue — IBM Bob TechXchange 2026 Submission

Using **IBM Bob 2.0**, I built a reusable **`codebase-rescue`** skill and applied it to ROV — a
broken, multi-generation voice-assistant codebase — turning it from *won't-import* into a single,
documented, tested, installable project.
---

## The problem

ROV is a  voice assistant(devloped prior to the hackathon and is a pre-existing codebase used as the rescue target)
that grew across several development generations without cleanup.
It accumulated duplicate versions of the same subsystems — **2 brain packages, 2 core packages,
3 plugin systems, 4 disconnected UIs, and 5 LLM entry points** — with no indication of which was
current. The result: **the application no longer ran.** It crashed on import before any code
executed, its dependency file was corrupted, and no automated test could even be collected. A new
contributor could not clone, install, or run it.

## What I built

A reusable **IBM Bob skill**, `codebase-rescue`, that rescues any multi-generation codebase in
three phases — **Inspect → Fix → Verify** — and supports scoped modes for focused checks. The
skill (not the one-off edits) is the deliverable: it can be re-run on any codebase with a single
command.

## Results

| | Before | After |
|---|---|---|
| Imports? | Crashes on `main.py:6`| Imports cleanly |
| Tests passing | 0 (none runnable)| 5 / 5 |
| Broken imports / phantom references | ~31 documented | 0 |
| `requirements.txt` | 3 corrupted UTF-16 lines| Full clean dependency list |
| Architecture | 2 brains, 2 cores, 3 plugin systems, 4 UIs| 1 canonical spine; 28 dead files quarantined |
| Bobcoins used | —| ~8 of 40 |

The entire rescue cost roughly 8 of 40 allocated Bobcoins, because the workflow front-loads a
cheap read-only inspection before spending anything on edits.

## How the skill works
so the overall codebase-rescue works in 3 phases 

- 1. **Inspect (read-only)(plan mode was used):** trace the entry point, classify every subsystem as CANONICAL or DEAD,
  list every run-blocker with file-and-line references, generate an architecture diagram, and
  stop for confirmation.
- 2. **Fix:(agent mode was used)** repair independent blockers first, then dependent ones, then quarantine (follows a never delete policy)
  dead code into a reversible folder, preserving any "bridge" file the spine still needs.
- 3. **Verify:** confirm the entry point imports and the tests pass.

## Repository structure

- **`docs/`** — artifacts IBM Bob generated: `rov_inspection.md` (full analysis + run-blocker
  inventory), `rov_architecture.md` (Mermaid diagram), `codebase-rescue-skill.md` (the reusable
  skill), and the before/after and imports-scan reports.
- **`bob_sessions/`** — IBM Bob task session summaries (evidence of Bob usage per task).
- **`_quarantine/`** — dead code moved out of the canonical spine (reversibly, not deleted).
- **Canonical spine** — `main.py`, `brain_v2/`, `router/`, `skills/`, `core_v2/`, `voice/`,
  `ai/rag.py`, and the `core/audio.py` bridge file.

## sub skills 
/codebase-rescue Full rescue of the open codebase

/codebase-rescue inspect only Read-only analysis, no changes

/codebase-rescue <path/to/file> Focus on a single file

/codebase-rescue --imports Check only broken imports & phantom references

/codebase-rescue --dead-code Find dead / unreachable code

/codebase-rescue --review Security & code-quality pass



> **Note:** ROV is a pre-existing codebase used as the rescue *target*. The hackathon
> contribution is the Bob-driven `codebase-rescue` skill and the fixes it applied during the
> contest — see the commit history and `bob_sessions/` for proof.


