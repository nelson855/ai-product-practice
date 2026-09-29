# AI Agent 开源项目仿做与实践路线

> 目标：通过 3 个不同复杂度的开源项目，完成从 **AI Feature → 固定 Workflow → Tool/Research Agent** 的实践过渡。
>
> 这份路线不是让你“Fork 后改一改就上线”，而是建议采用：
>
> **跑起来 → 拆架构 → 缩需求 → 脱离原代码重写 → 对照复盘 → 再决定是否产品化。**

---

## 0. 先给结论

结合你当前的状态，我建议优先研究以下 3 个主项目，并保留 1 个扩展项目：

| 层级 | 推荐项目 | 主要定位 | 我建议的用途 |
|---|---|---|---|
| Level 0/1 | Backblaze AI SaaS Starter Kit | AI 图片生成 + 完整 SaaS 外壳 | 学“一个 AI 功能如何真正变成可上线产品” |
| Level 1/2 | DAIR.AI Deep Research Agent | Planner → Search → Writer 的固定研究 Pipeline | 学“什么时候用固定 Workflow，而不是自由 Agent” |
| Level 2/3 | LangChain RAG Research Agent Template | RAG + Routing + Planning + Research Subgraph | 学“真正 Agent/Graph 的路由、计划、循环与状态” |
| 扩展 | darshil0/deep-research-agent | 更完整的研究型 Agent 产品 | 学产品化的 Research Agent：多搜索源、迭代研究、PDF 导出、错误恢复 |

推荐顺序：

```text
项目 1：AI Feature / SaaS
        ↓
项目 2：固定 Workflow
        ↓
项目 3：真正 Agent / Graph
        ↓
可选：更完整的 Research Agent 产品
```

---

# 1. 项目一：Backblaze AI SaaS Starter Kit

GitHub：

https://github.com/backblaze-labs/ai-saas-starter-kit

License：MIT

## 1.1 它是什么

这是一个相对完整的 AI SaaS Starter Kit，核心技术栈包括：

```text
Next.js 16
React 19
FastAPI
Supabase
Stripe
Backblaze B2
NVIDIA NIM / Flux 图片生成
```

项目已经包含：

- 用户注册和登录；
- 邮箱 OTP；
- 用户 Profile；
- Free / Pro / Team 套餐；
- Stripe Checkout；
- Billing Portal；
- AI 文生图；
- 文件上传和文件管理；
- 对象存储；
- Admin Console；
- Audit Log；
- `/health`、`/metrics`；
- E2E Test；
- Vercel + Railway / Render / Fly.io 等部署说明；
- 专门给 AI Coding Agent 使用的 `AGENTS.md` 和架构文档。

它最大的特点不是“Agent 多复杂”，恰恰相反：

> **AI 只是整个产品中的一个能力。**

图片生成流程本身很简单：

```text
用户输入 Prompt
      ↓
调用图片模型
      ↓
生成图片
      ↓
保存到对象存储
      ↓
生成记录
      ↓
返回页面
```

真正复杂的是外面的产品工程。

---

## 1.2 为什么值得你学习

这是我最推荐你第一个实践的项目。

因为你已经学了不少 Agent 技术，但如果你的目标是“自己做 AI 产品并上线”，你当前更需要补的是：

```text
Auth
Billing
Storage
Quota
User Data
Deployment
Logs
Admin
Error Handling
Product UX
```

而不是继续给 Agent 增加 Memory、Planning、Multi-Agent。

### 最值得关注的 6 个点

#### ① AI 能力只是一个模块

观察它如何把：

```text
AI Provider
```

限制在相对清晰的边界中，而不是整个系统处处直接调用模型 SDK。

#### ② 用户体系

重点看：

```text
登录
权限
Profile
Admin
Protected Route
```

这些能力对于真正上线的产品几乎是必需品。

#### ③ Stripe 计费

重点理解：

