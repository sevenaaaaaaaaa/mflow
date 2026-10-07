问题的本质是：不同子域下 `_ga` cookie 是隔离的，GA4 会生成两个不同的 client ID，同一个用户被计为两个独立访客。

**打通方案：GA4 跨域追踪（Cross-Domain Measurement）**

核心原理：用户在 `blogs` ↔ `www` 之间跳转时，URL 自动附加 `_gl` 参数，目标页的 GA4 tag 从中读取原始 CID 并复用，从而串联为同一 session。

---

## 具体操作（3 步，全在 GTM 后台完成）

### 第 1 步：GA4 Configuration Tag 配置跨域

GTM 后台 → 找到现有的 **GA4 Configuration Tag** → 编辑：

**Fields to Set：**
```
cookie_domain = auto
```

**Tag Configuration → Configure Cross-Domain Tracking：**
```
Enter domain conditions:
  lovart.ai
  blogs.lovart.ai
```

**More Settings → Cross-Domain Tracking → Auto Link Domains：**
```
Auto Link Domains: Yes
  lovart.ai
  blogs.lovart.ai
```

`cookie_domain: auto` 让 GA4 自动选择能覆盖的最高域级（`.lovart.ai`），而不是绑死在 `www.lovart.ai`。

### 第 2 步：GA4 Admin 里添加引荐排除

GA4 Admin → Data Streams → 你的 web stream → **Configure tag settings** → **List unwanted referrals**：

添加 `blogs.lovart.ai`

不加的话，用户从 blogs 跳到 www 会被计为一个新的 referral session（来源 = `blogs.lovart.ai`），虽然 CID 打通了但 session 仍会断开。

### 第 3 步：确保 blogs.lovart.ai 加载同一个 GTM 容器

这是前提——前面讨论过的，在 WordPress 注入 `GTM-WX5X6NS2`。配置好 GTM 容器后，上面的跨域配置对所有加载该容器的域名同时生效，不需要分别在两个域各配一次。

---

## 验证方法

部署后用浏览器 DevTools 验证：

1. 打开 `blogs.lovart.ai` → Application → Cookies → 记下 `_ga` 的值（`GA1.2.xxxxx.xxxxx`）
2. 点击页面中任意指向 `www.lovart.ai` 的链接
3. 观察跳转后的 URL：应该自动附加了 `?_gl=1*...` 参数
4. 查看 `www.lovart.ai` 的 `_ga` cookie——值应与第 1 步相同
5. 如果一致 → 打通成功；如果不一致 → 检查第 1 步中 cookie_domain 是否设为 `auto`（不要设成具体域名）

---

总结一下完整链路：

```
blogs.lovart.ai (WP + GTM-WX5X6NS2 + GA4 tag + cookie_domain=auto)
        │
        │  用户点击链接 → URL 自动加 _gl 参数
        ▼
www.lovart.ai (Next.js + GTM-WX5X6NS2 + GA4 tag + cookie_domain=auto)
        │
        │  GA4 从 _gl 参数读取原始 CID，复用同一个 _ga cookie
        ▼
    同一用户、同一 session → CID 打通 ✓
```