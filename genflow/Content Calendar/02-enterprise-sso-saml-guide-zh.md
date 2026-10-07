---
title: "面向企业团队的 Lovart SSO 与 SAML 集成指南"
date: 2027-06-03
category: 企业
tags: [lovart sso, saml 集成, 企业设计, 单点登录, 身份管理, 安全]
keywords: [lovart sso, saml 集成, 企业设计工具 sso, 单点登录设计, 身份提供商集成]
description: "一份全面的技术指南，用于为 Lovart 企业账户配置 SSO 和 SAML 身份验证——涵盖身份提供商设置、用户预配置、角色映射、安全策略以及常见故障排除场景。"
slug: sso-saml-integration-guide-enterprise-2027
featured_image: /images/lovart-sso-saml-guide.jpg
canonical_url: https://lovart.ai/blog/sso-saml-integration-guide-enterprise
language: zh
---

# 面向企业团队的 Lovart SSO 与 SAML 集成指南

[图片 1 占位符 — 用户场景]

当创意工具无法与组织的身份和访问管理基础设施集成时，企业对这些工具的采用就会遇到硬性障碍。IT 安全团队对此没有商量余地：如果一个 SaaS 工具无法通过公司的单点登录（SSO）提供商进行身份验证，它就不会被部署。无论产品多么有吸引力，无论设计团队多么热情。没有 SSO，就没有合作。

Lovart 的企业版计划（每个席位每月 149 美元）通过 SAML 2.0 和 OpenID Connect（OIDC）提供完整的 SSO 支持，并包含即时（JIT）用户预配置、基于角色的访问控制映射以及会话管理策略。本指南涵盖了完整的集成过程——从身份提供商配置到用户生命周期管理，再到常见的故障排除场景。

## 支持的身份提供商

[图片 2 占位符 — 概念图]

Lovart 支持与任何实现 SAML 2.0 标准的身份提供商（IdP）进行集成。我们已经验证了与以下提供商的集成：

| 身份提供商 | 配置复杂度 | 备注 |
|-------------------|-------------------------|-------|
| **Okta** | 低 | Okta 集成网络中的预构建 Lovart 应用 |
| **Microsoft Entra ID (Azure AD)** | 低 | 预构建的 Lovart 图库应用 |
| **Google Workspace** | 低 | SAML 应用配置，如下所述 |
| **OneLogin** | 低 | 预构建的应用目录条目 |
| **Ping Identity / PingOne** | 中 | 需要手动配置 SAML |
| **JumpCloud** | 中 | 需要手动配置 SAML |
| **Auth0** | 低 | 灵活的 SAML/OIDC，文档完善 |
| **任何符合 SAML 2.0 的 IdP** | 中 | 通用 SAML 配置如下所述 |

## SAML 配置概述

集成遵循标准的 SAML 2.0 服务提供商（SP）发起流程：

1. 用户导航到 Lovart（app.lovart.ai）或在其 IdP 仪表板中点击 Lovart 磁贴。
2. Lovart 将未认证的用户重定向到配置的 IdP。
3. IdP 对用户进行身份验证（或识别现有会话）并生成 SAML 断言。
4. 该断言通过 POST 方式发送回 Lovart 的断言消费者服务（ACS）端点。
5. Lovart 验证断言，将 SAML 属性映射到 Lovart 用户属性，并创建或更新用户账户（JIT 预配置）。
6. 用户被重定向到 Lovart 仪表板，并拥有一个活动会话。

### 必需的 SAML 配置参数

在 IdP 中将 Lovart 配置为服务提供商时，请使用以下值：

| 参数 | 值 |
|-----------|-------|
| **实体 ID / 颁发者** | `https://app.lovart.ai/saml/metadata` |
| **ACS URL** | `https://app.lovart.ai/saml/acs` |
| **单点注销 URL** | `https://app.lovart.ai/saml/slo` |
| **名称 ID 格式** | `urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress` |
| **签名算法** | RSA-SHA256 |
| **签名断言** | 必需 |
| **签名响应** | 推荐 |
| **加密断言** | 可选（支持） |

### 必需的 SAML 属性

Lovart 期望在 SAML 断言中包含以下属性。标记为 (*) 的属性对于 JIT 预配置是必需的：

| SAML 属性名称 | Lovart 属性 | 必需 | 备注 |
|---------------------|-----------------|----------|-------|
| `email` | 用户邮箱 | * | 必须匹配您的企业账户声明的域名 |
| `firstName` | 名字 | * | 在 Lovart UI 中显示 |
| `lastName` | 姓氏 | * | 在 Lovart UI 中显示 |
| `role` | Lovart 角色 | | 映射到 Lovart 角色（admin, manager, designer, viewer） |
| `department` | 团队/部门 | | 用于自动团队分配 |
| `title` | 职位 | | 在用户个人资料中显示 |