```text
用户购买套餐
      ↓
Stripe Checkout
      ↓
Webhook
      ↓
数据库更新 Subscription
      ↓
后端判断当前 Plan
      ↓
允许 / 禁止 AI 能力
```

#### ④ 文件存储

图片产品尤其需要理解：

```text
上传
对象存储
Metadata
下载
删除
访问 URL
```

#### ⑤ AI Coding 友好的仓库结构

这个项目专门维护：

```text
AGENTS.md
ARCHITECTURE.md
docs/
```

而且通过结构测试约束 AI Coding Agent 不要破坏分层。

这和你之前自己建立 `AGENTS.md` 的学习方式非常契合。

#### ⑥ 部署

它已经把：

```text
Frontend → Vercel
Backend → Railway / Render / Fly.io
```

这类典型个人开发者部署方式整理得比较清楚。

---

## 1.3 我建议你怎么操作

### Step 1：原样跑起来

不要修改代码。

完成：

```text
Clone
↓
安装依赖
↓
配置最少环境变量
↓
注册
↓
登录
↓
上传文件
↓
跑一次 AI 图片生成
```

如果 Stripe / AI Provider 配置比较麻烦，可以先只跑 Auth + 文件上传。

### Step 2：让 AI Coding 工具帮你画架构图

要求它回答：

```text
一次 AI 图片生成请求经过哪些层？

Controller / API 在哪里？
Service 在哪里？
Provider SDK 在哪里？
文件什么时候进入 B2？
数据库什么时候写入？
失败怎么处理？
用户套餐在哪里检查？
```

### Step 3：删除 70% 功能

你自己的练习版只做：

```text
登录
图片上传
一种图片生成
生成历史
文件保存
```

第一版不要做：

```text
Team
复杂 Admin
完整 Billing
多模型
复杂权限
```

### Step 4：不要 Fork 后继续魔改

建议：

```text
关闭原项目
↓
写自己的 PRD
↓
让 Codex 从空仓库生成
↓
重新实现
```

然后再回来比较两份代码。

这样才能真正学习。

---

# 2. 项目二：DAIR.AI Deep Research Agent

GitHub：

https://github.com/dair-ai/deep-research-agent

License：MIT

## 2.1 它是什么

这是一个研究型 AI 应用，目前主要流程是 3 个阶段顺序执行：

```text
Planner
   ↓
WebSearch
   ↓
ReportWriter
```

项目当前使用：

```text
Next.js 15
React 19
Claude / Claude Agent SDK
Exa Search
Vercel Sandbox
```

功能包括：

- 输入一个研究主题；
- Planner 生成搜索策略；
- WebSearch Agent 调用 Exa；
- 读取网页内容；
- ReportWriter 生成 Markdown 报告；
- Inline Citation；
- 实时展示 Pipeline 进度；
- Streaming；
- Vercel 部署。

---

## 2.2 为什么值得学习

它非常适合回答你刚才的一个核心问题：

> **很多所谓 Agent，流程是不是完全可以写死？**

答案是：可以。

这个项目虽然叫 Multi-Agent Pipeline，但从控制流角度，你完全可以把它理解成：

```java
Plan plan = planner.create(topic);
SearchResult results = searcher.search(plan);
Report report = writer.write(results);
```

也就是说：

> **程序决定“下一步做什么”，LLM 决定“这一步具体生成什么”。**

这就是固定 Workflow。

### 最值得关注的 5 个点

#### ① Planner 的输入输出

重点看 Planner 到底返回什么：

```text
自然语言？
Structured Output？
Search Query？
Date Range？
```

#### ② 阶段边界

观察：

```text
Planner
WebSearch
Writer
```

各自知道什么、不知道什么。

#### ③ Search Tool

重点理解：

```text
LLM
vs
Search API
```

真正事实来源应该来自 Search，而不是模型自己编。

#### ④ Streaming / Progress

研究任务可能几十秒甚至数分钟。

页面如何告诉用户：

```text
正在规划
正在搜索
正在读取资料
正在生成报告
```

这是很实用的产品体验。

#### ⑤ Sandbox / Deployment

