## Why

后续运行、实验和架构拆解必须基于一个可重复定位且状态清晰的上游版本，否则观察结论无法复现，也容易把路线文档中的假设误当成参考项目事实。现在先为 Backblaze AI SaaS Starter Kit 建立版本、环境、依赖和启动前状态基线，为 P01-S01 后续需求提供可信起点。

## What Changes

- 将 Backblaze AI SaaS Starter Kit 放入固定参考目录，并记录仓库 URL、默认分支、commit SHA、License、远程地址和初始 Git 状态。
- 依据参考仓库实际文件核实目录模块、包管理方式、前后端运行方式、基础设施依赖及其配置来源。
- 枚举环境变量，并按必需性、敏感性和费用/账户要求进行分类，不记录任何真实 Secret。
- 形成 `progress/p01/reference_baseline.md`，说明当前具备与缺失的运行条件，以及下一需求需要用户提供或决定的事项。
- 仅进行无外部写入的读取、安全检查和基础安装或静态检查可行性判断；不修改参考项目业务逻辑、不注册付费服务、不部署，也不进入 P01-S01-02。

## Capabilities

### New Capabilities

- `reference-project-baseline`: 建立可追溯、可复现且不泄露 Secret 的参考项目版本与运行环境基线。

### Modified Capabilities

无。

## Impact

- 新增或使用 `references/p01-backblaze-ai-saas-starter-kit/` 作为固定参考仓库目录。
- 新增 `progress/p01/reference_baseline.md` 作为本需求的主要交付物。
- 影响后续 P01-S01-02、P01-S01-03 以及 P01-S02 对上游行为和源码的分析依据。
- 不影响 P01 正式项目代码、公开 API 或部署环境；不引入真实凭据和付费资源写入。
