# Publication and data boundary

**This is not a private repository template.** Everything in the public Git history, Actions logs/artifacts, issues, generated website (including search JSON, hidden files and assets) is potentially accessible. No unapproved Level 1 content; no Level 2/DAIHEN material. Later migration cannot undo prior disclosure. Do not copy the private handoff notes into this repository.

## Before any content commit (including drafts)

Confirm public disclosure authorization and external translation authorization, or keep the material entirely outside this repository. Remove internal addresses, private repository links, usernames, personal data, secrets, unpublished results, restricted images (including metadata) and sponsor materials. Do not commit restricted data then try to hide it with a label or `.gitignore`. Only approved maintainers can write; use a reviewed PR process for wider collaboration. The current direct-commit prototype is not a review enforcement system. Human review of content and all safety-critical translations is required before operational use; do not publish such material automatically until an appropriate review gate is implemented.

## Build-time checks

`scripts/common.py` rejects unknown content locations, unexpected file types and symlinks in publishable content/assets/vendor/web; it is called by both the builder and translator. This reduces accidental file inclusion, not semantic leaks. The public-only boundary also applies to README, AGENTS, commits, issues and any files that are not built. Do not rely on these checks for confidentiality.

## Credentials and external services

Use a short-lived, repository-scoped fine-grained GitHub PAT only on a trusted HTTPS deployment. Never commit keys. LLM API credentials live in repository Actions Secrets. Do not give an external model access to unapproved content. Review pinned editor dependency and workflow permissions before using a real token. The browser editor currently targets GitHub API directly; token and page data can be exposed if site JavaScript is compromised. Do not confuse local coding-agent execution with local-only inference.

## Transfer checklist

1. Obtain lab authorization and identify actual Git service, web host, owner and CI runner. Reserve the public repository as public-safe; migrate by approved transfer or clone.
2. Revoke personal tokens, rotate secrets, configure new ownership and backups. For internal-only content, use a separate restricted Git remote and authenticated static hosting (HTTPS, VPN/SSO or equivalent approved mechanism).
3. Adapt browser Git adapter, issue/history links, CSP, CI wrapper and translation provider. Keep Markdown page IDs and static build. Use local or approved translation only. Test access without credentials and with a revoked account, including search indexes, assets and editor/API endpoints.
4. Verify access to Git history, logs, backups and artifacts as well as site. Only then add approved internal-only content. Do not mirror internal content to the old public remote.
