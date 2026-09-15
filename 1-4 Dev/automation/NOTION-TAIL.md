# Notion sync tail — append to every Automation prompt

**策略（2026-06-08）**：Notion = Obsidian 全文备份 → 未来主库。运行报告须写 **完整 MD 正文** 到 Notion 页 body，不只 Summary 字段。详见 `1-1 GEO Readme/notion-sync/README.md`。

After report-notify.sh, add row to **Lovart Ops Reports**:

- data_source_id: `61514ed3-39e2-4d84-b860-8334d740823e`
- database: https://app.notion.com/p/1d50d2daf96d41b29739b67a80c0e714
- config: `~/Documents/Lovart Local Dev/Output/automation-reports/notion-config.json`

Use Notion MCP `notion-create-pages` with parent data_source_id and properties:
Title, Type, Status, Date (date:Date:start), Summary, Local Path, Artifact, Follow-up (__YES__ if L3 triggered).
