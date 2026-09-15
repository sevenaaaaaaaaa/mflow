# MFlow 插件规范（v1）

> 插件 = 以约定目录结构放入 `plugins/` 的能力包，无需改动内核代码即可扩展三类能力。
> 发现机制：工作台启动与 `plugin_check.py` 扫描 `plugins/*/manifest.json`。

## 三类插件

| 类型 | type | 注册点 | 约定 |
|------|------|--------|------|
| 数据源 | `source` | Trident 步骤表 / Sentinel 源列表 | `entry.py` 暴露 `collect() -> dict`，输出 JSON 到 `$LOVART_LOCAL_DEV_ROOT/Output/Data Ingestion/` |
| 发布渠道 | `publisher` | `1-4 Dev/scripts/publish_adapters/` 同接口 | `entry.py` 暴露 `publish(item, cfg) -> {"ok", "url", "cms_id"}` |
| 模板包 | `template` | `templates/` | 单 JSON（见模板市场，无需代码） |

## manifest.json

```json
{
  "id": "my-source",
  "type": "source",
  "name": "人类可读名称",
  "version": "1.0.0",
  "author": "…",
  "entry": "entry.py",
  "permissions": ["network", "credentials:trident"],
  "config": {"api_key": {"desc": "…", "required": true}}
}
```

## 校验与安装

```bash
python3 plugins/plugin_check.py plugins/my-source   # 校验 manifest/entry/权限声明
```

六项检查：manifest 必填字段 / type 枚举 / entry 文件存在 / entry 暴露约定函数 /
无明文密钥（_permissions 里声明 credentials:* 才允许读凭证目录）/ 目录名与 id 一致。

## 权限模型

- `network`：允许出站请求
- `credentials:<scope>`：允许读取对应凭证目录（trident/sentinel/sanity）
- 未声明的行为在 code review 时视为不合规；工作台不自动执行未通过 plugin_check 的插件