它在 Vercel 部署 Claude Agent SDK 时使用 Sandbox，因为某些运行方式需要 subprocess 能力。

这很适合你观察：

> **本地能运行的 Agent，部署到 Serverless 后不一定还能原样运行。**

---

## 2.3 我建议你怎么仿

这里我反而建议你**不要照着它的 Multi-Agent 设计先写**。

第一版主动“降级”为普通 Workflow：

```text
ResearchWorkflow
│
├── createPlan()
├── search()
├── extractEvidence()
├── writeReport()
└── validate()
```

例如：

```java
public Report research(String topic) {
    ResearchPlan plan = planner.create(topic);
    List<SearchResult> results = search.search(plan);
    List<Evidence> evidence = extractor.extract(results);
    Report report = writer.generate(evidence);
    return validator.validate(report);
}
```

你可以用：

```text
Spring AI
或
LangChain4j
```

但**不要加 Agent Loop**。

等固定 Workflow 完成后，再问自己：

> 哪个节点真的需要自主决定下一步？

如果没有，那么它根本不需要变成自由 Agent。

---

# 3. 项目三：LangChain RAG Research Agent Template

GitHub：

https://github.com/langchain-ai/rag-research-agent-template

License：MIT

> **重要：该仓库已于 2026-03-11 被作者归档，目前为只读。**
>
> 因此我推荐它作为“架构学习材料”，而不是新的长期产品模板。

## 3.1 它是什么

这是 LangChain 官方曾经维护的 LangGraph Research Agent Template。

核心包含三个 Graph：

```text
Index Graph
Retrieval Graph
Researcher Subgraph
```

典型流程：

```text
User Query
   ↓
判断问题类型 / Route
   ↓
生成 Research Plan
   ↓
逐步执行 Plan
   ↓
生成多个 Search Query
   ↓
并行 Retrieval
   ↓
更新 Research State
   ↓
继续下一步
   ↓
生成最终回答
```

还包含：

- Chat History；
- Routing；
- Research Plan；
- Subgraph；
- Parallel Retrieval；
- Thread；
- State；
- Debug / State Replay 思路。

---

## 3.2 为什么值得学习

这是前三个项目中，第一个真正值得你从 **Agent / Graph** 角度学习的项目。

### 最值得关注的 6 个点

#### ① Routing

用户输入以后，并不是固定调用 Search。

系统先决定：

```text
这是需要研究的问题？
问题是否模糊？
是否应该追问？
是否属于当前知识域？
```

这里开始出现真正的条件路由。

#### ② Plan

它不是：

```text
search → write
```

而是：

```text
先规划若干研究步骤
↓
逐步执行
```

#### ③ Subgraph

Researcher 自己又是一张 Graph。

这对应你之前学过的：

```text
Workflow Composition
Sub Agent / Subflow
```

#### ④ Parallel Retrieval

多个查询可以：

```text
Query A ─┐
Query B ─┼→ Merge
Query C ─┘
```

#### ⑤ State

重点看：

```text
当前研究到哪一步？
剩余 Plan 是什么？
已经有哪些文档？
Chat History 是什么？
```

这些数据不再只是几个局部变量。

#### ⑥ Debug / Replay

LangGraph 的价值开始出现：

```text
查看某个 state
修改 state
从历史 state 重新执行
```

这正是你后面如果继续学习 LangGraph 时要重点理解的东西。

---

## 3.3 怎么使用它

因为项目已经 Archived，我不建议：

```text
Fork
↓
长期维护
↓
直接做成你的产品
```

我建议：

### 第一步

跑通或者至少读通：

```text
src/index_graph/
src/retrieval_graph/
src/retrieval_graph/researcher_graph/
```

### 第二步

画出：

```text
State
Node
Edge
Subgraph
```

### 第三步

用你自己的业务重新实现一个更小版本，例如：

> SEO 关键词 Research Agent

