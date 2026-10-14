# 04-setup — 环境搭建

- 快速上手：[`docs/quickstart.md`](../../docs/quickstart.md)
- 部署（本地 / Docker / 服务器）：[`docs/deploy-guide.md`](../../docs/deploy-guide.md)
- 目录与环境变量约定：[`路径契约.md`](路径契约.md)（变量定义在 `dev/automation/local-dev-env.sh`）
- 站点 / 品牌配置：`ops/site.json`（gitignored，字段见 `dev/scripts/library/site_profile.py`）；品牌专属资料放 `ops/brands/<brand>/`
- 本机定时任务模板：`dev/automation/plists/*.plist`，用 `bash dev/automation/plists/install.sh <label>` 渲染并加载

首次运行：

```bash
bash "dev/automation/bootstrap-local-dev.sh"   # 创建 $MFLOW_LOCAL_DEV_ROOT 目录骨架
bash "dev/scripts/session-init.sh"             # 会话门禁
bash "dev/scripts/run-tests.sh"                # 单元测试
```
