# AGENTS.md — <项目名>

<!-- TODO(agent): 复制本模板后，把所有 <占位符> 换成真实内容；不需要的小节整节删除，不要留空壳。 -->

<一句话：这个仓库是什么、给谁用、当前处于什么阶段。>

## 占位标记约定

- `TODO(agent)`: 需要 agent 按上下文填写的占位，填完删除标记。
- `DELETED-ON-PURPOSE`: 故意不提供的文件/小节。在对应位置留一行说明为什么不要，防止后续会话误以为缺失而补错。

## 事实优先级

文档冲突时：**当前代码 > memory/（或本文件）> docs/ 下旧长文**。
产品规格冲突以 docs/spec.md 为准。本文件与角色契约冲突时以本文件为准。

## Read first

| 文件 | 内容 |
|---|---|
| docs/GIT_WORKFLOW.md | issue → 分支 → worktree → PR → review → merge 全流程与合并闸门 |
| docs/REVIEW.md | reviewer 检查清单与 APPROVED 评论格式 |
| docs/TESTING.md | 验证分级（L1 静态 / L2 行为 / L3 构建 / L4 真实环境） |

## 硬红线

1. **不经用户明确指令不 commit / push**；禁止直推 main，禁止 force-push main，禁止 `git stash`（跨 worktree 串扰）。
2. **先有 issue 号，再开分支**；一个 issue = 一个分支 = 一个 PR。
3. **PR 写 `Refs #N`，禁止 Closes/Fixes/Resolves**；issue 只由用户关。合并不等于完成。
4. **证据先于宣布完成**：完成必须有命令输出证明（退出码 / 测试摘要 / 文件清单），否则明确说未验证。
5. **不在 main 上直接改**；动手前 `git branch --show-current` 确认，不对就停下来问。
6. **禁止入库**：密钥、用户数据、构建产物、机器特定绝对路径（用相对路径和环境变量）。
7. **一个文件一个写者**；并行 agent 按 `CODEOWNERS` 切分。

## 合并闸门（合并前逐条核验）

- `git fetch origin` 后 `gh pr view <N> --json mergeable,mergeStateStatus` 为 `MERGEABLE` / `CLEAN`；
- main worktree `git status --porcelain` 干净（远程 mergeable 看不到本地脏）；
- `git merge-tree $(git merge-base origin/main origin/<head>) origin/main origin/<head>` 无
  `changed in both`（该命令恒退出 0，必须 grep 判断）；
- 要求的验证命令通过；无越界路径、无红线内容。
- 自合并仅当：有非作者、非同会话 reviewer 的 APPROVED（reviewer 亲跑验证命令并记录结果与
  reviewed SHA）；review 后 head 出现新 commit / rebase / force-push 一律作废重审。
  高危变更（<列出，如：依赖升级、基础设施、数据库迁移>）额外需 owner sign-off。

## 验证基线

<!-- TODO(agent): 把下面四条换成真实命令。 -->
- 局部变更：<test / lint / typecheck 中最相关的最小命令>
- 跨模块或交付前：<完整 ci 命令>
- 主流程变更：<e2e 命令>
- 发布前必须本地跑通 <build 命令>：*CI 绿不等于能构建*。

该做到哪一级按「改动是否依赖真实的时间、网络、设备」定，分级规则见 docs/TESTING.md。

## 上下文纪律

- 不整读未变的文件；重读用 offset/limit。
- 测试/构建全量输出写进 git-ignored log，只看 tail（≤40 行）+ 立即捕获退出码。
- 先 `git diff --stat`，只展开在审文件的全量 diff。
- 列目录用 `git ls-files` / `-Depth 2`；定位用 `grep -l`，找到再读。
- 输出预计 >200 行就写临时文件再按需读片段。

## 项目特定约束

<!-- TODO(agent): 本项目的结构性事实（技术栈入口、软删除过滤、公开路由白名单等），
     每条带文件路径。超过 ~15 条时移出入本文件，由人审后归入 memory/ 或删除。 -->

## 沉淀纪律

- **禁止 agent 直接编辑本文件与 memory/core/**（bootstrap 时填占位除外）。学到的坑、约定、
  事实 → 写入 `.agent/inbox/<YYYY-MM-DD>-<短名>.md`：
  `type: pitfall|convention|fact` / `confidence: verified|suspected` /
  `suggested-home: AGENTS.md#<节> | memory/core/<篇>` / `source: "<证据>"`
  + 一句话结论、为什么、怎么防。
- inbox 由人定期审阅合入；suspected 且无证据的直接删。

## 语言

文档、代码、注释、commit message 用英文；与用户交流可用中文。
