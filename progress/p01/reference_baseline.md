# P01-S01-01 参考项目基线报告

- 建立时间：2026-09-29
- 参考目录：`references/p01-backblaze-ai-saas-starter-kit/`
- 状态标签约定：**已验证** = 有仓库文件或命令输出直接证明；**未验证** = 有证据来源但本需求内未能执行确认；**阻塞** = 缺少条件且需要外部动作；**待用户决定** = 需要用户提供输入或授权。

## 1. 来源与版本

| 项目 | 值 | 状态 | 证据 |
|---|---|---|---|
| 仓库 URL | `https://github.com/backblaze-labs/ai-saas-starter-kit` | 已验证 | 路线文档约定 + `git config --get remote.origin.url` |
| 远程地址 | 同上（`origin`） | 已验证 | 克隆后经 `git remote set-url` 重置为上游 URL |
| 默认分支 | `main` | 已验证 | `git symbolic-ref refs/remotes/origin/HEAD` → `refs/remotes/origin/main`；GitHub API 元数据一致 |
| 完整 commit SHA | `1b9c094c8e171aed165a4eb8b519cd727549e60f` | 已验证 | 参考仓库 `git rev-parse HEAD`；与 GitHub API `branches/main` 返回的 SHA 逐一字符一致 |
| 获取方式 | 经 `gh-proxy.com` 镜像执行 `git clone`（GitHub 主站直连超时），随后将 `origin` 重置为上游 URL | 已验证 | 镜像 `ls-remote` SHA 与 GitHub API 官方 SHA 相同；Git 内容寻址保证检出内容与该 SHA 一致 |
| 上游最近推送 | 2026-09-22 | 已验证 | GitHub API 仓库元数据 `pushed_at` |

说明：本机网络对 `github.com`、`codeload.github.com`、`raw.githubusercontent.com` 连接后传输停滞，`api.github.com` 与 `gh-proxy.com` 正常。因此克隆走镜像，但版本锚点（SHA）已经由官方 API 交叉验证，后续 Agent 可用第 1 表的 URL + SHA 定位完全相同的上游版本（如在网络正常环境，直接 `git clone` 上游 URL 后 `git checkout 1b9c094c8e171aed165a4eb8b519cd727549e60f`）。

## 2. License

| 项目 | 值 | 状态 | 证据 |
|---|---|---|---|
| License | MIT License（Copyright (c) 2026 Backblaze, Inc.） | 已验证 | `references/p01-backblaze-ai-saas-starter-kit/LICENSE`（全文）；`README.md` 徽章与文末 License 段一致；GitHub API `license.spdx_id = MIT` 一致 |

## 3. 目录和主要模块

证据：根目录列表、`AGENTS.md` §1、`README.md`、`pnpm-workspace.yaml`。状态：已验证。

```text
apps/web/          Next.js 前端（App Router）
services/api/      FastAPI 后端（分层 types → config → repo → service → runtime）
packages/shared/   共享 TypeScript 类型
supabase/          Supabase 本地栈配置与数据库迁移
infra/railway/     Railway 部署说明（仅文档）
scripts/           开发与预检脚本（dev.sh、doctor.mjs、pick-port.mjs、sync-*.mjs、configure_b2_cors.py）
docs/              项目级说明（features/、deployment.md、SECURITY.md、RELIABILITY.md 等）
.github/workflows/ CI（ci.yml）
```

- 包管理：pnpm workspaces（证据：`package.json`、`pnpm-lock.yaml`、`pnpm-workspace.yaml`，workspace 含 `apps/*` 与 `packages/*`）。
- 前端：`apps/web`，Next.js 16.2.11 + React 19.2.3 + TypeScript ^5 + Tailwind v4（证据：`apps/web/package.json`）。
- 后端：`services/api`，FastAPI 0.139.2 + Pydantic v2 + boto3，依赖在 `services/api/requirements.txt` 全部精确钉版（证据：该文件头部注释与内容）。
- 数据库：Supabase Postgres 17（本地栈，`supabase/config.toml` `[db] major_version = 17`）；迁移为单文件 `supabase/migrations/00000000000000_init.sql`（含 auth/billing/generation/admin 共 10 张表）。
- 运行时版本锁定文件（`.nvmrc`、`.python-version`、`runtime.txt` 等）：**不存在**。版本约束来源只有 `README.md` Quick Start 与 `package.json` `engines`、`services/api/pyproject.toml` 的 `target-version = "py311"`。
- 容器配置（Dockerfile / docker-compose）：**不存在**。容器使用完全由 Supabase CLI 的 `supabase start` 自管（证据：根目录与子目录无相关文件；`README.md` 只要求 Docker + Supabase CLI）。

