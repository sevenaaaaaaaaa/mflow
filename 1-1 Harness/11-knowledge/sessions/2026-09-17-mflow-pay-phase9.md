---
type: session-log
session_date: 2026-09-17
session_slug: mflow-pay-phase9
status: ready
---

# Session Log — Phase 9 · MFlow Pay（支付链接 / 加密收款 / 发卡 / 兑换券）

## 背景
用户提出"感觉能做临时支付链接、加密支付、发卡系统、兑换券机制，你试试"——定位上这是内容闭环的最后一段（触达→成交交付）。

## 交付（服务器 e2e 全过）
1. **临时支付链接**：`pay_create_order` → 商品×数量×券×TTL → `secrets.token_urlsafe(18)` 不可枚举 token → `https://nownexts.com/mflow/pay/{token}`；过期清扫（后台每分钟）
2. **加密收款 + 链上核验**：TRC20 走 TronGrid 公开端点（无 Key）三匹配（合约=USDT、收款地址、金额≥应付、时间窗≥建单-10min）→ 确认即交付；ERC20/BTC 手工确认；外部 webhook `POST /api/pay/webhook/{secret}`
3. **发卡**：卡密池 import（去重/上限5000）→ 确认后按序发卡 → 库存不足 `paid_no_stock`（notify 通知 + 补卡重发）
4. **兑换券**：amount / percent / free（0 元单直接发卡）+ products 白名单 + max_uses + expires
5. **公开收银台 pay.html**：商品/金额/倒计时/收款地址复制/提交 tx/轮询状态/出码复制
6. **工作台页**「支付 · 发卡」：概览 stats + 出链接 + 商品 + 卡密池 + 订单（链上核验/手动确认/取消/重发）+ 兑换券 + 收款配置
7. **机器只读联动**：X-MFlow-Token 可读 pay 订单（供 OpenFlow）

## e2e（真实域名）
商品建→导 3 卡→建 GEOFREE 券→出链接(pending/倒计时/无地址诚实提示)→公开页 200→公开状态无鉴权→手动确认→自动发卡 GEO-DEMO-0001→买家页可见→免费券 0 元直发 GEO-DEMO-0002→机器 token 读订单→未配地址核验清晰报错→未登录 confirm 401→假 webhook 403。

## 踩坑（重要）
- **重复读 body 导致挂死**：console 的 do_POST 已在鉴权区预读 `body = self._body()`；我在 pay 路由里又调了一次 → `BufferedReader.read(Content-Length)` 阻塞等满字节 → 请求挂到客户端超时，随后 EOF 才继续并创建垃圾商品。现象极具迷惑性（副作用已发生但无响应 + BrokenPipe 栈）。修：pay 路由改用预读 body（删 12 处重复读取）。**教训：同一个 Handler 里 body 只能读一次；新增路由前先看有没有预读。**
- 编辑大块路由时两次括号不配对（_send 字典尾）——ast/ node 双检逮住

## 待用户
- 配置收款钱包地址：USDT-TRC20 填了才开自动核验；ERC20/BTC 目前手工确认（需 Etherscan Key 才能自动）
- 首次真实收款建议小额跑通一次 TRC20 核验
- 演示数据已在线上：商品 geo-audit、券 GEOFREE（剩 1 次）、卡密剩 1 张、2 个已交付订单可作样例
