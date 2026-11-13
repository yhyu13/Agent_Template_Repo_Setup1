# Git Workflow — issue → worktree → PR

Coordinator 与并行 worker agent 的操作手册。骨架版：命令为 bash，PowerShell 差异见文末注。
<!-- TODO(agent): 把所有 <...> 换成本仓库真实的脚本名与命令后删除本行。 -->

## 0. Bootstrap（一次性，owner 做）

```bash
git status --short && git log --oneline -1 && git remote -v   # 三条都必须正常
gh auth status                                                  # 必须有 repo scope
```

## 1. 模型

- 一个 issue = 一个实现分支 + 一个 PR（`feat/` `fix/` `chore/` `docs/<issue>-<slug>`，slug ≤ 40 字符 kebab-case）。
- Trunk-based：main 受保护、始终可发布；分支短命（目标 < 2 天）。
- Worktree 位于 <worktree-dir>/<slug>（slug = 分支名 `/`→`-`）。

## 2. 角色与交接物

| 角色 | 负责 | 绝不做 |
|---|---|---|
| Coordinator | issue 拆解、文件所有权表、集成 | 在 worker 的 worktree 里实现 |
| Worker | 恰好一个 worktree 一个 issue：实现+证明+PR | 动别人的路径、审自己、无独立批准就合 |
| Verifier | 独立于 Worker 跑分级验证，记录级别、命令、观察结果与**没做哪一级** | 是实现者本人；用"自检"冒充验证 |
| Reviewer | 独立对抗式审查，记录 APPROVED + reviewed SHA | 是作者、与作者共享 worktree/会话 |

Verifier 与 Reviewer 可以是同一个人，但都不能是 Worker。**实现者自证是这个流程里最贵的
一种节约**：构建错误、mock 掩盖的退化，都是"自己说跑过了"漏出去的。

这三步可以由同一个 agent 顺序执行，但必须显式切换身份，并留下两条独立记录
（验证记录与 REVIEW 评论），而不是一句"我都检查过了"。

交接靠文件不靠聊天：issue 契约 → 分支 → PR 正文（模板见 `.github/PULL_REQUEST_TEMPLATE.md`）→ 验证日志。

## 3. Issue 契约（coordinator 逐字写入 issue）

标题动词开头；验收标准每条可机械判定（命令退出码 / 字节数 / 截图）；写明 In scope / Out of scope
路径、验证命令（reviewer 重跑的那一条）、阻塞边（#N 先合）。判不出来的验收标准改到能判为止。

## 4. Worktree 生命周期

```bash
<new-worktree 脚本> -Issue 42 -Slug webgl-audio -Kind feat   # 创建
cd <worktree-dir>/feat-42-webgl-audio && git status --short  # 确认隔离
# ...实现、跑 issue 里的验证命令...
git add <只加自己拥有的路径> && git commit -m "feat(x): ... (#42)"
git push -u origin feat/42-webgl-audio
gh pr create --draft --base main --title "..." --body-file /tmp/pr-42.md
gh pr ready 42                        # reviewer 审查通过前保持 draft
gh pr merge 42 --squash               # 仅在合并闸门全过后
<remove-worktree 脚本> && git worktree prune
```

### 禁止的 worktree 形态

- **禁止 worktree 内再建 worktree**——仓库里套一层仓库，之后每次 `git status` 都在骗人。
- **禁止把 worktree 放进系统临时目录**（`/tmp`、`%TEMP%`）：清理策略会连仓库一起删。
- **禁止在仓库外再开第 N 份 side checkout**：同一仓库最多一份工作树 + 若干 worktree。
- 目录名用 `<issue号>-<slug>` 或 `<type>-<slug>`，禁止随机名——否则没人知道哪份对应哪个 issue。
- **issue 关闭后立即** `git worktree remove` + 删本地分支；留着的话，三周后没人敢动它们。
- 产出（报告、复盘、截图）**进 `docs/`**，不许堆在仓库根——仓库根堆满未跟踪文件以后，
  `git status` 再也不能用来判断"有没有脏东西"。

## 5. 并行规则

- 单机并发 ≤ 3–4 个 worker；共享契约（接口/schema/文件布局）先在 main 稳定再拆分。
- 一个分支一个 worktree 一个写者，按文件所有权（CODEOWNERS）切，不按任务名切。
- 永不 `git stash`；端口/构建目录从 `WORKTREE_PATH` 派生，不复用固定值。

## 6. 冲突与失败协议

1. 请求 review 前：worktree 内 `git fetch origin && git rebase origin/main`。
2. 冲突在 worktree 内解决，重跑验证命令，只对自己分支 `git push --force-with-lease`。
3. 验证失败 → PR 保持 draft，evidence 块如实记录失败命令与退出码；不合并"基本绿"。
4. 合并后集成失败 → main 上新 PR `git revert <sha>`，不改写历史。
5. 被别的 issue 阻塞 > 1 天 → coordinator 重新切分，不悄悄扩大范围。

## 7. 合并政策

- 只 squash merge；PR 正文必须有 `Refs #N`（非用户批准不写 Closes/Fixes）、evidence 块、风险/回滚。
- 每个 PR 独立 review；reviewer 亲跑验证命令，APPROVED 评论记录命令、结果、reviewed SHA。
- review 后 head 有任何新 commit / rebase / force-push → 批准作废，重新审。
- 合并闸门清单见 `AGENTS.md`「合并闸门」。
- PowerShell 5.1 注：无 `&&`；`gh pr create` 用 `--body-file` 不用多行 `--body`。

## 8. 门禁血统（每条门禁写清它防的那次事故）

| 门禁 | 触发 | 它防的事故 |
|---|---|---|
| <lint / typecheck 命令> | 每次 commit | <一次真实的格式/类型债，附 issue 或 PR 号> |
| <test 命令> | 每次 PR | <一次回归，附 issue 号> |
| <build 命令> | 打 tag / 发布前 | <一次"CI 绿但构建失败"的发布事故，附 tag> |
| <真实环境验证> | 涉及真机/真实网络/外部域名的改动 | <一次本地全绿、真实环境全灭的事故，附 issue> |
| <合并闸门命令> | 每次合并 | <一次冲突合并或误合> |

**规则：新加一条门禁，必须能填上"它防的是哪次事故"。** 填不出来的门禁，半年后一定会
被当成噪音绕过——因为它没有任何人能说出为什么不能删。

反过来也成立：出了事故先问"哪条门禁本可以拦住它"，再决定加门禁还是补验证级别。**不要用
"以后大家注意点"代替门禁**，也不要为同一次事故堆三道门禁。
