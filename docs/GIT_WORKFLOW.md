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
| Reviewer | 独立对抗式审查，记录 APPROVED + reviewed SHA | 是作者、与作者共享 worktree/会话 |

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
