# ROV Codebase Inspection Report

> Read-only analysis — no files were modified to produce this report.

---

## 1. What ROV Is — Purpose and Canonical Runtime Flow

**ROV** ("Robotic / Responsive Operating Voice") is a Windows desktop voice assistant. It listens for a wake word ("Hey Jarvis"), records and transcribes the user's speech, passes the transcript through an intent/entity/planning pipeline (the "Brain"), dispatches the resulting execution plan to registered skills (opening apps, searching the web, querying a knowledge base, managing AI-generated plugins), and speaks a reply via TTS.

### Canonical Entry Points

There are two:

| File | Role |
|---|---|
| `main.py` | Development/foreground launcher — `python main.py` |
| `rov_background.pyw` | Production Windows background service — acquires a single-instance mutex, waits 8 s, then imports and starts `ROV()` from `main.py` |

**`rov_background.pyw` is the single intended production entry point.** Everything starts with `ROV().start()`.

### End-to-End Runtime Flow

```
rov_background.pyw → main.ROV() ctor
  │
  ├─ voice.detector.WakeWordDetector(callback=on_wake)   ← openwakeword, 16 kHz mic
  ├─ voice.recorder.Recorder()                           ← sounddevice/soundfile
  ├─ brain_v2.brain.Brain()                              ← full NLU pipeline
  └─ router.router.Router()  →  router.registry.SkillRegistry()
       ├─ skills.application.ApplicationSkill → core_v2.app
       ├─ skills.browser.BrowserSkill         → core_v2.browser
       ├─ skills.plugin.PluginSkill           → plugins.proposals / plugins.runtime
       └─ skills.knowledge.KnowledgeSkill     → ai.rag (Gemini embeddings)

ROV.start()
  └─ detector.start()   ← starts sounddevice InputStream in background thread
  └─ start_tray()       ← pystray system-tray icon (main thread blocks here)

[on wake-word crossing threshold]
  on_wake() ─ thread
    1. speaker.speak("Yes sir.")            ← edge_tts + VLC
    2. recorder.record()  → command.wav
    3. voice.wisper_engine.transcribe(wav)  ← faster_whisper
    4. brain_v2.Brain.process(text)
         normalize → intent → entities → plan → reason → validate
    5. router.Router.execute(plan)
         per Step: registry.get(action) → skill.execute(step)
    6. speaker.speak(reply)
```

---

## 2. Generational Map — Canonical vs Dead

### Brain Layers

| Module | File | Label | Reason |
|---|---|---|---|
| `brain_v2.brain.Brain` | `brain_v2/brain.py` | **CANONICAL** | Imported by `main.py:9` |
| `brain_v2.intent_recognizer` | `brain_v2/intent_recognizer.py` | **CANONICAL** | Used by Brain v2 |
| `brain_v2.entity_extractor` | `brain_v2/entity_extractor.py` | **CANONICAL** | Used by Brain v2 |
| `brain_v2.planner` | `brain_v2/planner.py` | **CANONICAL** | Used by Brain v2 |
| `brain_v2.normalizer` | `brain_v2/normalizer.py` | **CANONICAL** | Used by Brain v2 |
| `brain_v2.reasoning` | `brain_v2/reasoning.py` | **CANONICAL** | Used by Brain v2 |
| `brain_v2.validator` | `brain_v2/validator.py` | **CANONICAL** | Used by Brain v2 |
| `brain_v2.models` | `brain_v2/models.py` | **CANONICAL** | Shared dataclasses |
| `brain_v2.entities` | `brain_v2/entities.py` | **CANONICAL** | `Action` / `EntityType` enums |
| `brain_v2.intents` | `brain_v2/intents.py` | **CANONICAL** | `Intent` enum + keyword sets |
| `brain_v2.gemini_provider` | `brain_v2/gemini_provider.py` | **CANONICAL** | `GeminiProvider` class |
| `brain_v2.execution_plan` | `brain_v2/execution_plan.py` | **DEAD** | Unused orphan dataclass, superseded by `brain_v2.models.Plan` |
| `brain_v2.json_parser` | `brain_v2/json_parser.py` | **DEAD** | Never imported; contains two duplicate definitions of `parse_json` and `normalize` pasted one after the other |
| `brain_v2.prompt_builder` | `brain_v2/prompt_builder.py` | **DEAD** | Imports from `brain.intents.INTENTS` (does not exist); never used |
| `brain.brain.Brain` | `brain/brain.py` | **DEAD** | v1; entry point uses v2 |
| `brain.intent_engine` | `brain/intent_engine.py` | **DEAD** | v1 component |
| `brain.entity_extractor` | `brain/entity_extractor.py` | **DEAD** | v1 component |
| `brain.planner` | `brain/planner.py` | **DEAD** | v1 component |
| `brain.intents` / `brain.entities` | `brain/intents.py` / `brain/entities.py` | **DEAD** | Duplicate enums from v1; `brain.intents` lacks plugin intents |
| `brain.gemini` | `brain/gemini.py` | **DEAD** | Uses `google.genai` (newer SDK) vs v2's `google.generativeai`; never imported by canonical path |
| `brain.context_manager` / `brain.working_memory` | `brain/context_manager.py` / `brain/working_memory.py` | **DEAD** | v1 context stack |

