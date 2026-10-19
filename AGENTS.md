# Arabic Game Localization Playbook — agent entry point

This folder is a knowledge base, not a game project. Do not build or modify games here.

If you were asked to localize a game into Arabic:

1. Read `00_START_HERE_FOR_AI.md` fully (Arabic). It is the operating contract.
2. Read the project's `LOCALIZER_PROFILE.md` (template: `01_LOCALIZER_PROFILE.md`). The localizer's choices override this playbook's defaults, except the safety rules in `00` §3.
3. Identify the engine with `engines/README.md`, then read that engine file and `02_WORKFLOW.md`.
4. Reuse `code/` tools (tested Python) and `templates/` for the project's AGENTS/STYLE/glossary/PROGRESS/SKILLS/handoff files.

Scope: legally owned copies only; release difference patches, never game files (see `DISCLAIMER.md`).

Non-negotiables: the original game and the player's saves are read-only; translations are logical UTF-8 Arabic; wrap logical text first and then shape and reverse each line at build time; keep every control code and number; never claim "fixed" or "approved" without an in-game screenshot bound to the build's hashes; report to the user in Arabic.

If you change files in this playbook, keep it consistent: update `README.md`'s table and any cross references, and run `python -X utf8 code/selftest.py` after editing any code in `code/`.
