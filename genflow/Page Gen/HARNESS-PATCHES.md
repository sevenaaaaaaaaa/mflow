# Harness 补丁（iCloud 解锁后应用）

## `lovart-content-creation-orchestrator/references/page-routing.md`

**Source Files 表追加：**

```
| `1-3 Content Gen/Page Gen/Pages/Solution/solution-storylines-v2.json` | Solution v2 SSOT (12 storylines: P1–P6 + I1–I6). |
| `1-3 Content Gen/Page Gen/Pages/Solution/lovart-solution-page.md` | Solution page generation skill. |
```

**Storyline Routing 替换 Solution 行：**

```
| Solution page (persona) | `solution-p-marketing` … `solution-p-individual` (P1–P6) | Team, agency, founder, enterprise, freelancer narratives. |
| Solution page (industry) | `solution-i-ecommerce` … `solution-i-creator` (I1–I6) | Ecommerce, SaaS, local, wellness, mission, creator — industry signals beat persona. |
```

**SERP 表：** `S1-S3` → `solution-i-*` (I1–I6)

## `lovart-page-serp-writer/SKILL.md`

- `Solution: S1-S3` → `Solution: solution-p-* (P1–P6) + solution-i-* (I1–I6)`
- Industry example: `S2, S3` → 六个 `solution-i-*` ID

## 新增 Skill 镜像

```bash
cp "Pages/Solution/lovart-solution-page.md" "1-5 Harness/Skills/lovart-solution-page.md"
```