### Core / Service Layers

| Module | File | Label | Reason |
|---|---|---|---|
| `core_v2.app` | `core_v2/app.py` | **CANONICAL** | Used by `skills/application/actions.py` |
| `core_v2.app_index` | `core_v2/app_index.py` | **CANONICAL** | Used by `core_v2.app` |
| `core_v2.browser` | `core_v2/browser.py` | **CANONICAL** | Used by `skills/browser/actions.py` |
| `core_v2.core_types` | `core_v2/core_types.py` | **CANONICAL** | `OperationResult` dataclass |
| `core_v2.process` | `core_v2/process.py` | **CANONICAL** | Process management |
| `core.audio` | `core/audio.py` | **CANONICAL** | Creates the global `speaker` singleton imported by `main.py:8` — this one live file bridges the dead `core/` package into the canonical path |
| `core.app` | `core/app.py` | **DEAD** | v1 app launcher; depends on dead `core.memory` dict |
| `core.browser` | `core/browser.py` | **DEAD** | v1; imports `pyautogui` |
| `core.commands` | `core/commands.py` | **DEAD** | v1 command executor; imports phantom `core.typing` |
| `core.dispatcher` | `core/dispatcher.py` | **DEAD** | v1 input dispatcher; imported by `ui.py` (dead UI) |
| `core.router` | `core/router.py` | **DEAD** | v1 router; imports phantom `brain_v2.gemini_provider.ask` |
| `core.executor` | `core/executor.py` | **DEAD** | v1 executor |
| `core.intent` | `core/intent.py` | **DEAD** | v1 keyword dict |
| `core.parser` | `core/parser.py` | **DEAD** | v1 text parser |
| `core.nlp` | `core/nlp.py` | **DEAD** | v1 normalizer, superseded by `brain_v2.normalizer` |
| `core.files` | `core/files.py` | **DEAD** | v1 file creation |
| `core.file` | `core/file.py` | **DEAD** | v1 file ops; imports `from voice.speaker import speak` (a class method, not a free function) |
| `core.memory` | `core/memory.py` | **DEAD** | v1 plain-dict state |
| `core.logger` | `core/logger.py` | **DEAD** | Timestamp printer used only by dead `core/` modules |
| `core.system` | `core/system.py` | **DEAD** | Lock-screen helper; used only by dead `core.router` |
| `core.test_intent` | `core/test_intent.py` | **DEAD** | Script importing `from intent import detect_intent` — broken, file in wrong place |

### Plugin System