## 4. 启动组件与命令

证据：`package.json` scripts、`scripts/dev.sh`、`scripts/doctor.mjs`、`README.md` Quick Start。状态：已验证（命令本身未全部执行，见第 7、8 节）。

启动链路：

1. `pnpm dev` → 先跑 `predev`（`node scripts/doctor.mjs` 预检：Node/pnpm/Python 版本、`.env`、venv、端口）。
2. `scripts/dev.sh` 用 `pick-port.mjs` 选定 API 端口（默认 8000），设置 `NEXT_PUBLIC_API_URL` 与开发用 CORS 正则，再用 `concurrently` 并行启动：
   - `pnpm dev:web`：Next.js 前端，默认 `localhost:3000`。
   - `pnpm dev:api`：`services/api/.venv/bin/uvicorn main:app --reload`，默认 `localhost:8000`。
3. 前置一次性准备（README）：
   - `pnpm install`（安装 JS 依赖）。
   - `cd services/api && python3 -m venv .venv && pip install -r requirements.txt`。
   - `cp .env.example .env` 并填入 B2 与 Supabase 变量。
   - `supabase start`（Docker 拉起本地 Postgres + Auth + Studio + Mailpit，自动套用迁移），然后 `node scripts/sync-supabase-env.mjs` 把 3 个 Supabase 变量写入 `.env`。
4. 可选：`pnpm stripe:seed` + `pnpm stripe:listen`（Stripe 测试）；配置 NVIDIA key 后 `/generate` 可用。

组件关系：浏览器 → Next.js(:3000) → FastAPI(:8000) → Supabase（认证 + Postgres）；上传由浏览器经预签名 PUT 直传 B2；Stripe webhook 经 Stripe CLI 转发到 API `/billing/webhook`；AI 生成由 API 调 NVIDIA NIM，结果写 B2。

本地 Supabase 端口（证据：`supabase/config.toml`）：API/Kong 54321、DB 54322、Studio 54323、Mailpit（本地 SMTP 捕获）54324。

## 5. 环境变量分类

证据：`.env.example`（变量声明）与 `services/api/app/config/settings.py`（实际消费，pydantic-settings）。状态：已验证（仅元数据级盘点；本需求未读取、未记录任何真实值）。

### 5.1 启动必需

| 变量 | 用途 | 敏感性 | 外部账户 / 费用风险 |
|---|---|---|---|
| `B2_APPLICATION_KEY_ID` | B2 应用密钥 ID（S3 兼容 API） | 敏感 | Backblaze B2 账户；存储与流量按量计费（有免费额度） |
| `B2_APPLICATION_KEY` | B2 应用密钥（创建时仅显示一次） | 敏感 | 同上 |
| `B2_BUCKET_NAME` | B2 桶名 | 非敏感 | 同上 |
| `B2_REGION` | B2 桶区域（推导 S3 endpoint） | 非敏感 | 同上 |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase 项目 URL（前后端共用） | 非敏感 | 本地栈免费；hosted 有免费档，超额计费 |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key（设计为可公开） | 非敏感 | 同上 |
| `SUPABASE_SERVICE_ROLE_KEY` | service-role key，server-only | 敏感（禁止进浏览器） | 同上 |

### 5.2 可选（未配置时对应能力返回 503 或使用默认值）

