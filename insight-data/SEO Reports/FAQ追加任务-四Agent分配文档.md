# Lovart Blog FAQ 追加任务 — 四 Agent 分配文档

> 目标：为 TOP 149 优质 Blog 中 167 篇缺 FAQ 的文章追加 3-5 个 FAQ Q&A
> 任务类型：机械化追加——每篇 ~300 词，3-5 个主题相关 Q&A，追加到 body 末尾
> 分配方式：按 GSC 曝光轮询分配，4 个 Agent 各 ~42 篇

---

## 分配总览

| Agent | 数量 | 总曝光 | 高价值篇 |
|-------|:---:|:---:|------|
| **Agent A (Hermes)** | 42 篇 | 59,796 | flora-ai-review(35K), twitter-guide(2.9K), complete-guide×6 |
| **Agent B (OpenCode)** | 42 篇 | 48,404 | artlist-ai-review(27K), imagefx-review(6.9K), complete-guide×5 |
| **Agent C (Codex)** | 42 篇 | 36,349 | ai-art-copyright(18K), pixverse-review(4K), complete-guide×4 |
| **Agent D (Cursor)** | 41 篇 | 28,235 | complete-guide×8, picsart-review, ai-brand-kit |

---

## Sanity 连接代码（所有 Agent 共用）

```python
import json, urllib.request

with open('/Users/seveno/.config/sanity/config.json') as f:
    cfg = json.load(f)
token = cfg['authToken']

HEADERS = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
QUERY_URL = 'https://o11tm2qe.api.sanity.io/v2026-01-01/data/query/production'
MUTATE_URL = 'https://o11tm2qe.api.sanity.io/v2026-01-01/data/mutate/production'

def q(query_str):
    payload = json.dumps({'query': query_str}).encode()
    req = urllib.request.Request(QUERY_URL, data=payload, headers=HEADERS)
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())['result']

def mutate(mutations):
    payload = json.dumps({'mutations': mutations}).encode()
    req = urllib.request.Request(MUTATE_URL, data=payload, headers=HEADERS)
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())
```

## Slug 清单文件

每个 Agent 的完整 slug 列表已保存为 JSON 文件：
- Agent A: `/tmp/faq_agent_A_slugs.json`
- Agent B: `/tmp/faq_agent_B_slugs.json`
- Agent C: `/tmp/faq_agent_C_slugs.json`
- Agent D: `/tmp/faq_agent_D_slugs.json`

## 工作流（每篇）

### Step 1: 读取文章上下文
```python
slug = 'flora-ai-review'  # 从分配清单取
doc = q(f'*[_type=="blog" && language=="en" && slug.current=="{slug}"][0]{{_id, title, "text": pt::text(body)}}')

article_title = doc['title']
article_text = doc['text']
doc_id = doc['_id']
```

### Step 2: 根据文章主题生成 3-5 个 FAQ Q&A

**FAQ 规则**：
- 每个 Q&A 2-4 句话，有实质内容，不泛泛而谈
- 问题必须是搜索用户会真实搜索的长尾问题
- 答案必须包含具体信息（工具名、数字、对比）
- 如果文章是 Review 类型，FAQ 要覆盖该工具的竞品对比
- 如果文章是 Guide 类型，FAQ 要覆盖 "how to" 实操问题
- 如果文章是 Lovart 101，FAQ 要覆盖 Lovart 相关能力
- **Lovart 在 FAQ 中自然出现，但不强行推销**

**FAQ 模板参考**：

Review 类文章：
```
Q: Is [TOOL] better than [COMPETITOR]?
A: [TOOL] wins on [specific strength with data]. [COMPETITOR] wins on [specific strength]. For [use case], choose [recommendation].

Q: Can I use [TOOL] for [specific use case]?
A: [Yes/No/With caveats]. [Specific limitation or strength]. [Alternative if not suitable].
```

Guide/How-To 类文章：
```
Q: How long does it take to [achieve goal] with [method]?
A: [Specific timeframe with variables]. [Faster/slower depending on factors]. [Real-world example].

Q: What is the biggest mistake people make with [topic]?
A: [Specific mistake]. [Why it matters]. [How to avoid it].
```

### Step 3: 追加到 body 末尾

```python
# Fetch current body
doc = q(f'*[_type=="blog" && language=="en" && slug.current=="{slug}"][0]{{"body": body[]{{..., children[]{{..., marks[]}}}}}}')
body = doc['body']

# Check if FAQ already exists
has_faq = False
for block in body:
    if block.get('style') == 'h2':
        text = ''.join(c.get('text', '') for c in block.get('children', []))
        if text.strip().upper() == 'FAQ':
            has_faq = True
            break

if not has_faq:
    # Add FAQ heading
    h2_faq = {'_type': 'block', '_key': 'faq-h2', 'style': 'h2', 
              'children': [{'_type': 'span', 'text': 'FAQ'}], 'markDefs': []}
    body.append(h2_faq)
    
    # Add Q&A pairs (each Q is H3, each A is normal paragraph)
    faq_items = [
        ('Q: First question here?', 'A: First answer here.'),
        ('Q: Second question here?', 'A: Second answer here.'),
        ('Q: Third question here?', 'A: Third answer here.'),
    ]
    
    for q_text, a_text in faq_items:
        q_block = {'_type': 'block', '_key': 'faq-q' + str(len(body)), 'style': 'h3',
                   'children': [{'_type': 'span', 'text': q_text}], 'markDefs': []}
        a_block = {'_type': 'block', '_key': 'faq-a' + str(len(body)), 'style': 'normal',
                   'children': [{'_type': 'span', 'text': a_text}], 'markDefs': []}
        body.append(q_block)
        body.append(a_block)
    
    # Patch to Sanity
    mutate([{"patch": {"id": doc_id, "set": {"body": body}}}])
```

### Step 4: 验证
```bash
curl -s -o /dev/null -w "%{http_code}" "https://www.lovart.ai/blog/SLUG"
# Should return 200
```

## 质量要求

1. **FAQ 必须与文章主题相关**——读文章标题和正文前 500 词确认主题后再写 FAQ
2. **每个 Q&A 有实质内容**——不说 "it depends"，给出具体建议
3. **包含至少一个具体工具或数字**——"Dream Machine"、"$29/month"、"2.4x regeneration rate"
4. **Lovart 自然提及**——FAQ 中 1-2 个问题可涉及 Lovart 对比，但不强行推销
5. **不重复已有内容**——读文章确认 FAQ 问题没有被正文回答过

## 禁止行为

- 不修改已有 body 内容——只在末尾追加 FAQ
- 不删除任何现有 block
- 不修改 title、seo、slug 等字段
- 不添加 IMAGE PLACEHOLDER
- 不使用 AI-slop 词汇（unlock, revolutionize, seamless, empower, game-changer, cutting-edge, leverage）

## 进度追踪

完成每篇后输出：`[N/42] SLUG — FAQ added (3 Q&As)`

## 完成标准

全部 42/41 篇 FAQ 追加完毕，HTTP 200 验证通过，IndexNow 提交。