```text
Keyword
  ↓
Judge Intent
  ↓
Plan Research
  ↓
Search Competitors
  ↓
Search Trends
  ↓
Analyze
  ↓
Need More Data?
  ├── Yes → Search again
  └── No  → Report
```

这时候如果你发现：

```text
状态多
分支多
需要恢复
需要 HITL
```

再正式深入 LangGraph。

---

# 4. 扩展项目：darshil0/deep-research-agent

GitHub：

https://github.com/darshil0/deep-research-agent

License：MIT

## 4.1 它是什么

这是一个更偏“完整 Research Agent 产品”的项目。

当前 README 描述的能力包括：

- Gemini 2.0 Flash；
- Tavily / Google Search Tool / Hybrid Search；
- Iterative Research；
- Query Decomposition；
- Provider Fallback；
- Citation；
- 多语言；
- Web UI；
- WebSocket；
- PDF Export；
- API Authentication；
- 并发限制；
- Rate Limit / Provider Failure 考虑。

相比 LangChain 的 Template，它更接近：

> **“别人已经试着把 Research Agent 做成产品是什么样子。”**

---

## 4.2 为什么值得作为第四个看

前三个项目分别重点训练：

```text
产品工程
Workflow
Agent Architecture
```

这个项目则帮助你观察：

```text
Agent Architecture
        +
Production concerns
```

例如：

- 搜索 Provider 挂了怎么办；
- Query 数量怎么限制；
- 并发多少；
- PDF 在 Serverless 上为什么麻烦；
- Session 怎么保存；
- 成本和延迟如何控制。

我不建议你把它作为第一个项目，但很适合第三个项目之后研究。

---

# 5. 建议的统一练习方法

不要对四个项目采用不同的随意玩法。

统一使用下面这个流程。

## Phase 1：原样运行

目标：站在**用户**角度理解产品。

不要修改代码。

记录：

```text
输入是什么？
输出是什么？
一次任务耗时多久？
失败体验是什么？
需要哪些第三方服务？
```

---

## Phase 2：架构拆解

让 Codex / Claude Code 帮你输出：

```text
ARCHITECTURE_ANALYSIS.md
```

至少回答：

1. 用户一次请求经过哪些模块？
2. 哪一步调用 LLM？
3. 哪一步调用外部 API？
4. 哪一步访问数据库？
5. 哪一步写对象存储？
6. 流程由代码控制还是 LLM 控制？
7. 是否存在 Agent Loop？
8. State 在哪里？
9. 失败重试在哪里？
10. 部署有哪些特殊要求？

---

## Phase 3：缩需求

只取原项目约 20%～30% 功能。

原则：

> **学习一个核心问题，不是复刻整个公司。**

例如：

### 图片 SaaS

```text
原版：
Auth + Billing + Team + Admin + Storage + AI + Metrics...

你的版本：
Auth + Upload + AI + History
```

### Deep Research

```text
原版：
Planner + Multi-Agent + Streaming + Sandbox + Citation...

你的版本：
Plan + Search + Report
```

---

## Phase 4：从空目录重写

这是最重要的一步。

不要继续 Fork 原项目。

创建：

```text
my-ai-image-app
my-research-workflow
my-research-agent
```

然后给 AI Coding 工具：

```text
你的 PRD
你的架构图
你的技术约束
你的验收标准
```

让它从零实现。

---

## Phase 5：Diff

完成以后重新打开原项目，比较：

```text
别人为什么这样分层？

我的版本漏了哪些失败场景？

哪些东西我过度设计了？

哪些东西对方过度设计了？

哪些代码应该让框架承担？
```

这一步通常比“跟着教程敲一遍”更有价值。

---

# 6. License 与合规边界

> 以下是工程实践层面的风险提示，不构成正式法律意见。真正商业发布前，如果项目价值较高，建议对最终依赖、数据来源、模型条款和商标进行一次正式检查。

## 6.1 这几个项目的 License

当前检查结果：

