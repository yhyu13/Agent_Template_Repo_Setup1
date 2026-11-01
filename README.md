# AgentTemplateRepo1

<!-- TODO(agent): 本 README 是骨架。复制本模板到新项目后，由 agent 补齐：
     1) 项目一句话介绍（是什么、给谁用、当前阶段）；
     2) Quickstart（clone 后到能跑起来的最小命令序列）；
     3) 指向 AGENTS.md / docs/ 的导航表；
     4) License 名称（与 LICENSE 文件一致）。
     补完删除本 TODO 块。在模板仓库自身中使用时保持骨架不动。 -->

通用 agent 工作流模板仓库：issue → 分支 → worktree → 独立 review → 证据合并，
带沉淀 inbox 和三个常驻 skill。

## 复制后必改清单

| 位置 | 动作 |
|---|---|
| `AGENTS.md` 所有 `<占位符>` | TODO(agent): 按项目实际填写；不需要的小节整节删 |
| `docs/GIT_WORKFLOW.md` 的 `<...>` 段 | TODO(agent): 换成真实命令与脚本名 |
| `README.md` 本块 | TODO(agent): 补齐后删除 |
| `LICENSE` | TODO(agent): 确定许可证后替换占位（见文件内说明） |
| `.github/CODEOWNERS` | TODO(agent): 填入真实文件所有权表 |
| `.github/workflows/ci.yml` | TODO(agent): 把占位命令换成真实 lint/test |
| `docs/REVIEW.md` / `docs/TESTING.md` | fill later on demand：有真实 review/test 实践后再填 |

## 结构

- `AGENTS.md` — agent 行为规范（红线、合并闸门、沉淀纪律）。`CLAUDE.md` 只做 `@AGENTS.md` 导入。
- `docs/GIT_WORKFLOW.md` — 全流程操作手册；`docs/REVIEW.md`、`docs/TESTING.md` 按需填。
- `.claude/skills/` — 三个常驻 skill：truth-seeking-research（求真）、prompt-pro（提纲）、skill-distill（沉淀）。
- `.agent/inbox/` — agent 产出的候选沉淀，人审后合入；agent 不直接改 AGENTS.md。
- `.github/` — PR 模板（Evidence/Risk/Rollback）、issue 契约表单、CODEOWNERS。
- `scripts/` — worktree 生命周期脚本。

## 占位标记约定（全仓库通用）

- `TODO(agent)`：留给 agent 按上下文填，填完删标记。
- `fill later on demand`：文件先给骨架，出现真实实践再填。
- `DELETED-ON-PURPOSE`：故意不提供的内容，就地留一行说明，防止后续会话误补。
