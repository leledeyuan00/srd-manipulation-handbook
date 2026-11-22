# SRD Manipulation Handbook — starter v0.2

三语机器人知识库原型 / Trilingual static handbook prototype. This is a new starter based on the supplied handoff outline, not a migration of the previous Sphinx repository. All handbook pages are drafts.

## 1. 本地运行

需要 Python 3.12（CI 使用该版本）。在仓库根目录执行：

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/fetch_editor.py
python scripts/build.py
python -m http.server 8000 --directory site
```

浏览器打开 http://localhost:8000/ 。如仅查看阅读页，可跳过 `fetch_editor.py`；未安装编辑器时只能使用 Markdown 源码编辑。富文本 JS/CSS 在构建时下载，运行时从站点本身加载。编辑器依赖固定为 TOAST UI Editor 3.2.2；该版本较旧，正式上线前应审核依赖和漏洞，最好将经过检查的 bundle 固定哈希、提交到仓库（`git add -f vendor/*.js vendor/*.css`），或改用组织审核过的包。

## 2. GitHub 初始化与首次发布

1. 在获得实验室授权后创建 `srd-manipulation-handbook` 仓库（暂用个人账号，后续迁移至实验室）。不要直接覆盖原 Sphinx 仓库；先保留备份。整个仓库仅限获准公开且获准由所选翻译服务处理的内容；Level 1 未获准公开的内容也不能上传。企业交接完全独立。私人 repo 不等于私人 Pages 网站。
2. 从本项目根目录执行（将 URL 替换为你新建的 repo）：

```bash
git init -b main
git add .
git commit -m "Initial trilingual handbook starter"
git remote add origin https://github.com/YOUR_ACCOUNT/srd-manipulation-handbook.git
git push -u origin main
```

3. GitHub → Settings → Pages → Build and deployment → Source：GitHub Actions。若首次 push 因 Pages 未启用导致失败，完成设置后在 Actions 手动运行 Translate and publish handbook。
4. Settings → Actions → General 检查允许 Actions 运行、默认分支允许 workflow token 回写 `content/` 与 `translation-state.json`。不要为整个组织关闭 branch protection；如果分支策略不允许 bot 直推，应升级为 PR 模式。
5. 配置以下 Actions Variables 和 Secret，然后在 Actions 手动运行工作流：

| 类型 | 名称 | 值 |
| --- | --- | --- |
| Variable | `LLM_API_URL` | 经组织允许的 OpenAI-compatible HTTPS chat-completions 完整端点（例如 `https://api.openai.com/v1/chat/completions`） |
| Variable | `LLM_MODEL` | 该服务已开通的模型 ID |
| Variable | `LLM_WIRE_API` | `chat_completions`（默认）或 `responses`；公司 Responses API 使用 `responses` |
| Variable | `LLM_MAX_RETRIES` | 429 限流时的额外重试次数，默认 `2`；不重试其他 HTTP 错误 |
| Secret | `LLM_API_KEY` | 该服务的 API key |

初始 39 个页面已经有三语大纲且同步状态已初始化，第一次未改动文档时无需 API key，模型不会被调用。首次真正修改内容前配置 API。API 按服务计费；ChatGPT 订阅不包含通用 API 调用额度。模型和 API 都可以替换。

## 3. 在线编辑

- 阅读页右上角 Edit page。编辑器加载 GitHub 的最新文件，而不是从已发布旧页面直接保存。
- 使用仅针对该仓库、具有 Contents: Read and write 权限的 fine-grained personal access token；个人 token 不应共享。选择过期时间，离开实验室后撤销。不使用 Actions 的 `GITHUB_TOKEN` 或 LLM key 登录编辑器。
- token 只保存在当前页面内存和输入框，不写 localStorage/sessionStorage 或仓库。点击 Disconnect 清除；关闭页面后需重新输入。使用可信 HTTPS 站点。任何运行在该站点的 JS 都可能接触 token，生产环境建议改为 GitHub App + OAuth/PR，而不是长期依赖 PAT。
- 点击 Load from GitHub → 修改内容（WYSIWYG / Markdown）→ 输入 commit message → Commit to GitHub。文件 SHA 不一致将拒绝覆盖。网页不会立即变更，需等待 Actions 成功；查看 Actions 页面。
- New page：选择 Create page / missing language，输入例如 `02_imitation_learning/evaluation`，填写一种语言（第一行为 H1 标题），提交。自动生成其余两种语言，构建时自动加入导航。
- 图片：第一版先通过 GitHub 上传到 `assets/`，再在编辑器中插入 URL 如 `assets/setup.png`。不支持从网页直接上传二进制文件。可在 Markdown 模式检查路径。图片内容及图片内文字不自动翻译，截图中的机密信息必须去除。
- Translation correction only：只修改译文时勾选，会在 commit message 前添加 `[translation-fix]`。也支持 `【翻译错误】`、`【翻译修正】` 和 `[skip-translation]`。只记录此次版本，不反向翻译；该 commit 仍然会触发构建和发布。
- 使用 Issues 报告翻译错误：注明页面链接、语言、原句、建议修改。第一版由维护者审核修改，不会自动执行 Issue 内容。

## 4. 内容与文件结构

```text
content/
  home/{en,ja,zh}.md
  00_infrastructure/index/{en,ja,zh}.md
  01_realtime_control/index/{en,ja,zh}.md
  02_imitation_learning/
    index/{en,ja,zh}.md
    data_collection/{en,ja,zh}.md
    dataset/{en,ja,zh}.md
    training/{en,ja,zh}.md
    deployment/{en,ja,zh}.md
  03_denso_system/index/{en,ja,zh}.md
  04_lessons_learned/index/{en,ja,zh}.md
  05_handbook_maintenance/index/{en,ja,zh}.md
  appendix/{glossary,reading_list}/{en,ja,zh}.md
assets/                   # approved shared images
scripts/common.py         # parser, page schemas, structural signature
scripts/build.py          # static HTML, navigation, search index
scripts/translate.py      # change detection and translation
scripts/fetch_editor.py   # local editor assets
web/                      # frontend templates, CSS and browser scripts
translation-state.json    # baseline hashes; auto-managed
.github/workflows/docs.yml
```

Each page starts with one H1. Use ordinary CommonMark/GFM-style Markdown, fenced code, tables, links and bold blockquotes for warnings. Raw HTML is escaped by the static renderer. For sibling pages use `../dataset/` etc. Paths remain the same in all languages. The navigation order for the IL pipeline is fixed. New chapters require adding names to `scripts/common.py` and chapter IDs in `web/editor.js`; new pages within these chapters are discovered automatically. Section anchors are positional and may change with heading additions, so use page-level links for stable URLs until stable anchors are implemented.

The previous MyST content must be migrated separately: `{doc}`, `{term}`, `:::{warning}`, `todo`, `list-table`, intersphinx, and Mermaid need conversion. Do not paste MyST source unchanged into this prototype. The CMB handbook link is retained rather than duplicating CMB tutorials.

## 5. Translation workflow and failure behavior

`python scripts/translate.py --plan` shows the intended action (run against a Git repository with committed changes). For an OpenAI-compatible Responses endpoint, set `LLM_API_URL` to the full `/responses` URL and set `LLM_WIRE_API=responses`; the workflow passes this variable to the translator. `python scripts/translate.py` performs synchronization. `translation-state.json` stores SHA-256 hashes for the last synchronized content. A single changed language becomes the source; only its page is sent to the model. In a normal update the program requests the other two translations, passing the existing target as context, and validates Markdown heading/list/table structure, fenced code, inline code, and link/image destinations. All requested translations must pass before any translation file is written; a failure aborts the workflow rather than publishing inconsistent output. The source commit stays in git, and the published version stays at the last successful deploy.

When two or more languages of a page have unsynchronized changes, the program refuses automatic merging. Review all three texts and explicitly reconcile them. If they already agree, use a reviewed manual reconciliation commit touching the conflicting files with `[translation-fix]` (all three language files must exist; a harmless newline-only change can record the reviewed file if needed). Manual-only commits update the state without calling the model. The program reads the most recent Git commit message for each changed language. Whole-page deletion/rename and partial language deletion are deliberately blocked pending explicit state migration. Do not edit the state simply to hide a failed sync.

One workflow translates, validates, builds, commits generated files, and deploys the generated artifact. GitHub's `GITHUB_TOKEN` does not normally trigger a new push workflow. Concurrency group prevents overlapping workflow runs; a push race is rejected rather than force-pushed. A later run retries from the current branch head. The prototype assumes a trusted maintainer group with direct write permission; public contributions and protected branches should use reviewed PRs before automated translation and publish.

**Limitations:** Translation is page-level, not paragraph-level; future source edits may change prior manual word choices. Model instructions do not guarantee correct safety semantics, error strings or quantities. A full page and existing translation are sent to the external API provider. No sponsor-confidential material, personal data, passwords, API tokens, device addresses or unpublished results should be submitted to an unauthorized provider. Validate translated technical content with qualified lab members before treating it as authoritative. The current renderer is lightweight and does not reproduce all Sphinx features (mathematics, automatic glossary links, interactive diagrams, etc.).

## 6. Tests

```bash
python -m unittest discover -s tests -v
python scripts/translate.py --plan
python scripts/build.py
node --check web/editor.js
node --check web/read.js
```

CI first runs tests; fake-model tests check the synchronization logic without invoking a live service. For acceptance testing on a sandbox repo: (1) edit Chinese text and verify exactly the corresponding English/Japanese files update; (2) make a Japanese-only translation correction, verify other hashes unchanged; (3) create a page from English only; (4) simulate concurrent edits and verify refusal; (5) confirm token is not present in generated pages, local storage, or commits. Browser/editor, live GitHub writes and live model calls require network access and user-owned credentials, and have not been validated in this environment.

## 7. Next steps

- Replace demo outline content with approved lab SOPs, starting with policy training and DENSO troubleshooting.
- Add rich-text image uploads, localized editor UI, safe callout styles, stable anchors, math/diagrams and block-level translation memory.
- Add PR-based review (especially safety-critical pages), translation freshness/status badges and page-level revision notes.
- Keep all DAIHEN project materials in the separate, authorized handover repository; never import them here.
- See `ROADMAP.md` for current milestones and `SECURITY.md` for publication and migration rules.