### 角色映射

`role` SAML 属性映射到 Lovart 的权限级别：

| IdP 角色值 | Lovart 角色 | 权限 |
|----------------|-------------|-------------|
| `admin` | 管理员 | 完全账户控制、计费、SSO 配置、用户管理 |
| `manager` | 团队经理 | 模板发布、品牌工具包治理、资产审批、所分配团队的用户管理 |
| `designer` | 设计师 | 完整的设计能力、模板定制、品牌工具包使用 |
| `viewer` | 查看者 | 查看和评论资产，无设计能力 |

如果未提供 `role` 属性，用户默认为 `designer`。如果发送了无法识别的角色值，用户将被预配置为 `viewer`（安全默认值）。

## 分步设置：Okta

[图片 3 占位符 — 真实 UI 截图]

1. **在 Okta 管理控制台中：** 导航到 Applications > Browse App Catalog。搜索“Lovart”。选择 Lovart 应用。点击“Add Integration”。
2. **配置 Lovart 应用：** 在 Sign-On 选项卡上，确认已选择 SAML 2.0。记下身份提供商元数据 URL 或下载元数据 XML——您将在 Lovart 中用到它。
3. **在 Lovart 中：** 导航到 Account Settings > Security > SSO Configuration。从 IdP 下拉菜单中选择“Okta”。上传元数据 XML 或粘贴元数据 URL。点击“Test Connection”。Lovart 会验证元数据并报告任何配置问题。
4. **属性映射：** 验证默认属性映射（email, firstName, lastName, role）是否与您的 Okta 用户配置文件属性匹配。如果您的组织使用不同的属性名称，请进行调整。
5. **分配用户：** 在 Okta 中，将用户或组分配给 Lovart 应用程序。用户将在首次登录时在 Lovart 中预配置（JIT 预配置）。
6. **测试：** 让一个测试用户通过 Okta 仪表板或导航到 app.lovart.ai 登录 Lovart。用户应被重定向到 Okta 进行身份验证，然后重定向回 Lovart，并拥有一个活动会话和正确的角色。

## 分步设置：Microsoft Entra ID (Azure AD)

1. **在 Azure 门户中：** 导航到 Entra ID > Enterprise Applications > New Application > Browse Gallery。搜索“Lovart”。选择 Lovart 图库应用。点击“Create”。
2. **配置 SAML：** 在 Lovart 应用程序页面，导航到 Single Sign-On > SAML。点击 Basic SAML Configuration 上的“Edit”。验证实体 ID 和回复 URL 是否与上表中的值匹配。
3. **下载元数据：** 在 SAML 配置页面上，下载联合元数据 XML。
4. **在 Lovart 中：** 导航到 Account Settings > Security > SSO Configuration。从 IdP 下拉菜单中选择“Microsoft Entra ID”。上传元数据 XML。点击“Test Connection”。
5. **属性与声明：** 在 Azure 中，配置必需的属性（email, firstName, lastName, role）。默认情况下，Azure 将 `user.mail` 映射到 email，`user.givenname` 映射到 firstName，`user.surname` 映射到 lastName。如果使用基于角色的访问控制，请为 `role` 添加自定义声明。
6. **分配用户：** 在 Azure 中，将用户或组分配给 Lovart 企业应用程序。
7. **测试：** 使用测试用户登录以验证完整流程。

## 分步设置：Google Workspace

1. **在 Google 管理控制台中：** 导航到 Apps > Web and Mobile Apps > Add App > Add Custom SAML App。
2. **配置自定义 SAML 应用：** 输入“Lovart”作为应用名称。下载 IdP 元数据。输入上表中的 ACS URL 和实体 ID。将名称 ID 格式设置为 EMAIL。映射必需的属性（email → Primary Email, firstName → First Name, lastName → Last Name）。
3. **在 Lovart 中：** 导航到 Account Settings > Security > SSO Configuration。从 IdP ��拉��单中选择“Google Workspace”。上传 IdP 元数据。点击“Test Connection”。
4. **启用应用：** 在 Google 管理中，将 Lovart 应用设置为“对所有人开启”或“对部分组织开启”（建议：从测试组开始）。
5. **测试：** 使用测试用户验证登录流程。

## 即时（JIT）预配置

Lovart 默认对 SAML 认证的用户使用 JIT 预配置。当用户首次通过 SAML 登录时：

