# Review 手册

<!-- fill later on demand: 骨架。当本仓库产出第一批真实 PR 后，把下面的清单按实际踩坑补全成
     可勾选的版本；在此之前按 AGENTS.md「合并闸门」+ 本文骨架执行。 -->

Reviewer（非作者、非同会话）审 PR 时按序检查：

1. **越界**：diff 是否只在 issue 的 in-scope 路径内（对照 CODEOWNERS）。
2. **验证**：亲跑 issue 契约里的验证命令，记录命令、退出码、关键输出。
3. **红线扫描**：AGENTS.md 硬红线逐条对照（密钥、构建产物、绝对路径、main 直推）。
4. **reviewed SHA**：记录审查时的 head SHA；作者后续 rebase 即作废。

APPROVED 评论格式：

```markdown
APPROVED
Reviewed SHA: <sha>
Verification: `<command>` → exit 0, <关键输出行>
```

有 blocking 发现时写 `CHANGES REQUESTED` + file:line + 理由，不写笼统的 LGTM 以外的话。