| 变量 | 用途 | 敏感性 | 外部账户 / 费用风险 |
|---|---|---|---|
| `B2_PUBLIC_URL_BASE` | 公有桶稳定 URL 基址 | 非敏感 | B2 |
| `SUPABASE_URL` / `SUPABASE_ANON_KEY` | 分离部署时的覆盖项 | 非敏感 | Supabase |
| `AUTH_CACHE_TTL_SECONDS` | 身份查询缓存 TTL（默认 30） | 非敏感 | 无 |
| `NVIDIA_API_KEY` | NVIDIA NIM key（`nvapi-` 前缀） | 敏感 | build.nvidia.com 免费 key 含初始额度，超额按量计费 |
| `NVIDIA_IMAGE_MODEL`、`GENERATION_*` 系列 | 生成模型与参数（默认值在 settings.py） | 非敏感 | 生成调用按量 |
| `STRIPE_SECRET_KEY` | Stripe secret（测试模式 `sk_test_` 前缀） | 敏感 | Stripe 账户；test mode 不产生真实扣费 |
| `STRIPE_WEBHOOK_SECRET` | webhook 签名密钥（`whsec_` 前缀） | 敏感 | Stripe CLI 本地转发 |
| `STRIPE_PRICE_PRO` / `STRIPE_PRICE_TEAM` | 价格 ID（由 `pnpm stripe:seed` 生成） | 非敏感 | Stripe |
| `BILLING_SUCCESS_URL` / `BILLING_CANCEL_URL` / `BILLING_PORTAL_RETURN_URL` | 支付后跳转 | 非敏感 | 无 |
| `NEXT_PUBLIC_API_URL` | 前端到 API 的地址（默认本机 8000） | 非敏感 | 无 |
| `ENABLE_DOCS` | 开放 `/docs` 等交互文档（默认关） | 非敏感 | 无 |
| `API_CORS_ORIGINS` / `API_CORS_ORIGIN_REGEX` | CORS 白名单 | 非敏感 | 无 |
| `TRUST_PROXY` | 信任 X-Forwarded-For（默认关） | 非敏感 | 无 |
| `METRICS_TOKEN` | `/metrics` Bearer 保护 | 敏感（自设随机串） | 无 |
| `API_PORT` | API 端口（默认 8000） | 非敏感 | 无 |

## 6. 外部服务与费用/账户要求

| 服务 | 角色 | 必需性 | 配置来源 | 受影响能力 | 费用/账户 |
|---|---|---|---|---|---|
| Backblaze B2 | 对象存储（S3 兼容，boto3） | 必需 | `.env` B2_* | 上传、文件管理、AI 产物保存 | 需注册；按量计费有免费额度 |
| Supabase | 认证 + Postgres | 必需 | `.env` 三个变量；本地栈由 `supabase start` + `sync-supabase-env.mjs` 自动写入 | 登录、角色、全部业务表 | 本地免费；hosted 免费档起 |
| Stripe | 订阅计费 | 可选 | `.env` STRIPE_* + `pnpm stripe:seed/listen` | `/billing`、计划门控（未配置 503） | test mode 免费；live 涉及真实扣费 |
| NVIDIA NIM（Genblaze SDK 编排） | 文生图 `flux.1-dev` | 可选 | `.env` NVIDIA_API_KEY | `/generate`（未配置 503） | 免费 key 含初始额度，超额按量 |
| npm registry / PyPI | 依赖安装来源 | 安装时需要 | `pnpm-lock.yaml` / `requirements.txt` | 依赖安装 | 免费；本机可达性未验证 |
| Vercel / Railway / Render / Fly | 生产部署 | 本需求不涉及 | `apps/web/railway.json`、`services/api/railway.json`、`services/api/vercel.json`、`infra/railway/README.md` | 部署 | 未验证，本需求不部署 |

本需求未注册任何服务、未产生外部写入或费用。

## 7. 当前运行条件

证据：`scripts/doctor.mjs` 的版本常量、README Quick Start、`package.json` engines。本机探测命令均为只读 `--version` 类命令。

| 条件 | 要求 | 本机现状 | 状态 |
|---|---|---|---|
| Node.js | >= 20 | v23.11.0 | 已满足（已验证） |
| pnpm | >= 9 | 未安装 | 缺失（阻塞，可经 `corepack enable` 提供） |
| Python | >= 3.11 | 3.11.15 | 已满足（已验证） |
| Git | 无硬性要求 | 2.55.0 | 已满足（已验证） |
| Docker（Supabase 本地栈依赖） | 守护进程运行 | CLI 29.7.2 已装，守护进程未运行 | 缺失（阻塞，需启动 Docker Desktop 或改用 Colima） |
| Supabase CLI | 本地栈需要 | 未安装 | 缺失（阻塞，`brew install supabase/tap/supabase`） |
| Stripe CLI | 仅可选 Stripe 测试需要 | 未安装 | 缺失（非阻塞，对应可选能力） |
| B2 账户与凭据 | 启动必需 | 未提供 | 待用户决定 |
| Supabase 本地栈启动 | 启动必需 | 依赖 Docker + CLI，未验证 | 阻塞（同上两项） |
| npm registry 可达性 | 安装需要 | 未验证（GitHub 主站已确认异常） | 未验证 |
| PyPI 可达性 | 安装需要 | 未验证 | 未验证 |