| 项目 | License | 商用 | 修改 | 需要保留 License / Copyright |
|---|---|---|---|---|
| Backblaze AI SaaS Starter Kit | MIT | 通常允许 | 允许 | 是 |
| DAIR.AI Deep Research Agent | MIT | 通常允许 | 允许 | 是 |
| LangChain RAG Research Agent Template | MIT | 通常允许 | 允许 | 是 |
| darshil0/deep-research-agent | MIT | 通常允许 | 允许 | 是 |

MIT 是非常宽松的开源许可证。

一般允许：

```text
使用
复制
修改
发布
分发
再许可
商业使用
```

但必须保留许可证中的：

```text
Copyright Notice
License Notice
```

因此：

> **MIT 不等于“删掉 LICENSE 当成完全原创”。**

---

## 6.2 Fork / 复制代码 vs 学习后重写

这两种行为要区分。

### A. 直接 Fork / 大量复制代码

建议：

```text
保留原 LICENSE
保留原版权声明
增加 THIRD_PARTY_NOTICES.md
说明基于哪个项目修改
```

### B. 阅读架构后，自己从头实现

如果最终没有复制受版权保护的具体实现代码，通常比直接 Fork 更干净。

但不要故意让 AI 对原代码做近乎逐行改写，然后声称完全原创。

学习阶段不需要过度纠结；商业发布阶段需要把来源关系理清楚。

---

# 7. 除了 License，还有 8 类更容易被忽略的合规问题

很多开发者只看 LICENSE，这其实不够。

## 7.1 第三方依赖 License

仓库是 MIT，不代表：

```text
它所有依赖
所有字体
所有图片
所有数据
```

都是 MIT。

上线前建议生成 dependency license report。

重点检查：

```text
GPL / AGPL
商业限制 License
字体 License
UI Asset License
模型权重 License
```

---

## 7.2 AI 模型服务条款

例如项目里使用：

```text
Anthropic
OpenAI
Google Gemini
NVIDIA
```

你还需要遵守具体 Provider 的：

- API Terms；
- Acceptable Use；
- 数据处理规则；
- 商用规则；
- 区域限制；
- Rate Limit；
- 内容政策。

**开源项目的 MIT License 不会替你解决模型服务条款。**

---

## 7.3 Search Provider 条款

研究型 Agent 可能使用：

```text
Exa
Tavily
Google Search
```

需要关注：

```text
是否允许缓存结果？
是否允许展示全文？
是否允许商业重分发？
是否有速率限制？
是否必须注明来源？
```

---

## 7.4 网页内容版权

Research Agent 搜网页以后，不代表可以：

```text
把整篇文章复制进报告
```

产品应该优先：

```text
总结
引用少量必要内容
提供来源链接
```

而不是做内容镜像。

---

## 7.5 用户上传文件

如果用户上传：

```text
PDF
图片
合同
内部资料
```

你需要考虑：

- 隐私政策；
- 保存多久；
- 谁能访问；
- 是否传给第三方模型；
- 用户能否删除；
- 日志中是否泄露内容。

---

## 7.6 API Key / Secret

永远不要：

```text
把 Provider API Key 放浏览器
把 Stripe Secret 放前端
提交 .env 到 Git
把 Vercel Token 返回客户端
```

Research Agent 尤其要注意 Sandbox / MCP / Tool 的 Secret 传播。

---

## 7.7 品牌与商标

MIT 允许代码商用，不代表允许你：

```text
直接使用原项目 Logo
假装是 Backblaze / LangChain 官方产品
复制产品名称造成混淆
```

代码版权和商标是不同问题。

建议自己的产品使用独立：

```text
名称
Logo
Domain
Branding
```

---

## 7.8 AI 输出责任

如果 Research Agent 输出：

```text
投资建议
医疗建议
法律建议
```

风险会显著上升。

你的前几个练习项目最好优先选择：

```text
低风险工具
内容生产
资料整理
开发者工具
SEO 分析
图片工具
```

而不是一开始做高风险专业决策 Agent。

---

# 8. 我建议你的实际项目顺序

## Project 1：AI 图片工具

