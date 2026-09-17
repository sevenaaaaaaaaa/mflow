# MFlow Pay（支付链接 · 加密收款 · 发卡 · 兑换券）

> 定位：内容闭环的**最后一段变现**——内容 → 触达 → 成交交付。
> 铁律：不代持资金（收款地址用户自备）；交付只在「已确认到账」后发生；发布/资金类动作归管理员。

## 能力

| 能力 | 说明 |
|------|------|
| 临时支付链接 | 指定商品/数量/兑换码/有效期（默认 60 分钟）→ 生成不可枚举 token 链接 `https://nownexts.com/mflow/pay/{token}`，可复制/直接发买家 |
| 加密收款 | USDT-TRC20（**链上自动核验**）/ USDT-ERC20 / BTC（手工确认）。TRC20 用 TronGrid 公开端点核验：金额 + 收款地址 + 时间窗三匹配 |
| 发卡系统 | 卡密池按商品导入（批量/去重），订单确认到账后**自动发卡**；库存不足挂 `paid_no_stock` 不丢单，补卡后一键重发 |
| 兑换券 | 三种类型：抵扣金额 / 折扣 % / 免费兑换（0 元单直接发卡）。支持适用商品白名单、次数上限、过期日 |
| 外部支付回调 | `POST /api/pay/webhook/{secret}`——Stripe / OpenFlow 等外部支付确认后调用即交付 |
| 外部系统只读 | 机器 token（`X-MFlow-Token`）可读订单/商品/统计（GET-only） |

## 订单状态机

```
pending（待支付，含过期时间）
  ├─ confirmed → paid → delivered（自动发卡）
  │              └─ paid_no_stock（补卡后 redeliver）
  ├─ expired（超时清扫，每分钟）
  └─ cancelled（管理员取消）
```

## 买家流程（公开收银台 /pay/{token}）

1. 打开链接 → 看商品/金额/倒计时
2. 转 USDT(TRC20) 到指定地址（复制按钮）
3. 粘贴交易哈希 → 提交核验
4. 核验通过 → 页面直接显示卡密/兑换码（可复制）

卖家侧（工作台「支付 · 发卡」页）：商品管理 / 卡密池 / 订单（链上核验·手动确认·取消·重发）/ 兑换券 / 收款配置。

## 配置（工作台 → 支付 · 发卡 → 收款配置）

| 项 | 说明 |
|----|------|
| USDT-TRC20 地址 | 填了即开启自动核验（每 60s 巡检 pending 单 + 提交哈希即时核验） |
| USDT-ERC20 / BTC | 仅展示给买家，到账由管理员手工确认 |
| webhook secret | 外部支付回调凭证（`POST /api/pay/webhook/<secret>`，body: `{order_id|token, amount, tx_hash, provider}`） |
| 链接有效期 | 默认 60 分钟 |

## API（管理端，admin）

- `POST /api/pay/product/save|delete`、`POST /api/pay/cards/import|clear`
- `POST /api/pay/link/create`（= 建单+出链接）
- `POST /api/pay/order/confirm|redeliver|cancel`、`POST /api/pay/verify`（链上核验）
- `POST /api/pay/voucher/save|delete`、`POST /api/pay/config/save`
- `GET /api/pay/overview|products|orders|cards|vouchers`

公开（无鉴权，token 即凭据）：`GET /pay/{token}`、`GET /api/pay/order/{token}`、`POST /api/pay/claim`、`POST /api/pay/webhook/{secret}`。

## 安全设计

- 订单 token `secrets.token_urlsafe(18)`，不可枚举；卡密仅在核验/确认后出现，且只回给持 token 的买家
- 公开端点不能改单（confirm/verify 等写操作 401）；机器 token 只读（POST 403）
- 资金动作全部落 `run/approvals.log` 审计
- 数据文件 `run/pay/*.json`（600 目录，git-ignore，不入库）

## 边界（诚实）

- **不代持资金**：收款地址是用户自己的；MFlow 只做核验与交付。
- ERC20/BTC 目前**无链上自动核验**（需 Etherscan/BSCScan API Key，未接入）→ 手工确认。
- 首次真实收款前，请先用小额真实转账验证一次 TRC20 核验链路。
