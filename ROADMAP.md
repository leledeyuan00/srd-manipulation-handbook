# Development roadmap — v0.2

## Current baseline

v0.1 static builder, browser editor, page-level translation and GitHub workflow retained. Sponsor handover removed entirely from the content tree and navigation; new chapters added for lessons learned and maintenance. Initial pages are outlines, not verified SOPs. No live deployment/API acceptance yet.

## Milestones (in order)

- [ ] Local browser test: layout, navigation, mobile, search, code copy and WYSIWYG round-trip including tables, code and warnings. Review pinned editor dependency before providing PAT.
- [ ] Create authorized personal public-safe GitHub repo; deploy synthetic sample. Test scoped expiring PAT, conflict detection, new page and credential handling.
- [ ] Configure approved model API and test Chinese/English/Japanese source updates, translation correction, new page and simultaneous edits with synthetic content. Confirm build/deploy and no recursive runs. Review technical accuracy before adopting.
- [ ] Improve editor: safe image upload, page navigation management, stable anchors, math and diagrams. Consider PR review and segment-level translation memory; require explicit acceptance criteria and tests.
- [ ] Write approved public-safe content: training SOP first, DENSO/general control principles, dataset, collection, deployment, reference materials. Independently complete restricted handover; no cross-copy.
- [ ] Transfer to lab: identify Git platform, implement adapter, CI and authorization, run migration checklist in SECURITY.md.

## Acceptance gate

Unit tests + static build + link checks + JS syntax must pass locally. Live PAT, browser, model and GitHub Actions tests must be recorded separately; do not mark passed based on mocked tests. Preserve the last successful release and never force-push translation changes.