参考：

```text
Backblaze AI SaaS Starter Kit
```

自己实现：

```text
AI Image Mini SaaS
```

V1：

```text
登录
上传
Prompt
生成
历史
```

学习目标：

```text
完整上线
```

不要学习 Agent。

---

## Project 2：Research Workflow

参考：

```text
DAIR.AI Deep Research Agent
```

自己实现：

```text
SEO Research Workflow
```

例如输入：

```text
“AI PDF Translator”
```

固定流程：

```text
Generate Search Plan
↓
Search
↓
Extract Evidence
↓
Analyze Competition
↓
Generate Report
```

学习目标：

```text
Workflow
Structured Output
Search API
Evidence
Citation
Streaming
```

暂时不要自由 Agent Loop。

---

## Project 3：SEO Research Agent

参考：

```text
LangChain RAG Research Agent Template
+
darshil0/deep-research-agent
```

自己实现：

```text
Keyword Research Agent
```

Agent 可以自主判断：

```text
数据够了吗？
↓
不够
↓
继续搜索

竞争对手信息够了吗？
↓
不够
↓
换关键词
```

这里才正式加入：

```text
Tool Calling
Loop
State
Planning
Tracing
Evaluation
```

如果此时你开始真正遇到：

```text
状态复杂
任务运行很久
任务需要中断恢复
人工审批
```

再回去继续你的：

```text
LangGraph Learning
```

这样 LangGraph 会学得非常快。

---

# 9. 每个项目我建议你保留的 5 个文档

你以后自己开发 AI 产品，可以形成固定习惯：

```text
README.md
AGENTS.md
PRODUCT.md
ARCHITECTURE.md
LEARNING_NOTES.md
```

## PRODUCT.md

只写：

```text
用户是谁
解决什么问题
核心流程
V1 包含什么
V1 不包含什么
```

## ARCHITECTURE.md

写：

```text
前端
后端
模型
数据库
Storage
第三方 API
关键 Flow
```

## AGENTS.md

约束 Codex / Claude：

```text
技术栈
目录边界
禁止过度设计
测试要求
不要擅自升级架构
```

## LEARNING_NOTES.md

每做一个项目都回答：

```text
哪些地方必须用 AI？
哪些地方普通代码更好？
哪些流程应该写死？
哪些决策适合交给 LLM？
我是否真的需要 Agent？
```

这一份文档长期来看价值会很高。

---

# 10. 最后一个判断原则

做这三个项目时，请始终使用下面这个顺序判断复杂度：

```text
能普通代码解决？
        ↓ Yes
普通代码
        ↓ No

一次 LLM 调用可以？
        ↓ Yes
AI Feature
        ↓ No

固定 Workflow 可以？
        ↓ Yes
Workflow
        ↓ No

需要模型动态选择 Tool？
        ↓ Yes
Tool Agent
        ↓

需要复杂长任务 / Resume？
        ↓ Yes
LangGraph / Durable Orchestration
        ↓

单 Agent 已经真的不够？
        ↓ Yes
Multi-Agent
```

**永远优先选择能解决问题的最低复杂度。**

这应该成为你今后做 Agent 产品最重要的一条工程原则。

---

# 11. Sources / 核查时间

本文基于 2026-09-28 对以下项目 README / GitHub 信息的核查：

- Backblaze AI SaaS Starter Kit  
  https://github.com/backblaze-labs/ai-saas-starter-kit
- DAIR.AI Deep Research Agent  
  https://github.com/dair-ai/deep-research-agent
- LangChain RAG Research Agent Template  
  https://github.com/langchain-ai/rag-research-agent-template
- darshil0/deep-research-agent  
  https://github.com/darshil0/deep-research-agent

重要状态：

- `langchain-ai/rag-research-agent-template` 已于 **2026-03-11** 归档，仅建议作为架构学习参考。
- 其他项目的依赖、API 和 License 状态在你真正 Fork / 上线前仍建议重新核查一次，因为开源项目会持续变化。
