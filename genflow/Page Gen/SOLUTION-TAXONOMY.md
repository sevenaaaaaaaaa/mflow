# Solution 双轴故事线体系（v2）

> SSOT：`solution-storylines-v2.json`（本目录）  
> 待合并替换：`Refresh-Page/solution-storylines.json`（旧版 6 条混合命名）

---

## 一、为什么要双轴

Solution 页同时回答两个问题：

1. **谁买**（人群 / 组织角色）— 采购主体、编制结构、工作方式  
2. **为谁做**（行业 / 垂直场景）— 业务对象、素材类型、转化路径

旧版 6 条里 **4 条偏人群、2 条偏行业**，且：

- 创业公司被塞进「营销团队」线，和创始人叙事混在一起  
- 小商家 Hub 被标成「个体户」线，实际应是**本地生活行业**  
- 健身 Hub 被标成 solo，实际应是**健康美业行业**  
- 缺 SaaS、创作者、企业内部设计团队等常见选题

v2 改为 **6 + 6 平衡**，并规定：**行业信号优先于人群信号**。

---

## 二、人群轴（P1–P6）

| ID | 编号 | 适用 | 叙事 | JSON 范例 |
|----|------|------|------|-----------|
| `solution-p-marketing` | P1 | 市场、增长、内容运营团队 | 渠道扩产、分布式生产 | ✅ marketing-teams |
| `solution-p-founder` | P2 | 创业公司创始人、产品负责人 | 0→1 品牌与 GTM、缺设计编制 | 📝 startups.md |
| `solution-p-design` | P3 | 企业内部设计 / 品牌团队 | 品牌系统、业务方自助、产能放大 | ⬜ 待写 |
| `solution-p-agency` | P4 | 代理商、创意工作室 | 多客户、pitch、利润率 | ✅ agencies |
| `solution-p-enterprise` | P5 | 大企业、全球品牌组织 | 治理、合规、多区域 | 📝 enterprise.md |
| `solution-p-individual` | P6 | 自由职业、顾问、个体经营者 | 个人交付、低门槛 | 📝 freelancers.md |

---

## 三、行业轴（I1–I6）

| ID | 编号 | 适用 | 叙事 | JSON 范例 |
|----|------|------|------|-----------|
| `solution-i-ecommerce` | I1 | 电商、DTC、Shopify、平台卖家 | 买家旅程、SKU、全漏斗测试 | ✅ shopify |
| `solution-i-saas` | I2 | B2B SaaS、科技产品、开发者工具 | PLG、产品发布、销售赋能 | ✅ saas |
| `solution-i-local` | I3 | 餐饮、本地门店、房产中介、服务业 | 到店引流、套餐促销、口碑 | ✅ small-business-hub |
| `solution-i-wellness` | I4 | 健身、瑜伽、美业、健康教练 | 会员转化、前后对比、社群 | ✅ fitness-wellness-hub |
| `solution-i-mission` | I5 | 非营利、NGO、教育机构、社区组织 | 筹款、影响力、志愿者 | ✅ nonprofits |
| `solution-i-creator` | I6 | 创作者、播客、Newsletter、个人 IP | 多平台栏目、商单、粉丝增长 | ✅ creators |

图例：✅ 已有 JSON 范例 · 📝 有 Markdown 待转 JSON · ⬜ 待规划

---

## 四、选型优先级（写稿前必做）

```
1. 标题/slug 是否点名行业？（fitness / nonprofit / shopify / restaurant）
   → 是：行业轴（I*），即使读者是「小团队」
2. 正文核心痛点是否行业特有？（SKU、筹款、课程包、探店）
   → 是：行业轴
3. 否则看采购主体：
   - 多客户外包 → P4 agency
   - 全球品牌采购 → P5 enterprise
   - 内部设计部 → P3 design
   - 创始人无设计岗 → P2 founder
   - 个人接单 → P6 individual
   - 市场部扩产 → P1 marketing（默认）
```

**反例纠正：**

| 旧映射 | 问题 | v2 正确 |
|--------|------|---------|
| small-business-hub → solo | 小商家是行业场景 | `solution-i-local` |
| fitness-wellness-hub → solo | 健身是垂直行业 | `solution-i-wellness` |
| startups → marketing-team | 创始人叙事不同 | `solution-p-founder` |

---

## 五、旧 ID 别名（兼容）

| 旧 ID | 新 ID |
|-------|-------|
| `solution-team` | `solution-p-marketing` |
| `solution-ecommerce` | `solution-i-ecommerce` |
| `solution-agency` | `solution-p-agency` |
| `solution-enterprise` | `solution-p-enterprise` |
| `solution-solo` | `solution-p-individual` |
| `solution-mission` | `solution-i-mission` |

---

## 六、覆盖缺口（建议补范例顺序）

**行业轴**（当前 **6/6** 有 JSON）：

- ✅ ecommerce · saas · local · wellness · mission · creator

**人群轴：**

1. `solution-p-founder` — startups Markdown 已有  
2. `solution-p-individual` — freelancers Markdown 已有  
3. `solution-p-enterprise` — enterprise Markdown 已有  
4. `solution-p-design` — 待新建 Markdown  

---

## 七、模块差异速查

| 故事线 | 首屏 | 对比 | 证言 | 特色段 |
|--------|------|------|------|--------|
| P1 marketing | cinematic | table | testimonial | stacked |
| P2 founder | journey | table | testimonial | 横版步骤 |
| P3 design | cinematic | table | review-3col | canvas-wall |
| P4 agency | mosaic | table | review-4col | canvas-wall |
| P5 enterprise | cinematic + bento-6 | table | review-3col | showcase-horizontal |
| P6 individual | split | before-after | testimonial | 横版步骤 |
| I1 ecommerce | journey | table | review-3col | stacked |
| I2 saas | cinematic | table | review-3col | stacked |
| I3 local | journey | table | testimonial | 横版步骤 |
| I4 wellness | cinematic | before-after | testimonial | stacked |
| I5 mission | journey | table | testimonial | stacked |
| I6 creator | gallery | table | testimonial | showcase-horizontal |

完整 12 段序列见 `solution-storylines-v2.json`。