| Module | File | Label | Reason |
|---|---|---|---|
| `plugins.plugin` | `plugins/plugin.py` | **CANONICAL** | Abstract base `Plugin` class |
| `plugins.runtime` | `plugins/runtime.py` | **CANONICAL** | Dynamic plugin executor |
| `plugins.proposals` | `plugins/proposals.py` | **CANONICAL** | Proposal / approval workflow |
| `plugins.gemini_generator` | `plugins/gemini_generator.py` | **CANONICAL** | AI code generation |
| `plugins.plugin_loader` | `plugins/plugin_loader.py` | **DEAD** | Uses `manifest.json` scheme inconsistent with canonical `proposal.json` scheme; broken import `from plugin import Plugin` |
| `plugins.plugin_registry` | `plugins/plugin_registry.py` | **DEAD** | Older registry; broken import `from plugin import Plugin` |

### UI Front-Ends

| Module | File | Label | Reason |
|---|---|---|---|
| `main.ROV.start_tray` (pystray) | `main.py:164` | **CANONICAL** | The production UI — tray icon + Tkinter dialog prompt, wired to `on_text_command` |
| `uib.app` | `uib/app.py` | **DEAD** | More elaborate CTk UI; not wired into `main.py`; no connection to Brain v2 |
| `ui.py` | `ui.py` | **DEAD** | Legacy CTk UI; imports broken `core.dispatcher.process_input` |
| `studio` | `studio/` | **DEAD** | PySide6 developer dashboard; standalone, not imported anywhere in runtime path |

### Gemini / LLM Entry Points

| Module | File | Label | Reason |
|---|---|---|---|
| `brain_v2.gemini_provider.GeminiProvider` | `brain_v2/gemini_provider.py` | **CANONICAL** | Uses `google.generativeai`, correct SDK for v2 path |
| `plugins.gemini_generator.GeminiPluginGenerator` | `plugins/gemini_generator.py` | **CANONICAL** | Plugin code generation |
| `ai.rag` | `ai/rag.py` | **CANONICAL** | Embeddings + knowledge-base search; uses `google.genai` (newer SDK) |
| `ai.chat` | `ai/chat.py` | **DEAD** | Simple chat wrapper; uses `google.generativeai`; imported only by dead `core.dispatcher` |
| `brain.gemini` | `brain/gemini.py` | **DEAD** | v1 Gemini wrapper; uses `google.genai`; imported only by dead `core.router` via phantom `ask` |

---

## 3. Why It Doesn't Run — Concrete Failure Inventory

### A. Import Failures at Module-Load Time

These block startup immediately when Python tries to import `main`.

| # | File | Line | Problem |
|---|---|---|---|
| 1 | `main.py` | 6 | `from voice.wisper_engine import transcribe` — **filename is `wisper_engine.py`** (missing `h`). Also a side-effect import: `WhisperModel` is instantiated on module load. |
| 2 | `main.py` | 8 | `from core.audio import speaker` chains to `voice.speaker.Speaker()` at import time. `vlc` is a C-extension (`python-vlc`) that requires VLC to be installed on the system. |
| 3 | `brain_v2/gemini_provider.py` | 9 | `import google.generativeai as genai` — the pip package `google-generativeai` is not in `requirements.txt`. |
| 4 | `brain_v2/gemini_provider.py` | 30 | `genai.GenerativeModel("gemini-3.5-flash")` — the model `"gemini-3.5-flash"` **does not exist** in the Gemini API. Real names are `"gemini-1.5-flash"` or `"gemini-2.0-flash"`. Raises a 404/API error at runtime. |
| 5 | `voice/detector.py` | 6 | `from openwakeword import Model` — `openwakeword` is not in `requirements.txt`. |
| 6 | `voice/wisper_engine.py` | 1 | `from faster_whisper import WhisperModel` — `faster-whisper` is not in `requirements.txt`. |
| 7 | `voice/speaker.py` | 2 | `import edge_tts` — `edge-tts` is not in `requirements.txt`. |
| 8 | `voice/speaker.py` | 5 | `import vlc` — pip package is `python-vlc`, not in `requirements.txt`. |
| 9 | `tray_icon_helper.py` | 2 | `from PIL import Image` — `Pillow` not in `requirements.txt`. |
| 10 | `brain_v2/brain.py` | 19 | `from plugins.runtime import PluginRuntime` — instantiation at Brain `__init__` reads `plugins/installed/`, which does not exist in the repo; causes `FileNotFoundError` on first run. |

