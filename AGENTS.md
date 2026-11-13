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
| memory/README.md | **开工第一步**：症状路由表 + 不可漂移约束；`memory/` 优先于 `docs/` 旧长文 |
| docs/DECISIONS.md | 决策权限：哪些自己拍板、哪些必须回用户、怎么问最小问题 |
| docs/GIT_WORKFLOW.md | issue → 分支 → worktree → PR → review → merge 全流程与合并闸门 |
| docs/REVIEW.md | reviewer 检查清单与 APPROVED 评论格式 |
| docs/TESTING.md | 验证分级（L1 静态 / L2 行为 / L3 构建 / L4 真实环境） |

开工顺序固定：`memory/README.md` → 命中的 `memory/*` 领域文档 → 改哪个目录读哪个目录的
`AGENTS.md`。先查 `memory/symptom-routing.md`，没有命中就补一行——不先查等于每次重新踩坑。

## 决策权限

`docs/LEVELS.md` 回答"能不能动手"；本节回答"这个判断能不能自己拍板"。两者独立：一个 L3
（可自动合并）的任务里，照样可能有必须回用户的判断。

- **A 代码可判定** → 自行决定，在 PR 里留一行：决策 + 依据（`file:line`）。
- **B 事实不在仓库里**（真机、真实网络、生产数据、用户要的口吻、没写下来的业务规则）→
  发**一次**最小问题清单，然后停。
- **C 产品 / 体验方向**（多个都可接受、没有事实能裁决）→ 给 2–3 个选项与后果，不替用户选。

三条硬约束：不要因为"看起来显然"把 C 降级成 A——这是返工的高发区；不要多轮追问，问不到
就升级为 C 给选项；问题必须能用产物回答（toast 原文 / 截图 / 机型与系统 / 具体那两行数据），
禁止"你觉得怎样"。**沉默不是批准。** 决策表格式见 docs/DECISIONS.md。

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

**验证者不得是实现者。** 实现者自己跑的那叫自检，不叫验证；分级证据必须由另一个人
（另一个会话 / 另一个 agent）跑并记录「在哪跑、什么命令、观察到什么、哪一级没做」。
reviewer 与 verifier 可以是同一人，但都不能是作者。

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

**两个出口，一个门槛，同一个 PR。**

| 学到的东西 | 写到哪 | 形态 |
|---|---|---|
| 新症状（"用户这么说时该打开哪里"） | `memory/symptom-routing.md` | 一行 |
| 不可漂移的约束 | `memory/invariants.md` | 一条：rule + because + check |

- **门槛**：这轮学到的东西如果写不成上面两处的一行，它就不值得进记忆。写不成行说明还没
  想清楚，或者它只是过程流水——过程写进 PR 描述就够了。
- **同一个 PR**：症状行与约束条必须和修复一起进 PR，不要等验收后补。验收后的记忆一定丢。
- **禁止 agent 直接编辑本文件**（bootstrap 填占位除外）。要改规则本身 → `.agent/inbox/`
  提案，由人审。
- `.agent/inbox/<YYYY-MM-DD>-<短名>.md` 是"还没把握 / 需要人裁决"的暂存区：
  `type: pitfall|convention|fact` / `confidence: verified|suspected` /
  `suggested-home: memory/<篇> | AGENTS.md#<节>` / `source: "<证据>"`；
  suspected 且无证据的直接删。
- **方向被推翻时，就地标注而不是删除**：在该段落前加
  `⚠️ 本节已在 <YYYY-MM-DD> 修订：<新口径>`，并保留旧文。删掉旧方向，下一个人会重做一遍。

## 语言

文档、代码、注释、commit message 用英文；与用户交流可用中文。