1. **域名验证：** 用户的电子邮件域名必须匹配您的 Lovart 企业账户声明的域名。未声明域名的用户将被拒绝（这可以防止未经授权的用户被预配置）。
2. **账户创建：** 使用 SAML 断言中的属性创建一个 Lovart 用户账户。
3. **许可证分配：** 该用户消耗一个企业版席位许可证。如果您的账户没有可用席位，用户将收到一条错误消息，并被引导联系其 Lovart 管理员。
4. **团队分配：** 如果提供了 `department` 属性，该用户会自动添加到 Lovart 中相应的团队。如果该团队不存在，则会创建它。
5. **欢迎：** 用户以其预配置的角色和权限进入 Lovart 仪表板。

**席位管理：** 企业管理员可以在计费页面上监控席位使用情况。超过 90 天未登录的用户可以被取消预配置（释放其席位），而无需删除其资产——他们的设计仍可供其团队访问。重新激活将恢复其账户并重新消耗一个席位。

## 安全策略

SSO 是企业安全的基础，但并非唯一的安全层。Lovart 企业版支持额外的安全策略：

- **会话持续时间：** 可配置为 1 小时到 30 天。默认值：8 小时。
- **IdP 发起的会话强制：** 要求所有会话都源自 IdP，从而为企业用户禁用直接 Lovart 登录。这确保了 IdP 的会话策略（MFA、设备信任、基于位置的访问）始终得到执行。
- **IP 白名单：** 将访问限制在特定的 IP 范围内。即使拥有有效的 SAML 断言，允许范围之外的用户也会被阻止。可针对每个团队或整个账户进行配置。
- **审计日志：** 所有登录事件和 SSO 配置更改都会被记录，并可供企业管理员访问。日志保留 12 个月。

## 常见故障排除场景

### “SAML 响应验证失败 — 签名不匹配”

**原因：** IdP 元数据中的证书与用于签署 SAML 断言的证书不匹配。
**解决方法：** 在您的 IdP 中，验证签名证书。如果证书已轮换，请在 Lovart 中更新元数据（Account Settings > Security > SSO Configuration > Update Metadata）。

### “未找到用户 — 域名未声明”

**原因：** 用户 SAML 断言中的电子邮件域名尚未被您的 Lovart 企业账户声明。
**解决方法：** 在 Lovart 中，导航到 Account Settings > Domains。添加并验证域名。需要 DNS TXT 记录验证。验证后，具有该电子邮件域名的用户将自动预配置。

### “没有可用席位”

**原因：** 您的企业版计划已达到许可席位限制。
**解决方法：** 导航到 Account Settings > Billing 以添加席位，或取消预配置非活跃用户以释放席位。席位更改会立即生效。

### “角色无法识别”

**原因：** SAML 断言中的 `role` 属性包含的值与 Lovart 预期的角色值不匹配。
**解决方法：** 验证您的 IdP 中的角色映射。有效值（不区分大小写）：admin, manager, designer, viewer。如果问题仍然存在，请检查 SAML 断言中是否存在尾随空格或编码问题。

### “无限重定向循环”

**原因：** 通常是 IdP 和 Lovart 之间的 cookie 或会话冲突。
**解决方法：** 清除浏览器 cookie。验证您的 IdP 是否未配置为对每个 SAML 请求都要求重新认证（这会在 Lovart 重定向到 IdP 且 IdP 立即重定向回来时形成循环）。检查 IdP 和 Lovart 中的会话持续时间是否兼容。

## 获取支持

[图片 4 占位符 — 品牌行动号召]

企业客户可以获得专门的 SSO 集成支持：
- **文档：** 完整的技术文档，请访问 docs.lovart.ai/sso
- **支持工单：** ，主题行包含“SSO”以获得优先处理
- **集成通话：** 企业客户可以安排与 Lovart 解决方案工程师进行 30 分钟的集成通话

---

*Lovart 企业版 SSO 功能在企业版计划（每个席位每月 149 美元）中可用。SSO 配置需要在 Lovart 中拥有管理员角色，并在您的身份提供商中拥有适当的权限。在向整个组织推广之前，请使用测试用户测试您的 SSO 配置。*

### 附录：图片提示

**图片 1 — 用户场景**：
一位专业且平易近人的人坐在办公桌前，看着电脑屏幕，试图进行设计时略显沮丧——温暖的自然光线，坦率的纪实风格

**图片 2 — 概念图**：
手绘草图，展示使用 AI 进行设计的分步工作流程——网格纸上的干净线条艺术，箭头连接每一步，极简风格

**图片 3 — 真实 UI 截图**：
[需要真实截图：Lovart ChatCanvas 界面，展示本文所述的关键功能——干净的 UI，不杂乱，并显示可见结果]

**图片 4 — 品牌行动号召**：
Lovart AI 设计代理的专业品牌视觉——展示面向企业团队的 SSO 与 SAML 集成指南中描述的最终精美设计结果——现代、鼓舞人心、电影级灯光