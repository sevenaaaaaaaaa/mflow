

从 `110005` chunk（`util-report` 模块）找到了埋点上报的 payload 拼接逻辑：

```javascript
let f = getCookieWebid();    // ← 读 webid cookie → 用作 cid
let p = getUserUuid() || ""; // ← 读 useruuid cookie → 用作 uuid

let payload = {
    tz:       timezone,
    langs:    navigator.languages,
    uuid:     p,              // useruuid cookie
    cid:      f,              // webid cookie ← 这就是你说的 cid
    ct:       Date.now(),
    region:   "oversea" | "cn",
    pageUrl:  location.href,
    ua:       navigator.userAgent,
    referer:  document.referrer,
    ...eventData
};

// 发到
reportData: "/api/www/log/acceptor/f"
```

### 当前各 cookie 用途

| Cookie | 用途 | 来源 |
|--------|------|------|
| `webid` | 上报 payload 的 `cid` 字段，Statsig 的 `stableID` | 服务端 set-cookie（10年） |
| `useruuid` | 上报 payload 的 `uuid` 字段 | 服务端 set-cookie |
| `usertoken` | JWT 鉴权（7 天） | 登录后 set |
| `refreshToken` | JWT 刷新（90 天） | 登录后 set |

`webid` 的值格式是 `1784299693209zuatenbk`（时间戳 + 随机串），这确实是**服务端根据规则生成的**。你说得对，它不是 GA4 的 `_ga`，是你们自己的 cid 体系。

---

## 跨子域打通方案：两个 cookie 都要改 domain

需要打通的不只是 `webid`，实际上 **两个 cookie 都需要**：

### 服务端改动（Next.js）

```javascript
// webid — 上报 cid + Statsig stableID
response.cookies.set('webid', value, {
    domain: '.lovart.ai',    // ← 从默认当前域改为泛域
    path: '/',
    maxAge: 315360000,       // 10 年，保持不变
    secure: true,
    sameSite: 'none',
});

// useruuid — 上报 uuid
response.cookies.set('useruuid', value, {
    domain: '.lovart.ai',    // ← 新增
    path: '/',
    secure: true,
    sameSite: 'none',
});
```

### 为什么要改 useruuid 而不只是 webid

`useruuid` 和 `webid` 在埋点 payload 里是**两个独立字段**，各自有各自的含义。后端 `/api/www/log/acceptor/f` 接收后很可能用这对 `(cid, uuid)` 做用户去重/关联。如果只有 `webid` 打通了但 `useruuid` 没有，数据到了后端会产生不一致的关联关系。

### WordPress 端需要做什么

**零改动。** 只要 cookie domain 改为 `.lovart.ai`，浏览器访问 `blogs.lovart.ai` 时会自动携带这两个 cookie。WP 端只需要：
1. 注入 GTM `GTM-WX5X6NS2`（这个是前面讨论过的）
2. 注入一段上报 JS，从 cookie 读出 webid/useruuid，构造同样的 payload 发到 `/api/www/log/acceptor/f`

上报 JS 大致这样：

```javascript
function getCookie(name) {
    var m = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
    return m ? decodeURIComponent(m[1]) : '';
}

var payload = {
    tz: Intl.DateTimeFormat().resolvedOptions().timeZone,
    langs: navigator.languages,
    uuid: getCookie('useruuid'),
    cid: getCookie('webid'),
    ct: Date.now(),
    region: 'oversea',  // 或根据博客服务器判断
    pageUrl: location.href,
    ua: navigator.userAgent,
    referer: document.referrer
};

navigator.sendBeacon('https://www.lovart.ai/api/www/log/acceptor/f', JSON.stringify(payload));
```

### 还有一个问题：CORS

`/api/www/log/acceptor/f` 在 `www.lovart.ai` 上。从 `blogs.lovart.ai` 发 `fetch` 或 `sendBeacon` 过去是跨域请求。需要确保该接口响应头包含：

```
Access-Control-Allow-Origin: https://blogs.lovart.ai
Access-Control-Allow-Credentials: true
```

或者如果是 `sendBeacon` + `no-cors` 模式，后端需要能接收简单跨域请求。

---

## 总结

你要打通的是两个 cookie（`webid` + `useruuid`），改法是在 Next.js 服务端给它们加 `Domain=.lovart.ai`。然后 WP 端加一段 JS 模仿同样的 payload 格式发到 `/api/www/log/acceptor/f`，再加上 CORS 白名单。