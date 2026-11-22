# Development roadmap — v0.2

## Current baseline

v0.1 static builder, browser editor, page-level translation and GitHub workflow retained. Sponsor handover removed entirely from the content tree and navigation; new chapters added for lessons learned and maintenance. Initial pages are outlines, not verified SOPs. No live deployment/API acceptance yet.

### Local baseline review - 2026-11-22

- Working tree reviewed on `main`; no tracked changes were present before this review.
- `python -m unittest discover -s tests -v`: 13 tests passed and 1 symlink test was skipped because the current Windows account cannot create symlinks. This run used Python 3.10.7 with the pinned Python packages, not the CI target Python 3.12.
- `python scripts/build.py`: passed and generated 39 handbook pages (13 page IDs in three languages).
- `python scripts/translate.py --plan`: passed; all page decisions were `None`, so no model or network call was made.
- Ad hoc generated-site link check: checked 41 HTML files and found 0 missing internal files or anchors. This check is not yet part of the repository tests or CI.
- `node --check web/editor.js` and `node --check web/read.js`: not run because Node.js is unavailable in the current environment.
- Real browser editing, GitHub write, GitHub Actions, deployment and model API acceptance tests were not run.
- Partial live editor acceptance: a repository-scoped fine-grained PAT successfully authenticated and loaded an existing Markdown source file from GitHub. Editing, commit creation, conflict handling, Actions, deployment and credential cleanup are not yet verified.
- Local no-LLM workflow check: with all 13 page hashes matching `translation-state.json` and all three LLM variables unset, `python scripts/translate.py` completed with `0 translation file(s) updated`. The local implementation therefore does not require an LLM key when no page needs synchronization; a remote first-run failure must be diagnosed from the Actions step log and repository baseline.
- GitHub Pages deployment diagnostic: the build job uploaded the `github-pages` artifact successfully, but `actions/deploy-pages@v4` failed with HTTP 404 `Ensure GitHub Pages has been enabled`. This is a repository Pages configuration issue, not an LLM/API or `scripts/build.py` failure.
- Live editor write diagnostic: loading from the organization-owned repository succeeded, but committing returned `Resource not accessible by personal access token`. The PAT read path is verified; write access to the organization-owned repository is not. The next test will use an authorized personal-account repository, with no architecture change.
- User-reported live editor acceptance: after moving to the personal-account repository, a rich-text edit was committed successfully and the published site updated. This verifies the normal editor write and publish path once; conflict handling, token cleanup, new-page creation and automatic translation remain unverified.
- Responses API adapter stage: added mock-tested OpenAI-compatible Responses support with `LLM_WIRE_API=responses`, full `/responses` endpoint configuration, `store: false`, and workflow variable passthrough. Local tests and build passed; no real company endpoint was called. Live API schema and translation-quality acceptance remain unverified.
- HTTP 400 diagnostics stage: translation requests now preserve the status code and a truncated, credential-redacted server response body in the local error. The current local run passed 16 Python tests with 1 symlink test skipped, passed the 39-page static build and Python syntax compilation; the real gateway error body is still required to identify the company endpoint incompatibility.
- Bounded 429 retry stage: added a default maximum of 2 retries, support for numeric and HTTP-date `Retry-After`, short fallback backoff when the header is absent, and mock coverage for honoring and stopping retries. The real gateway remains responsible for deciding when capacity is available.

### Open implementation risks

- The acceptance gate is not automated end to end. CI runs Python tests and the build, but does not run JavaScript syntax checks or an internal-link checker.
- `scripts/fetch_editor.py` accepts an existing or downloaded TOAST UI bundle without a reviewed checksum. These scripts can execute on the same page as a repository PAT, so dependency integrity must be resolved before credential testing.
- The browser editor checks only that Markdown starts with an H1 before committing directly to the default branch. It does not enforce the complete parser/build contract, so CI can reject content only after the source commit exists.
- Translation planning, page validation and model calls are interleaved. A later page conflict or validation error can fail a run after earlier pages have already been sent to the approved model service.
- Current tests do not cover generated HTML, navigation/search behavior, WYSIWYG round-trip behavior, workflow behavior, or credential non-persistence in a browser.

## Milestones (in order)

- [ ] Local browser test: layout, navigation, mobile, search, code copy and WYSIWYG round-trip including tables, code and warnings. Review pinned editor dependency before providing PAT.
- [ ] Create authorized personal public-safe GitHub repo; deploy synthetic sample. Test scoped expiring PAT, conflict detection, new page and credential handling.
- [ ] Configure approved model API and test Chinese/English/Japanese source updates, translation correction, new page and simultaneous edits with synthetic content. Confirm build/deploy and no recursive runs. Review technical accuracy before adopting.
- [ ] Improve editor: safe image upload, page navigation management, stable anchors, math and diagrams. Consider PR review and segment-level translation memory; require explicit acceptance criteria and tests.
- [ ] Write approved public-safe content: training SOP first, DENSO/general control principles, dataset, collection, deployment, reference materials. Independently complete restricted handover; no cross-copy.
- [ ] Transfer to lab: identify Git platform, implement adapter, CI and authorization, run migration checklist in SECURITY.md.

## Next development stage

Complete the local acceptance foundation before creating a public repository or entering a PAT.

1. Add repeatable generated-site tests for page counts, language navigation, internal files/anchors, search indexes and non-public input exclusion. Run them in CI.
2. Add JavaScript syntax checks to CI and document a supported local Node.js version. Keep browser acceptance separate from syntax checks.
3. Add editor-side structural validation for the existing content contract, while keeping `scripts/common.py` and the static build authoritative. Add tests for invalid page IDs, missing or duplicate H1, conflicts and new-page modes.
4. Split translation synchronization into a complete preflight plan/validation pass followed by model calls and atomic writes. Extend mocked tests for late conflicts, invalid output and no-write behavior.
5. Review TOAST UI Editor 3.2.2 and choose an approved integrity strategy: commit reviewed assets with recorded hashes, or replace it with an organization-approved package. Do not test a real PAT before this gate passes.
6. Run the first milestone's browser matrix with synthetic content: desktop/mobile layout, three-language navigation, search, code copy, Markdown/WYSIWYG round trips for tables, code fences and warnings, fallback editor behavior, and token non-persistence. Record browser versions and results here.

Exit criteria: Python 3.12 tests, static build, automated link checks and JavaScript syntax checks pass in a clean environment; the reviewed editor bundle is reproducible; browser results and remaining limitations are recorded. This completes only the first milestone, not live GitHub, deployment or model acceptance.

## Acceptance gate

Unit tests + static build + link checks + JS syntax must pass locally. Live PAT, browser, model and GitHub Actions tests must be recorded separately; do not mark passed based on mocked tests. Preserve the last successful release and never force-push translation changes.