### B. Phantom References — Symbols Called That Were Never Defined

| # | File | Line | Symbol Called | Reality |
|---|---|---|---|---|
| 11 | `core/router.py` | 1 | `from brain_v2.gemini_provider import ask` | `ask` is **not defined** in `brain_v2/gemini_provider.py`; only `GeminiProvider.generate()` exists. |
| 12 | `core/commands.py` | 5 | `from core.typing import type_text` | `core/typing.py` **does not exist** anywhere in the codebase. |
| 13 | `core/commands.py` | 2 | `from voice.speaker import speak` | `speak` is a **method on `Speaker`**, not a free function; no module-level `speak()` is exported. |
| 14 | `core/file.py` | 3 | `from voice.speaker import speak` | Same phantom free function as #13. |
| 15 | `core/test_intent.py` | 1 | `from intent import detect_intent` | There is no top-level `intent.py`; the function lives in `core.intent`. |
| 16 | `brain_v2/prompt_builder.py` | 3 | `from brain.intents import INTENTS` | `INTENTS` is **not defined** in `brain/intents.py`; that module only contains the `Intent` enum. |
| 17 | `skills/developer/skill.py` | 25 | `Action.ANALYZE_PROJECT` | **Not a member** of `brain_v2.entities.Action`. |
| 18 | `skills/developer/skill.py` | 31 | `Action.REVIEW_CODE` | **Not a member** of `brain_v2.entities.Action`. |
| 19 | `skills/developer/skill.py` | 37 | `Action.CREATE_PROJECT` | **Not a member** of `brain_v2.entities.Action`. |

### C. Duplicate Definitions — Silent Logic Corruption

| # | File | Lines | Problem |
|---|---|---|---|
| 20 | `brain_v2/json_parser.py` | 4 + 36 | `parse_json()` defined twice; second definition body is `...` (stub), overrides the working first. |
| 21 | `brain_v2/json_parser.py` | 24 + 41 | `normalize()` defined twice; also has stray `import json` mid-file at line 26. |
| 22 | `core_v2/browser.py` | 39 + 73 | `search_google()` defined twice; second definition silently overrides the first. |
| 23 | `voice/detector.py` | 47–56 + 58–67 | The entire trigger-detection block is pasted twice inside `audio_callback`; the second `triggered` variable silently overrides the first. |
| 24 | `brain_v2/planner.py` | 64–68 + 77–81 | `elif intent == Intent.SHOW:` block pasted twice; second copy is unreachable dead code. |

### D. Structural Bugs in the Canonical Planner

| # | File | Lines | Problem |
|---|---|---|---|
| 25 | `brain_v2/planner.py` | 38–40 | `plan.steps = [Action.OPEN_WEBSITE]` — puts a raw **`Action` enum member** into `steps`, not a `Step` dataclass. Router calls `step.action`, which crashes with `AttributeError`. |
| 26 | `brain_v2/planner.py` | 43–46 | `plan.steps = ["locate_project", "open_project"]` — puts raw **strings** into steps. Same crash. |
| 27 | `brain_v2/planner.py` | 66–68 | `plan.steps = [Action.SHOW_COMPONENT]` — raw enum, not `Step`. |
| 28 | `brain_v2/planner.py` | 103–105 | `plan.steps = [Action.GENERATE_PLUGIN]` — raw enum, not `Step`. |
| 29 | `brain_v2/planner.py` | 86–90 | `plan.steps = [Action.HIDE_COMPONENT]` — raw enum, not `Step`. |
| 30 | `router/registry.py` | 33–57 | `Action.OPEN_WEBSITE`, `Action.SHOW_COMPONENT`, `Action.HIDE_COMPONENT`, `Action.GENERATE_PLUGIN`, `Action.NEEDS_REASONING`, `Action.OPEN_PROJECT`, `Action.LOCATE_PROJECT` are **never registered** in the skill registry — any plan step with those actions raises `ValueError: No skill registered for action`. |

