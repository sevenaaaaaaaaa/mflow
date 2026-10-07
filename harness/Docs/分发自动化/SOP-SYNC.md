# SOP 同步说明

Canonical SSOT（Obsidian）：

`LifeOS Pro PARA Vault/2-Area/Product Project Management/全渠道内容分发自动化SOP.md`

因 iCloud 目录当前对 Cursor 不可读，本工作副本位于：

`~/Projects/content-distribution/`

## 同步到 Obsidian（本机执行）

```bash
DEST="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/2-Area/Product Project Management/content-distribution"
mkdir -p "$DEST"
rsync -av --exclude '.env' ~/Projects/content-distribution/ "$DEST/"
```

## 与 SSOT 对齐项

本目录 `SOP-DECOMPOSED.md` + `RUNBOOK.md` 已落实规划中的：

- Gate 0 防抢权重
- GA 评分模型
- 10 平台矩阵
- 双轨 A/B 流程
- Trident 数据接入
- MVP（Medium + DEV.to）

若 Obsidian SOP 有额外渠道或规则，以 SSOT 为准合并到 `RUNBOOK.md`。