## 8. 初始 Git 状态与结束时 Git 状态

| 时点 | 参考仓库状态 | 证据 |
|---|---|---|
| 初始（克隆完成后） | 干净：`## main...origin/main`，无未跟踪/未提交文件 | `git status --short --branch` |
| 结束（本报告生成前） | 干净：`git status --porcelain` 输出为空，HEAD 仍为 `1b9c094c8e171aed165a4eb8b519cd727549e60f` | 同命令复核 |

- 本需求未修改参考项目任何业务文件；macOS 在目录内生成的 `.DS_Store` 被参考仓库 `.gitignore` 覆盖，不影响状态判定（已验证）。
- 主仓库状态：仅新增本需求产物（`references/`、`progress/`、`tests/`、openspec change 文件勾选），无任何提交（已验证，结束时 `git status` 复核）。

## 9. 执行的命令与结果

| 命令 | 结果 | 结论 |
|---|---|---|
| `git ls-remote`（上游直连） / `curl` 各 GitHub 端点 | 主站与 codeload 传输停滞、raw 超时；api.github.com 正常 | 网络受限，走镜像 + API 交叉验证 |
| `git ls-remote https://gh-proxy.com/... HEAD refs/heads/main` | 返回 SHA `1b9c094c…e60f` | 镜像可用 |
| GitHub API `repos/.../branches/main` | SHA 与镜像一致 | 版本锚点已验证 |
| `git clone`（经 gh-proxy）→ `git remote set-url origin <上游URL>` | 成功，工作区干净 | 任务 1.2/1.3 完成 |
| 各运行时 `--version` 探测 | 见第 7 节 | 只读，无副作用 |
| `docker version` | 客户端正常，守护进程未运行 | 阻塞项 |
| `node scripts/doctor.mjs` | 退出码 1，报 3 项：pnpm 缺失、venv 未建、`.env` 缺失 | 与手工探测一致；脚本只读，无写入 |

评估后**未执行**的命令及原因（设计决策 4：默认只做可行性判断）：

| 命令 | 写入范围 | 未执行原因 |
|---|---|---|
| `pnpm install` | `node_modules/`（被 gitignore）+ 可能动锁文件 | pnpm 未安装；npm registry 可达性未验证；大量外部下载 |
| `python3 -m venv .venv && pip install -r requirements.txt` | `services/api/.venv/`（被 gitignore） | PyPI 可达性未验证；属 P01-S01-02 准备动作 |
| `supabase start` / `sync-supabase-env.mjs` | Docker 容器、卷、`.env` | Supabase CLI 与 Docker 守护进程均缺；需用户授权安装 |
| `cp .env.example .env` 并填值 | `.env`（被 gitignore） | 需要用户提供 B2 凭据；属下一需求输入 |

## 10. 基线结论与下一需求待决事项

基线本身：**已验证完成**——上游身份（URL、main、SHA、MIT License、干净 Git 状态）全部可追溯，仓库证据盘点与环境变量分类齐全。

当前不具备直接启动条件（阻塞）：pnpm、Supabase CLI 未安装，Docker 守护进程未运行，B2 凭据未提供。

P01-S01-02 需要用户提供或决定的事项：

1. **待用户决定**：是否授权安装 pnpm（`corepack enable`）与 Supabase CLI（brew）。
2. **待用户决定**：启动 Docker Desktop，或改为安装 Colima。
3. **待用户提供**：Backblaze B2 账户的 bucket 名称、区域、应用密钥（4 个 B2_* 必需变量）。
4. **待用户决定**：是否需要可选能力——Stripe 测试模式（装 Stripe CLI）与 NVIDIA NIM key；不需要则对应功能保持 503。
5. **待用户决定**：npm/PyPI 如不可达，是否使用镜像源。