### E. requirements.txt Is Corrupted

| # | File | Problem |
|---|---|---|
| 31 | `requirements.txt` | File has UTF-16 BOM encoding with space-separated characters (e.g., `c u s t o m t k i n t e r`). Only 3 packages are listed (`customtkinter`, `darkdetect`, `packaging`), all in corrupted form. **All actual runtime dependencies are absent**: `openwakeword`, `faster-whisper`, `google-generativeai`, `edge-tts`, `python-vlc`, `sounddevice`, `soundfile`, `numpy`, `pystray`, `Pillow`, `python-dotenv`, `google-genai`. |

---

## 4. The Minimal Canonical Spine

### Keep — One True Runtime Path

| Package | Purpose |
|---|---|
| `main.py` | Entry point |
| `rov_background.pyw` | Production launcher |
| `config.py` | Configuration |
| `tray_icon_helper.py` | Tray icon helper |
| `voice/` | All 4 files: `detector.py`, `recorder.py`, `wisper_engine.py`, `speaker.py` |
| `brain_v2/` | All except `json_parser.py`, `execution_plan.py`, `prompt_builder.py` |
| `router/` | Both files |
| `skills/` | `base.py`, `application/`, `browser/`, `plugin/`, `knowledge/` |
| `plugins/` | `plugin.py`, `runtime.py`, `proposals.py`, `gemini_generator.py` |
| `ai/rag.py` | Knowledge base RAG |
| `core/audio.py` | Single live bridge file — creates `speaker` singleton |
| `core_v2/` | All 5 files |

### Quarantine / Delete

| Directory / File | Reason |
|---|---|
| `brain/` (entire) | v1 brain — fully superseded; introduces duplicate `Intent`, `Action`, `EntityType` enums |
| `core/` — all files **except `core/audio.py`** | v1 service layer — broken imports, phantom modules, `pyautogui` dependency |
| `plugins/plugin_loader.py` | Dead loader with broken `from plugin import Plugin` |
| `plugins/plugin_registry.py` | Dead registry with same broken import |
| `brain_v2/json_parser.py` | Dead, duplicate definitions, stray mid-file import |
| `brain_v2/execution_plan.py` | Orphaned dataclass never used |
| `brain_v2/prompt_builder.py` | References phantom `brain.intents.INTENTS` |
| `ui.py` | Dead CTk UI importing broken `core.dispatcher` |
| `uib/` (entire) | Unconnected alternative UI |
| `studio/` (entire) | PySide6 developer dashboard, not wired into runtime |
| `skills/developer/` | References three non-existent `Action` enum members; not registered in router |
| `skills/file/` | Unregistered skill |
| `ai/chat.py`, `ai/init.py`, `ai/testai.py` | `chat.py` only used by dead `core.dispatcher`; others are stubs |
| `time.py` | Root-level file that shadows stdlib `time` module and imports phantom functions |

---

## 5. Consolidation Plan

Steps marked **(I)** are independent and can be done in parallel.  
Steps marked **(D: N)** depend on step N being complete first.

