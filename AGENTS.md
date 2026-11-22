# AGENTS.md — SRD Manipulation Handbook

## Mission and boundaries
- Maintain a trilingual public-safe living handbook for new M1/D1 students at SRD, Tohoku University. Readers know basic Linux/Python but may be new to ROS 2, manipulators and LeRobot.
- Explain why and how; connect the lab system to public CMB documentation instead of copying library tutorials.
- This repository is PUBLIC-SAFE ONLY until an authorized internal migration is completed. Level 0 and explicitly approved Level 1 only. Never import DAIHEN project files, internal-only information, raw logs, private links, credentials or unpublished results. Public disclosure and external model processing require permission. Read SECURITY.md before any content, assets, publication or translation change. Do not read the separate handover repository in this workspace.
- Do not push, deploy, change remotes, send content to an external API, or change security settings without user authorization. Local builds and mocked tests are preferred. This file is guidance, not an access control mechanism.

## Collaboration
- Discuss plans and questions in Chinese; handbook content may originate in English, Japanese or Simplified Chinese (English default when convenient). Use short sentences, precise terms and no idioms. Prefer complete files or sections. Batch unresolved questions; explain logical and wording changes separately when relevant.
- Before edits inspect README.md, ROADMAP.md, SECURITY.md, relevant source files and existing changes. Preserve user work. Keep changes scoped, avoid unnecessary dependencies and unrelated rewrites. Report changed paths, tests actually run and unresolved risks. Update ROADMAP.md when milestones change.

## Content contract
- Standard Markdown (CommonMark plus tables and strikethrough), not RST/MyST. One H1 at the start, then a short learning objective; one topic per page (split long pages with approval). Keep stable page IDs and relative links such as `../dataset/`. Shared approved images use `assets/...`.
- Exact tested command, purpose, expected output; if an actual value/version/flag/path is unknown, use a visible TODO blockquote rather than guess. Ask for permitted, redacted evidence. Preserve exact authorized vendor error strings and give an explanation. Use failure and phase as research terms. Troubleshooting: symptom/error → evidence → verified cause → verified fix → validation.
- Safety warnings at the relevant step; never suggest bypassing safety circuits. No unverified procedures as runnable SOPs. Authorized humans must review hardware operations and all safety-critical translations.
- Preserve the six sections of `02_imitation_learning/training`; see its nested AGENTS.md. Do not invent facts from older handoff notes; validate against approved sources.

## Code architecture and translation contract
- `content/<page-id>/{en,ja,zh}.md`, `web/` UI, `scripts/common.py` parser/chapter registry, `scripts/build.py` static build, `scripts/translate.py` sync, `translation-state.json` baseline, `.github/workflows/docs.yml` orchestration. Update registry and editor validation together for new chapters.
- Preserve any-language source updates, translation-fix markers, conflict refusal, and structural validation. Do not manually rewrite state to conceal a failed sync. For a new baseline or deletion, require explicit reviewed migration. Keep model output as data; do not execute it. No external calls during tests.
- Token stays in current browser session memory, never logs/local storage/source. Avoid third-party runtime scripts; use audited local assets. Keep GitHub-specific UI/API separate from build and translation. Future internal Git adapter is not implemented yet.
- `site/` is generated, never edit or commit it; all contents and search indexes are publicly accessible. Public scope checks are structural only, not a classifier for secrets. No security-significant changes without explicit review.

## Validation / definition of done
- From repository root: `python -m pip install -r requirements.txt` (approved environment); `python -m unittest discover -s tests -v`; `python scripts/build.py`; `node --check web/editor.js`; `node --check web/read.js`.
- After committing a source edit, `python scripts/translate.py --plan` inspects Git history without network calls. Do not run actual translation without authorization. Use mocked translation tests for normal updates, fixes, conflicts and invalid output.
- Verify language navigation, internal links and search; distinguish static tests from real browser or live GitHub/API acceptance. Do not claim deployment or translation is verified unless actually tested.
