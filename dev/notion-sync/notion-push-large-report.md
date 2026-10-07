# 大月报推送说明（>30KB）

当 `notion-push-batch.py R1 2` 返回的 `content_len > 30000` 时，改用两步：

1. **创建页（仅属性）**
   ```bash
   python3 notion-next-batch.py R1 1
   # 从 batch JSON 去掉 content，调用 notion-create-pages
   ```

2. **填充正文**
   ```bash
   # page_id 来自 create 返回值
   notion-update-page command=replace_content new_str=<全文>
   # 若超限，按 15KB 分块 insert_content position=end
   ```

记录：
```bash
python3 notion-record-push.py "<Source Path>"
```