| # | Step | Dependencies | Notes |
|---|---|---|---|
| 1 | **Rebuild `requirements.txt`** — delete the corrupted UTF-16 file; write a clean UTF-8 version listing: `openwakeword`, `faster-whisper`, `google-generativeai`, `google-genai`, `edge-tts`, `python-vlc`, `sounddevice`, `soundfile`, `numpy`, `pystray`, `Pillow`, `python-dotenv`, `customtkinter` | **(I)** | Completely self-contained |
| 2 | **Rename `voice/wisper_engine.py` → `voice/whisper_engine.py`** and fix `main.py:6` import from `wisper_engine` to `whisper_engine` | **(I)** | Typo fix only |
| 3 | **Fix the Gemini model name** in `brain_v2/gemini_provider.py:30` — change `"gemini-3.5-flash"` to `"gemini-2.0-flash"` (or `"gemini-1.5-flash"`). Apply same fix in `ai/rag.py` if it uses the same bad name | **(I)** | One-line fix each |
| 4 | **Create `plugins/installed/` and `plugins/staged/` directories** (with `.gitkeep`) so `PluginRuntime` and `PluginProposalService` do not fail on first run | **(I)** | File-system only |
| 5 | **Fix the canonical Planner** (`brain_v2/planner.py`) — replace all six branches that put raw `Action` enum values or raw strings into `plan.steps` with proper `Step(action=..., parameters={...})` dataclass instances | **(I)** | Fixes issues #25–29 |
| 6 | **Deduplicate `voice/detector.py`** — remove the copy-pasted `now` / `triggered` block (lines 58–66) | **(I)** | Issue #23 |
| 7 | **Deduplicate `core_v2/browser.py`** — remove second `search_google` definition (line 73–74) and duplicate `from urllib.parse import quote_plus` import (line 50) | **(I)** | Issue #22 |
| 8 | **Register missing canonical actions in the Router registry** (`router/registry.py`) — decide which skill handles `NEEDS_REASONING`, `SHOW_COMPONENT`, `HIDE_COMPONENT`, `OPEN_WEBSITE`, `GENERATE_PLUGIN`, `OPEN_PROJECT`, `LOCATE_PROJECT` — or remove them from the planner/entities enum if not yet implemented | **(D: 5)** | Planner must be fixed first |
| 9 | **Quarantine / delete dead code** — move `brain/`, dead `core/` files (all except `core/audio.py`), `ui.py`, `uib/`, `studio/`, `plugins/plugin_loader.py`, `plugins/plugin_registry.py`, `brain_v2/json_parser.py`, `brain_v2/execution_plan.py`, `brain_v2/prompt_builder.py`, `skills/developer/`, `skills/file/`, `ai/chat.py`, `time.py` into a `_quarantine/` folder | **(I)** | Reduces confusion from stale `.pyc` and duplicate enums |
| 10 | **Install dependencies and verify import chain** — run `pip install -r requirements.txt` then `python -c "from main import ROV"` to confirm no `ImportError` | **(D: 1, 2, 3, 4)** | All package fixes must be done first |
| 11 | **End-to-end smoke test** — run `python main.py`, confirm tray icon appears and a text command entered through the dialog passes through Brain → Router → ApplicationSkill without exception | **(D: 5, 6, 7, 8, 10)** | Full integration gate |

---

## Summary of Critical Blockers

Before any code runs, these must be resolved:

1. **`requirements.txt` is unreadable** — UTF-16 garbage; no dependencies can be installed.
2. **Typo `wisper_engine`** — `main.py` cannot import `transcribe`.
3. **`"gemini-3.5-flash"` is not a real model name** — fails at runtime on any Gemini API call.
4. **Six planner branches push raw enum values / strings into `plan.steps`** — Router crashes with `AttributeError: 'Action' object has no attribute 'action'` for WEBSITE, SHOW, HIDE, PROJECT, and GENERATE intents.
5. **Seven `Action` values emittable by the planner have no registered skill** — Router raises `ValueError`.
6. **Three phantom `Action` members** referenced by `DeveloperSkill` (`ANALYZE_PROJECT`, `REVIEW_CODE`, `CREATE_PROJECT`) do not exist in the enum.
7. **All external packages missing from requirements** — a clean-install environment fails on every import.

---

*See `docs/rov_architecture.md` for the Mermaid architecture diagram.*
