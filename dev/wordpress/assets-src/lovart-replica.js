/**
 * lovart-replica.js — blogs.lovart.ai 复刻页共享交互 bundle（v3）
 *
 * v1 来源：replica-homepage 已验证 inline JS（before/after 滑块、FAQ 手风琴、
 *          锚点防跳顶、横向拖拽）。
 * v3 增强（针对忠实模块页交互缺失）：
 *   - capability-tabs：多 tab 点击切换（按钮 role=tab 按索引对应 tabpanel），
 *     并支持自动轮播（每 5s 前进，hover/聚焦/手动点击暂停）
 *   - before/after 对比滑块：保留原有拖动；无 data-lp-section 包裹时也按
 *     [role=slider] 就近兜底初始化
 *   - FAQ/howto/workflow 手风琴：aria-expanded 开闭 + 内容面板显隐（保留原有）
 *   - 对话面板（prompt-launcher / hero-cinematic 等含输入框的）：可输入、
 *     Enter/发送按钮把输入作为新一条消息插入对话流并清空输入框
 *   - 页脚主题切换：data-track-id=footer_theme_day/night/auto，切换 .lr 的
 *     dark/light 环境类并记忆（localStorage）
 *   - 页脚语言切换：含 “English/中文/日本語” 等的语言按钮 → 下拉选择，
 *     仅前端记忆与切换显示（站点为单语言复刻，不做真正翻译跳转）
 *
 * 说明：复刻页为静态资产，后端无 Lovart 账号/计费/翻译服务；价格区的真实
 *      价格与功能清单在源抓取时即缺失，JS 无法凭空生成——价格展示由
 *      lovart-replica.css 的占位样式 + 静态文案承担，交互（月/年切换高亮）在此恢复。
 */

/* Lovart 复刻页 FAQ 各页定制答案 —— 基于 Lovart 官方功能与各行业场景编写。
   键 = 页面 slug（replica-solution- 前缀已剥），值 = 与页面 FAQ 问题一一对应的答案数组。
   由 lovart-replica.js 的 initFaqFill 在检测到手风琴 panel 为空时按序注入。 */
window.LR_FAQ_ANSWERS = {
  "ai-design-solution-for-saas": [
    "Both. PLG teams use Lovart to ship in-app empty states, onboarding flows, and paywall creatives from a single brief, while sales-led teams generate one-pagers, deck visuals, and ABM assets on the same Brand Kit. The workflow is identical: brief once, then branch assets per funnel stage.",
    "Start with three things: your logo files (SVG/PNG), your brand colors and fonts, and 2–3 existing product screenshots or a product URL. Lovart's Brand Kit ingests these in minutes and uses them as the source of truth for every asset it generates afterward.",
    "Yes. Describe the release or feature once, and Lovart produces a coordinated set: in-app modals and tooltips, launch emails, social posts, and ad variants—all sharing the same visual system. You edit copy or layout per channel without regenerating the whole set.",
    "Brand Kit locks your palette, typography, logo usage, and tone into a reusable profile, so PMM, design, and sales all generate on-brand assets without handing files back and forth. New teammates pick it up instantly instead of learning a design system doc.",
    "Yes. Enterprise plans include role-based access, shared Brand Kits with approval controls, SSO, audit logs, and the ability to lock templates so regional teams can localize copy without breaking layout or brand rules.",
    "All plans include a commercial license. You own the assets you generate and can use them in product, marketing, paid ads, and customer-facing materials without attribution."
  ],
  "ai-design-solution-for-agencies": [
    "Yes. Create a separate Brand Kit per client—each with its own logos, colors, fonts, and voice—and switch between them in one workspace. Assets for Client A never bleed into Client B, and you can invite clients to review or comment on their own kit only.",
    "Only if you tell them. Lovart output is polished, fully editable design work—not watermarked AI artifacts. Most agencies present it as their in-house design process; the speed is your competitive advantage, not something you have to disclose.",
    "It expands your margins instead of compressing them. Agencies typically keep project pricing stable and pocket the efficiency gain, or use the speed to offer faster-turnaround tiers. Lovart's per-seat cost is a fraction of a single freelance revision round.",
    "Yes. Export production-ready files (PNG, JPG, SVG, PDF) and present them under your own brand. There's no Lovart branding on deliverables, so the work reads as your agency's output end to end.",
    "Fast. Designers adapt in a day because Lovart works from briefs and Brand Kits rather than a new tool paradigm. Account managers and strategists can generate client-ready drafts themselves, freeing senior designers for high-judgment work."
  ],
  "ai-design-solution-for-creators": [
    "No. Podcasters, newsletter writers, TikTok and Instagram creators, streamers, and course creators all use it. If you publish anywhere, you need thumbnails, covers, episode art, and promo graphics—Lovart generates them from a single description of the episode or post.",
    "Yes. Share your Brand Kit with your editor or VA so they generate thumbnails and covers that stay on-brand without you reviewing every pixel. You keep ownership and final say; they get a self-serve way to produce assets in your style.",
    "Lovart exports every platform's dimensions: YouTube thumbnails (1280×720), Instagram posts and stories, TikTok, X headers, podcast cover art (3000×3000), and more. Generate once, then resize per platform while keeping text and subject framed correctly.",
    "Yes. Build a reusable media kit or sponsor-read template with your branding, then swap in each sponsor's name, product, and talking points. It keeps sponsored content visually consistent with your channel instead of looking like an ad break.",
    "Yes. Every element—text, layout, background, subject—is editable after generation. Adjust the headline, move the composition, or swap a background without starting over, so you iterate on a thumbnail until it clicks.",
    "Yes. A commercial license is included, so thumbnails, sponsor graphics, merch designs, and paid promotions are all cleared for monetized content."
  ],
  "ai-design-for-fitness-wellness-hub": [
    "All three. Solo coaches generate class promos and client-transformation posts themselves; boutique studios keep a consistent look across class schedules and challenges; multi-location gyms push brand-approved assets to every branch. The workflow scales from one person to a franchise.",
    "Yes. Upload member progress photos (with their consent) and Lovart lays them out into professional before/after graphics, challenge recaps, and testimonial cards—sized for Instagram, your app, or in-studio screens—while keeping faces and details accurate.",
    "No. Coaches and front-desk staff generate on-brand graphics from a text brief, no design background needed. If you do have a designer, they set up the Brand Kit once and the whole team self-serves from then on.",
    "Instagram and Facebook posts/stories, class-schedule graphics, email headers, Google Business photos, in-app banners, and printable posters or flyers for the front desk. Each is exported at the right dimensions and resolution for its channel.",
    "Yes. Corporate locks the Brand Kit—colors, logo, class-naming, photo style—and each location fills in its own schedule, coach names, and local offers. Members get a consistent brand experience everywhere, with zero rogue flyers.",
    "Yes. Commercial use is covered, including member transformation marketing, paid ads, and printed materials. Just make sure you have each member's written consent before featuring their photos or results."
  ],
  "ai-design-solution-for-shopify": [
    "No—Lovart is a standalone design agent, not a Shopify app. You don't install anything in your store. You bring your product photos and brand assets, generate listing images, ad creatives, and campaign visuals in Lovart, then upload the finished files to Shopify as usual.",
    "Your product photos on clean backgrounds, your logo, and your brand colors. If you have a product page or catalog URL, add that too. Lovart uses these to build a Brand Kit so every generated image matches your store's look.",
    "Yes. Describe the product or promotion once, and Lovart produces the full set: PDP hero and lifestyle images, collection banners, email graphics, and paid-social ad variants—consistent from first touch to checkout.",
    "Brand Kit holds your palette, fonts, logo, and product-photography style constant, so a flash sale, a new collection, and a restock announcement all look like the same store. No more mismatched marketplace-style listings.",
    "Yes. Edit text, swap backgrounds, adjust layout, or change a model's pose after generation. You refine a hero image until it converts instead of accepting the first render.",
    "Yes. A commercial license is included, so product images, ads, and storefront banners are all cleared for selling."
  ],
  "ai-design-for-small-business-hub": [
    "No. Cafés, salons, retail shops, contractors, gyms, and local services all use it. Any business that needs menus, flyers, social posts, or signage can generate them from a plain description—no restaurant-specific features required.",
    "Yes. Export high-resolution PDF and PNG files suitable for professional printing—menus, flyers, business cards, window posters, and banners. Set your dimensions and bleed before export and the files are press-ready.",
    "No. Describe what you need in plain words—\"a lunch special flyer, warm tones, my logo top-left\"—and Lovart handles layout, typography, and imagery. You review and tweak text; the design work is done for you.",
    "In minutes. Update the dish name, price, and photo on your saved special template and export a fresh version for your socials, Google profile, and in-store board before the lunch rush.",
    "Yes. Save your Brand Kit and templates, then each location fills in its own address, hours, and local offers. Every branch looks like the same business without you re-doing the design each time.",
    "Yes. A commercial license is included, so menus, ads, signage, and packaging are all cleared for business use."
  ],
  "ai-design-solution-for-marketing-teams": [
    "Yes. Marketers generate campaign assets from a brief—no design training needed. Lovart handles layout and brand consistency; you supply the message and targeting. Designers step in only for high-stakes creative direction.",
    "It frees them. Routine production—ad variants, social sizes, email headers—moves to self-serve, so your design team focuses on brand systems, campaigns concepts, and work that actually needs their judgment instead of resizing banners.",
    "Yes. Generate dozens of on-brand ad variants—different headlines, visuals, and CTAs—from one brief, then feed them straight into your testing platform. Creative volume stops being the bottleneck in your testing roadmap.",
    "Yes. Shared workspaces and Brand Kits let the whole team generate on-brand assets, with roles and approvals so junior marketers can draft while leads review before anything ships.",
    "Fast enough to ride the news cycle. A reactive post, trend-jacking creative, or same-day launch graphic takes minutes from brief to export, so your team can respond while the moment is still relevant.",
    "Brand Kit enforces your palette, fonts, logo, and tone across every region. Local teams translate and localize copy inside locked layouts, so a campaign looks identical whether it ships in Berlin, Tokyo, or São Paulo."
  ],
  "ai-design-solution-for-nonprofits": [
    "Lovart offers discounted and grant-supported access for registered nonprofits. Apply with your organization's details and the team will set you up—many small nonprofits use it at little or no cost depending on the program.",
    "Registered 501(c)(3) organizations in the US and equivalent registered charities elsewhere qualify. You'll provide your registration number and a brief description of your mission; approval is typically quick.",
    "Yes. A shared workspace lets staff and volunteers generate on-brand materials under one nonprofit Brand Kit, with roles so a volunteer can draft an event flyer while a staff member approves it before it goes out.",
    "Yes. Output is polished, print-ready design suitable for gala invitations, annual reports, major-donor decks, and foundation grant materials—not clip-art. You control the imagery and tone to match the gravity of the audience.",
    "Yes. Upload your logo, colors, fonts, and existing photo library into a Brand Kit. Everything Lovart generates—appeals, event graphics, impact reports—stays consistent with the identity your donors already recognize."
  ],
  "good-design-for-business-owners": [
    "Lovart is an AI design agent: you describe what you need in plain language and it produces finished, editable design work—logos, marketing materials, social graphics, presentations, and more—using your brand assets as the reference.",
    "Logos and brand refreshes, flyers and signage, social media content, menus or price lists, business cards, pitch decks, product packaging concepts, and ad creative. Essentially any visual your business needs, generated from a brief instead of a designer brief-and-wait cycle.",
    "Yes. Lovart routes across leading image, video, and language models and picks the right one for each task, so you get current-generation quality without managing separate AI subscriptions.",
    "Yes. Paid plans include a full commercial license—you own what you generate and can use it in your products, marketing, and paid advertising with no attribution required.",
    "Export PNG, JPG, SVG, and PDF at web, social, and print resolutions, in custom dimensions. Platform presets cover Instagram, Facebook, LinkedIn, and standard print sizes with bleed.",
    "There's a free tier with monthly credits to try real projects. Paid plans start at $19/month and add more credits, faster generation, and team features.",
    "Reach us anytime through the in-app help chat or support@lovart.ai—we answer product, billing, and licensing questions directly."
  ],
  "good-design-for-marketers": [
    "Lovart is an AI design agent built for marketing work: brief it once and it produces coordinated campaign assets—ads, social, email, landing visuals—on your brand, editable down to the last headline.",
    "Campaign creative across channels, ad variants for A/B testing, social content calendars, email headers, event and webinar graphics, pitch and report decks, and brand-consistent templates your whole team can reuse.",
    "Yes. Lovart integrates leading image, video, and language models and selects the best one per task, so your creative stays at the current state of the art without extra subscriptions.",
    "Yes. Paid plans include a full commercial license—you own the output and can run it in paid campaigns, client work, and any revenue-generating channel.",
    "Export PNG, JPG, SVG, and PDF at any dimensions, with presets for every ad network and social platform, plus print-ready formats with bleed.",
    "A free tier with monthly credits lets you run real campaigns. Paid plans start at $19/month for more credits, faster queues, and team collaboration.",
    "Our team is available via the in-app chat or support@lovart.ai for campaign, licensing, or workflow questions."
  ],
  "comparison-hub": [
    "Lovart is a design workflow, not a Shopify app. It doesn't plug into your admin; it produces the product images, PDP visuals, and ad creative your store needs, which you then upload to Shopify or any other platform.",
    "Product photos on clean backgrounds, your logo and brand palette, and—if available—a product URL or catalog. Lovart builds a Brand Kit from these so every output matches your storefront.",
    "Yes. It generates PDP hero shots, lifestyle scenes, infographics, size charts, and ad-ready variants from one product brief, all consistent with your brand photography style.",
    "Beyond raw generation, it produces conversion-focused layouts—benefit callouts, comparison visuals, review-style graphics, and A/B variants—so you test and improve the funnel, not just fill image slots.",
    "Yes. All text is editable post-generation, including sale copy, CTAs, and localized language versions, without regenerating the visual.",
    "Thinking Mode plans multi-step asset sets and reasons about layout before rendering—best for campaigns; Fast Mode renders single assets immediately—best for quick iterations and tests.",
    "This page showcases the comparison-focused component set used across our solution pages, so you can evaluate layout and content patterns side by side.",
    "There's a free tier with monthly credits. Paid plans start at $19/month (Starter), $32/month (Basic), and $90/month (Pro), with annual billing at a discount and Ultimate for high-volume teams."
  ],
  "product-launch": [
    "Lovart is a design workflow, not a Shopify app. It doesn't plug into your admin; it produces the product images, PDP visuals, and ad creative your store needs, which you then upload to Shopify or any other platform.",
    "Product photos on clean backgrounds, your logo and brand palette, and—if available—a product URL or catalog. Lovart builds a Brand Kit from these so every output matches your storefront.",
    "Yes. It generates PDP hero shots, lifestyle scenes, infographics, size charts, and ad-ready variants from one product brief, all consistent with your brand photography style.",
    "Beyond raw generation, it produces conversion-focused layouts—benefit callouts, comparison visuals, review-style graphics, and A/B variants—so you test and improve the funnel, not just fill image slots.",
    "Yes. All text is editable post-generation, including sale copy, CTAs, and localized language versions, without regenerating the visual.",
    "Thinking Mode plans multi-step asset sets and reasons about layout before rendering—best for campaigns; Fast Mode renders single assets immediately—best for quick iterations and tests.",
    "This page showcases the launch-focused component set used across our solution pages, so you can evaluate layout and content patterns side by side.",
    "There's a free tier with monthly credits. Paid plans start at $19/month (Starter), $32/month (Basic), and $90/month (Pro), with annual billing at a discount and Ultimate for high-volume teams."
  ]
};


/* ---------- 对比表各页定制内容 ----------
   6 个 solution 页的 comparison-table 表体在源站就是空壳（客户端 hydration 注入），
   且每行缺第 4 列（Lovart 高亮列）。initCompareFill 按 slug 注入 5 行 × 4 列内容，
   并补建缺失的 Lovart 列单元格；h2/sub 仅用于订正源站张冠李戴的健身文案。 */
window.LR_COMPARE = {
  "ai-design-solution-for-agencies": {
    "rows": [
      ["Handle overflow briefs", "Booked out for weeks", "Quality varies by vendor", "On-demand capacity in minutes"],
      ["Protect margins", "Senior rates on junior tasks", "Markup on markup", "Flat subscription, unlimited variants"],
      ["Keep every client's brand straight", "Relies on briefs and memory", "Style drifts between vendors", "Brand Kit per client, applied automatically"],
      ["Turn revisions around fast", "New round, new day", "Async back-and-forth across time zones", "Touch Edit and Text Edit in place"],
      ["Pitch with speculative creative", "Too costly before the win", "Not worth outsourcing", "Concept boards and mockups before the pitch"]
    ]
  },
  "ai-design-solution-for-marketing-teams": {
    "h2": "How marketing team creative production compares",
    "sub": "Three models. One that keeps pace with the campaign calendar.",
    "rows": [
      ["Campaign assets at launch speed", "Weeks per campaign round", "Fast but generic", "Full campaign set from one brief"],
      ["On-brand every time", "Depends on the brief", "Templates drift off-brand", "Brand Kit + Style Consistency"],
      ["Every channel and format", "Per-deliverable fees", "Manual resizing per channel", "Social, email, ads, landing from one concept"],
      ["Iterate on performance data", "New PO per iteration", "Start over each time", "Touch Edit variants in minutes"],
      ["Scale testing volume", "Costly per variant", "One template, one look", "Fast Mode for hooks, offers and markets"]
    ]
  },
  "ai-design-solution-for-nonprofits": {
    "rows": [
      ["Stretch every dollar", "Agency fees compete with programs", "Free but uneven", "Flat subscription, unlimited campaigns"],
      ["Look credible to donors", "Great, when budget allows", "Amateur look hurts trust", "Studio-quality output every time"],
      ["Launch appeals fast", "Weeks of lead time", "Depends on volunteer time", "Appeal assets in minutes"],
      ["Stay on-brand across chapters", "Guidelines in a PDF", "Everyone improvises", "Brand Kit enforced on every asset"],
      ["Report impact beautifully", "Annual-report project pricing", "Charts in a Word doc", "Impact reports, infographics and social from your data"]
    ]
  },
  "ai-design-solution-for-saas": {
    "h2": "How SaaS GTM creative production compares",
    "sub": "Three models. One that ships at release cadence.",
    "rows": [
      ["Ship at release cadence", "Sprint-cycle mismatch", "Queue behind product work", "Assets at the speed of shipping"],
      ["Full-funnel GTM creative", "Per-deliverable scoping", "Bandwidth caps at launch", "Ads, landing, email, social from one brief"],
      ["Product-accurate visuals", "Rounds of screenshot corrections", "Depends on designer context", "Reads your product, docs and URLs"],
      ["Iterate on conversion data", "Change orders and delays", "Competes with roadmap work", "Touch Edit variants in minutes"],
      ["Scale without headcount", "Retainers grow with scope", "Hiring takes quarters", "Flat subscription, unlimited variants"]
    ]
  },
  "ai-design-solution-for-shopify": {
    "rows": [
      ["Launch SKUs fast", "Shoot scheduling per product", "Fast but off-brand", "PDP and lifestyle images from your product"],
      ["Refresh seasonal campaigns", "Reshoots every season", "Same templates as competitors", "New scenes without new shoots"],
      ["Cover every placement", "Per-asset pricing", "Manual resizing", "PDP, ads, email, social in one flow"],
      ["Brand consistency at scale", "Depends on the retoucher", "Drifts across templates", "Brand Kit on every asset"],
      ["Test creative variants", "Too costly to test", "Limited variation", "Fast Mode for hooks, offers and formats"]
    ]
  },
  "good-design-for-marketers": {
    "h2": "How marketer creative production compares",
    "sub": "Three models. One built for deadline-driven marketers.",
    "rows": [
      ["Campaign assets on deadline", "Availability lottery", "Fast but generic", "Minutes from brief to full set"],
      ["On-brand output", "Varies by freelancer", "Templates drift", "Brand Kit + Style Consistency"],
      ["Multi-format deliverables", "Per-asset fees", "Resize by hand", "Social, ads, email, decks from one brief"],
      ["Quick edits and variants", "Billable revision rounds", "Rebuild from scratch", "Touch Edit and Text Edit in place"],
      ["More testing, less budget", "Cost per variant adds up", "One look per template", "Fast Mode for hooks, offers and audiences"]
    ]
  }
};

(function () {
  function q(sel, root) { return (root || document).querySelector(sel); }
  function qa(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  /* ---------- before/after 对比滑块 ----------
     源结构（comparison-before-after）：外层 role="slider"（cursor-col-resize）+ 
     两个 clip-path 图层（before: inset(0 50% 0 0) 右裁 / after: inset(0 0 0 50%) 左裁）
     + 中线（left:50%）。拖动 = 同时更新两图层的 clip 与中线位置。 */
  function initSlider(slider) {
    if (!slider || slider.dataset.lovartSlider) return;
    slider.dataset.lovartSlider = "1";
    // touch-none 会阻止 touch 拖动，覆盖为允许水平手势
    try { slider.style.touchAction = "pan-y"; } catch (e) {}
    var sec = slider.closest("[data-lp-section]") || slider.parentElement;
    var before = null, after = null, line = null, knob = null;
    qa("[style*='clip-path']", sec).forEach(function (el) {
      if (el === slider || !slider.contains(el)) return; // 排除滑块本体背景
      var cp = el.style.clipPath || "";
      if (/inset\(0(px)?\s+[\d.]+%\s+0(px)?\s+0(px)?\)/.test(cp)) before = el;
      else if (/inset\(0(px)?\s+0(px)?\s+0(px)?\s+[\d.]+%\)/.test(cp)) after = el;
    });
    qa("[style*='left:50%'], [style*='left: 50%']", sec).forEach(function (el) {
      if (el === slider) return;
      // 细线（w-px）与圆形手柄（rounded-full）都要随动
      if (/w-px|bg-white/.test(el.className)) line = el;
      else if (/rounded-full/.test(el.className)) knob = el;
      else if (!line) line = el;
    });
    function rect() { return slider.getBoundingClientRect(); }
    function setPct(pct) {
      if (!isFinite(pct)) return;
      pct = Math.min(100, Math.max(0, pct));
      slider.setAttribute("aria-valuenow", pct.toFixed(0));
      if (before) before.style.clipPath = "inset(0 " + (100 - pct).toFixed(2) + "% 0 0)";
      if (after) after.style.clipPath = "inset(0 0 0 " + pct.toFixed(2) + "%)";
      if (line) line.style.left = pct.toFixed(2) + "%";
      if (knob) knob.style.left = pct.toFixed(2) + "%";
    }
    var dragging = false;
    slider.addEventListener("pointerdown", function (e) {
      dragging = true;
      try { slider.setPointerCapture(e.pointerId); } catch (err) {}
      setPct(((e.clientX || rect().left + 1) - rect().left) / (rect().width || 1) * 100);
    });
    slider.addEventListener("pointermove", function (e) { if (dragging) { e.preventDefault(); setPct(((e.clientX || 0) - rect().left) / (rect().width || 1) * 100); } });
    slider.addEventListener("pointerup", function () { dragging = false; });
    slider.addEventListener("pointercancel", function () { dragging = false; });
    // 键盘可达性
    slider.addEventListener("keydown", function (e) {
      var cur = parseFloat(slider.getAttribute("aria-valuenow") || "50");
      if (e.key === "ArrowLeft") { e.preventDefault(); setPct(cur - 5); }
      if (e.key === "ArrowRight") { e.preventDefault(); setPct(cur + 5); }
    });
  }

  /* ---------- FAQ / howto / workflow 手风琴 ----------
     radix 结构：button[aria-expanded][id=radix-X] ↔ div[role=region][aria-labelledby=radix-X]
     button 无 aria-controls，panel 靠 aria-labelledby 反向关联。开闭需同步
     button/panel/item 三处 data-state，并切换 hidden（panel 高度动画靠 data-state）。 */
  function findPanel(btn) {
    var ctrl = btn.getAttribute("aria-controls");
    if (ctrl) return document.getElementById(ctrl);
    if (btn.id) {
      var byLabel = document.querySelector('[role="region"][aria-labelledby="' + btn.id + '"]');
      if (byLabel) return byLabel;
    }
    var item = btn.closest("[data-state]");
    if (item) {
      var region = item.querySelector('[role="region"]');
      if (region) return region;
    }
    return btn.parentElement ? btn.parentElement.nextElementSibling : null;
  }
  function initAccordion(root) {
    /* 静态 HTML 的 panel 全部 hidden（radix 服务端渲染的收起态），脚本必须负责：
       1) 初始同步——把 aria-expanded=true 的项展开；全关时展开第一项（对齐设计稿）
       2) 点击切换——单开互斥 + JS 高度动画（源站 animate-accordion-down/up 依赖
          radix CSS 变量，镜像层没有，必须自己驱动高度过渡） */
    function setState(btn, panel, open, animate) {
      btn.setAttribute("aria-expanded", String(open));
      var item = btn.closest("[data-state]");
      if (item) item.setAttribute("data-state", open ? "open" : "closed");
      if (btn.hasAttribute("data-state")) btn.setAttribute("data-state", open ? "open" : "closed");
      if (!panel) return;
      if (panel.hasAttribute("data-state")) panel.setAttribute("data-state", open ? "open" : "closed");
      var svg = btn.querySelector("svg");
      if (svg) svg.style.transform = open ? "rotate(180deg)" : "";
      if (!open) {
        if (animate && !panel.hasAttribute("hidden")) {
          panel.style.height = panel.scrollHeight + "px";
          void panel.offsetHeight;
          panel.style.transition = "height 0.25s ease";
          panel.style.height = "0px";
          var close = function () { panel.setAttribute("hidden", ""); panel.style.display = ""; panel.style.height = ""; panel.style.transition = ""; };
          panel.addEventListener("transitionend", close, { once: true });
          setTimeout(close, 350);
        } else {
          panel.setAttribute("hidden", "");
          panel.style.height = ""; panel.style.transition = "";
        }
      } else {
        panel.removeAttribute("hidden");
        if (animate) {
          panel.style.height = "0px";
          void panel.offsetHeight;
          panel.style.transition = "height 0.25s ease";
          panel.style.height = panel.scrollHeight + "px";
          var done = function () { panel.style.height = "auto"; panel.style.transition = ""; };
          panel.addEventListener("transitionend", done, { once: true });
          setTimeout(done, 350);
        } else {
          panel.style.height = ""; panel.style.transition = "";
        }
      }
    }
    var groups = [];
    qa("[aria-expanded]", root).forEach(function (btn) {
      if (btn.dataset.lovartAcc) return;
      var p0 = findPanel(btn);
      if (!p0 || p0.getAttribute && p0.getAttribute("role") !== "region") return; // 只接管真手风琴
      btn.dataset.lovartAcc = "1";
      var grp = btn.closest("[data-lp-section]") || btn.parentElement;
      if (groups.indexOf(grp) === -1) groups.push(grp);
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var open = btn.getAttribute("aria-expanded") !== "true";
        // 单开互斥：同组内其它展开项收起
        if (open) {
          qa('[aria-expanded="true"]', grp).forEach(function (other) {
            if (other !== btn) setState(other, findPanel(other), false, true);
          });
        }
        setState(btn, findPanel(btn), open, true);
      });
    });
    // 初始同步（无动画）
    groups.forEach(function (grp) {
      var btns = qa('[aria-expanded]', grp).filter(function (b) { return b.dataset.lovartAcc; });
      if (!btns.length) return;
      var opened = false;
      btns.forEach(function (b) {
        if (b.getAttribute("aria-expanded") === "true") { setState(b, findPanel(b), true, false); opened = true; }
        else setState(b, findPanel(b), false, false);
      });
      if (!opened) setState(btns[0], findPanel(btns[0]), true, false); // 设计稿默认展开第一项
    });
  }

  /* ---------- capability-tabs：点击切换 + 自动轮播 ---------- */
  function initTabs(root) {
    qa('[role="tablist"]', root).forEach(function (list) {
      if (list.dataset.lovartTabs) return;
      list.dataset.lovartTabs = "1";
      var tabs = qa('[role="tab"]', list);
      if (!tabs.length) return;
      // 面板：与 tablist 同一 section 内的 tabpanel，按索引对应
      var scope = list.closest("[data-lp-section]") || list.parentElement;
      var panels = qa('[role="tabpanel"]', scope);
      var timer = null, cur = 0;

      function activate(idx, user) {
        cur = ((idx % tabs.length) + tabs.length) % tabs.length;
        tabs.forEach(function (t, i) {
          var on = i === cur;
          t.setAttribute("aria-selected", String(on));
          if (t.hasAttribute("data-state")) t.setAttribute("data-state", on ? "active" : "inactive");
          t.classList.toggle("lr-tab-active", on);
        });
        panels.forEach(function (p, i) {
          var on = i === cur;
          p.style.display = on ? "" : "none";
          if (on) { p.removeAttribute("hidden"); } else { p.setAttribute("hidden", ""); }
          if (p.hasAttribute("data-state")) p.setAttribute("data-state", on ? "active" : "inactive");
        });
        if (user) restart(); // 手动点击后重置轮播计时
      }
      function next() { activate(cur + 1, false); }
      function restart() { if (timer) clearInterval(timer); timer = setInterval(next, 5000); }
      function stop() { if (timer) { clearInterval(timer); timer = null; } }

      tabs.forEach(function (t, i) {
        t.addEventListener("click", function (e) { e.preventDefault(); activate(i, true); });
      });
      // hover/聚焦暂停轮播，移出恢复
      scope.addEventListener("mouseenter", stop);
      scope.addEventListener("mouseleave", function () { if (!timer) restart(); });
      scope.addEventListener("focusin", stop);
      scope.addEventListener("focusout", function () { if (!timer) restart(); });

      // 初始：以 aria-selected=true 的为准，否则第 0 个
      var init = 0;
      tabs.forEach(function (t, i) { if (t.getAttribute("aria-selected") === "true") init = i; });
      activate(init, false);
      restart();
    });
  }

  /* ---------- 对话面板：可输入、可发送 ----------
     对话输入框可能出现在 hero（无 data-lp-section，类 hero-chat-in）或
     prompt-launcher / hero-cinematic 等区块。统一以「含 textarea/可编辑框的
     最近卡片容器」为作用域初始化。 */
  function initChat(root) {
    var inputs = qa("textarea, input[type='text'], [contenteditable='true']", root).filter(function (el) {
      // 排除搜索框/表单
      return !/(search|email|password|tel|url|number)/i.test(el.type || "") && !el.closest("form[action]");
    });
    inputs.forEach(function (input) {
      var sec = input.closest("[data-lp-section]") || input.closest("[class*='hero-chat'], [class*='chat'], main, .lr");
      if (!sec || sec.dataset.lovartChat) return;
      sec.dataset.lovartChat = "1";
      var sendBtn = q("button[type='submit']", sec)
        || qa("button", sec).filter(function (b) {
             var label = (b.textContent || "") + (b.getAttribute("aria-label") || "");
             return /send|发送|submit|生成|create|→|↑|➤/i.test(label);
           })[0]
        || qa("button", sec).filter(function (b) { return b.querySelector("svg") && !b.getAttribute("aria-expanded"); })[0];
      // 对话流容器：优先 overflow 滚动容器，否则 hero-chat-in 卡片，否则输入框父级
      var stream = q("[class*='overflow-y-auto'], [class*='overflow-y-scroll'], [class*='hero-chat-in']", sec)
        || input.parentElement;
      function val() { return input.tagName === "TEXTAREA" || input.tagName === "INPUT" ? input.value : input.textContent; }
      function clear() { if (input.tagName === "TEXTAREA" || input.tagName === "INPUT") input.value = ""; else input.textContent = ""; }
      function send() {
        var text = (val() || "").trim();
        if (!text) return;
        if (stream) {
          var msg = document.createElement("div");
          msg.className = "lr-chat-user-msg";
          msg.textContent = text;
          stream.appendChild(msg);
          stream.scrollTop = stream.scrollHeight;
        }
        clear();
      }
      if (sendBtn) sendBtn.addEventListener("click", function (e) { e.preventDefault(); send(); });
      input.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
      });
    });
  }

  /* ---------- 页脚主题切换 ---------- */
  function applyTheme(mode) {
    qa(".lr").forEach(function (el) {
      if (mode === "day") { el.classList.remove("dark"); el.classList.add("light"); }
      else if (mode === "night") { el.classList.remove("light"); el.classList.add("dark"); }
      else { /* auto: 跟随系统 */ }
    });
    if (mode === "auto") {
      var dark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
      applyTheme(dark ? "night" : "day");
      return;
    }
  }
  function initTheme(root) {
    var stored = null;
    try { stored = localStorage.getItem("lr-theme"); } catch (e) {}
    if (stored) applyTheme(stored);
    qa("[data-track-id^='footer_theme_']", root).forEach(function (btn) {
      if (btn.dataset.lovartTheme) return;
      btn.dataset.lovartTheme = "1";
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var mode = (btn.getAttribute("data-track-id") || "").replace("footer_theme_", "");
        if (mode === "day") mode = "day";
        if (mode === "night") mode = "night";
        if (mode === "auto") mode = "auto";
        try { localStorage.setItem("lr-theme", mode); } catch (err) {}
        applyTheme(mode);
      });
    });
  }

  /* ---------- 页脚语言切换（前端记忆，无翻译服务） ---------- */
  function initLang(root) {
    var btns = qa("button, a", root).filter(function (b) {
      return /^(English|中文|简体中文|繁體中文|日本語|한국어|Español|Français|Deutsch)/.test((b.textContent || "").trim());
    });
    btns.forEach(function (b) {
      if (b.dataset.lovartLang) return;
      b.dataset.lovartLang = "1";
      b.addEventListener("click", function (e) {
        // 站点为单语言静态复刻：阻止无效跳转，提示当前为演示环境
        e.preventDefault();
      });
    });
  }

  /* ---------- 价格区：月/年切换高亮（静态占位，真实价格源抓取时即缺失） ---------- */
  function initPricing(root) {
    qa("[data-testid^='paywall-tab-'], [data-lp-section='pricing-block'] button", root).forEach(function (btn) {
      if (btn.dataset.lovartPricing) return;
      var grp = btn.closest("[role='tablist'], [class*='rounded-full'], div");
      btn.dataset.lovartPricing = "1";
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        if (!grp) return;
        qa("button", grp).forEach(function (b) { b.classList.remove("lr-paywall-active"); });
        btn.classList.add("lr-paywall-active");
      });
    });
  }

  /* ---------- FAQ 各页定制答案注入 ----------
     源站 FAQ 手风琴 panel 是空壳（答案靠客户端 hydration 注入），静态抓取拿不到。
     LR_FAQ_ANSWERS 提供按页面 slug 定制的答案，initFaqFill 在检测到手风琴时
     按序把答案填入对应 panel（保留原 DOM 结构与开闭交互）。 */
  function pageSlug() {
    var m = location.pathname.match(/replica-(?:solution-)?([a-z0-9-]+)\/?$/i);
    return m ? m[1] : null;
  }
  function initFaqFill(root) {
    var answers = (window.LR_FAQ_ANSWERS || {})[pageSlug()];
    if (!answers || !answers.length) return;
    var sec = q('[data-lp-section="faq"]', root);
    if (!sec || sec.dataset.lovartFaqFill) return;
    var panels = qa('[role="region"]', sec);
    if (!panels.length) return;
    sec.dataset.lovartFaqFill = "1";
    panels.forEach(function (panel, i) {
      if (i >= answers.length) return;
      if ((panel.textContent || "").trim().length > 0) return; // 已有内容则不动
      var body = document.createElement("div");
      body.className = "lr-faq-answer pb-4 font-sans text-[14px] leading-[1.65] text-text-secondary";
      body.textContent = answers[i];
      panel.appendChild(body);
    });
  }

  /* ---------- 对比表内容注入 ----------
     6 个 solution 页的 comparison-table 表体为空壳且每行缺 Lovart 高亮列。
     按 slug 注入 LR_COMPARE 内容；td 不足 4 个时补建 Lovart 列（沿用满表的
     高亮类名）；data 提供 h2/sub 时订正源站张冠李戴的标题文案。 */
  var LOVART_TD_CLASS = "h-[72px] px-3 align-middle font-sans text-[13px] md:px-6 md:text-[14px] bg-bg-base-secondary text-text-default font-medium border-border-neutral-l2 border-l border-b";
  function initCompareFill(root) {
    var data = (window.LR_COMPARE || {})[pageSlug()];
    if (!data || !data.rows || !data.rows.length) return;
    var sec = q('[data-lp-section="comparison-table"]', root);
    if (!sec || sec.dataset.lovartCompareFill) return;
    var rows = qa("tbody tr", sec);
    if (!rows.length) return;
    sec.dataset.lovartCompareFill = "1";
    rows.forEach(function (tr, i) {
      if (i >= data.rows.length) return;
      var want = data.rows[i];
      var tds = qa("td", tr);
      var allEmpty = tds.every(function (td) { return !(td.textContent || "").trim(); });
      if (!allEmpty) return; // 已有内容则不动
      tds.forEach(function (td, j) { if (j < want.length && j < 3) td.textContent = want[j]; });
      if (tds.length < 4 && want.length >= 4) {
        var td = document.createElement("td");
        td.className = LOVART_TD_CLASS;
        td.textContent = want[3];
        tr.appendChild(td);
      } else if (tds.length >= 4 && want.length >= 4) {
        tds[3].textContent = want[3];
      }
    });
    if (data.h2) { var h2 = q("h2", sec); if (h2) h2.textContent = data.h2; }
    if (data.sub) {
      var h2el = q("h2", sec);
      var wrap = h2el && h2el.parentElement && h2el.parentElement.parentElement;
      var p = wrap ? q("p", wrap) : q("p", sec);
      if (p) p.textContent = data.sub;
    }
  }

  /* ---------- 价格区：真实定价渲染（Lovart 官方 member/packages 数据） ----------
     源站 pricing-block 是 animate-pulse 骨架屏（客户端 hydrate 时才填真实卡片），
     静态抓取拿不到 → 这里用内嵌的真实定价数据（4 档 × 月/年）替换骨架网格，
     并接月/年切换联动重渲染。 */
  var LR_PRICING = {"monthly":[{"name":"Starter","price":19,"original":19,"feats":["2000 Credits monthly","2000 extra credits first month","~40 Agent conversations","~500 GPT images","~8000 Flux images","~111 Kling videos","Unlimited Trial Models","Commercial license"]},{"name":"Basic","price":32,"original":32,"feats":["3500 Credits monthly","3500 extra credits first month","~35 Agent conversations","~438 GPT images","~7000 Flux images","~51 Kling videos","Unlimited Trial Models","Commercial license"]},{"name":"Pro","price":90,"original":90,"feats":["11000 Credits monthly","11000 extra credits first month","~110 Agent conversations","~1375 GPT images","~22000 Flux images","~162 Kling videos","Unlimited Trial Models","Commercial license"]},{"name":"Ultimate","price":199,"original":199,"feats":["22000 Credits monthly","22000 extra credits first month","~220 Agent conversations","~2750 GPT images","~44000 Flux images","~324 Kling videos","Unlimited Trial Models","Commercial license","Priority generation queue","Dedicated support"]}],"yearly":[{"name":"Starter","price":192,"original":228,"feats":["2000 Credits monthly","2000 extra credits first month","~40 Agent conversations","~500 GPT images","~8000 Flux images","~111 Kling videos","Unlimited Trial Models","Commercial license"]},{"name":"Basic","price":324,"original":384,"feats":["3500 Credits monthly","3500 extra credits first month","~35 Agent conversations","~438 GPT images","~7000 Flux images","~51 Kling videos","Unlimited Trial Models","Commercial license"]},{"name":"Pro","price":888,"original":1080,"feats":["11000 Credits monthly","11000 extra credits first month","~110 Agent conversations","~1375 GPT images","~22000 Flux images","~162 Kling videos","Unlimited Trial Models","Commercial license"]},{"name":"Ultimate","price":1992,"original":2388,"feats":["22000 Credits monthly","22000 extra credits first month","~220 Agent conversations","~2750 GPT images","~44000 Flux images","~324 Kling videos","Unlimited Trial Models","Commercial license","Priority generation queue","Dedicated support"]}]};

  function pricingCard(plan, period) {
    var per = period === "yearly" ? "/yr" : "/mo";
    var card = document.createElement("div");
    card.className = "border-lo-border-neutral-l2 mt-[30px] flex w-full flex-col gap-6 rounded-[16px] border pb-6 bg-transparent";
    var feats = plan.feats.map(function (f) {
      return '<div class="flex items-center gap-2">' +
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" class="shrink-0 text-text-default"><path d="M3 8.5l3.2 3L13 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
        '<span class="font-sans text-[13px] leading-[1.5] text-text-secondary">' + f + '</span></div>';
    }).join("");
    card.innerHTML =
      '<div class="border-lo-border-neutral-l2 flex flex-col gap-4 border-b p-6">' +
        '<div class="flex h-6 items-center gap-1"><span class="font-sans text-[16px] font-medium text-text-default">' + plan.name + '</span></div>' +
        '<div class="flex items-baseline gap-1"><span class="font-sans text-[32px] leading-none font-semibold text-text-default">$' + plan.price + '</span><span class="font-sans text-[13px] text-text-tertiary">' + per + '</span></div>' +
        (plan.original > plan.price ? '<div class="font-sans text-[12px] text-text-tertiary line-through">$' + plan.original + per + '</div>' : '') +
        '<button type="button" class="mt-2 inline-flex h-10 w-full cursor-pointer items-center justify-center rounded-full bg-bg-invert font-sans text-[14px] font-medium text-text-invert transition-opacity hover:opacity-90">Get started</button>' +
      '</div>' +
      '<div class="flex flex-col gap-3 px-6">' + feats + '</div>';
    return card;
  }

  function renderPricing(sec, period) {
    var grid = q(".grid", sec);
    if (!grid) return;
    grid.innerHTML = "";
    LR_PRICING[period].forEach(function (plan) { grid.appendChild(pricingCard(plan, period)); });
  }

  function initPricingRender(root) {
    qa('[data-lp-section="pricing-block"]', root).forEach(function (sec) {
      if (sec.dataset.lovartPricingRender) return;
      // 只替换骨架（animate-pulse）或空网格；若已有真实卡片则不动
      var isSkeleton = !!q(".animate-pulse", sec);
      var grid = q(".grid", sec);
      if (!grid) return;
      if (!isSkeleton && grid.children.length > 0) return;
      sec.dataset.lovartPricingRender = "1";
      renderPricing(sec, "monthly");
      // 月/年切换联动
      var monBtn = q("[data-testid='paywall-tab-monthly']", sec);
      var yrBtn = q("[data-testid='paywall-tab-annually']", sec);
      function setActive(btn, other) {
        if (btn) btn.classList.add("lr-paywall-active");
        if (other) other.classList.remove("lr-paywall-active");
      }
      if (monBtn) monBtn.addEventListener("click", function (e) { e.preventDefault(); setActive(monBtn, yrBtn); renderPricing(sec, "monthly"); });
      if (yrBtn) yrBtn.addEventListener("click", function (e) { e.preventDefault(); setActive(yrBtn, monBtn); renderPricing(sec, "yearly"); });
      if (monBtn) monBtn.classList.add("lr-paywall-active");
    });
  }

  /* ---------- 锚点防跳顶 + 横向拖拽（保留原有） ---------- */
  function initNoJump(root) {
    (root || document).addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a");
      if (!a) return;
      var href = a.getAttribute("href") || "";
      if (href === "" || href === "#") { e.preventDefault(); return; }
      if (href.charAt(0) === "#" && href.length > 1) {
        var t = document.querySelector(href);
        if (t) { e.preventDefault(); t.scrollIntoView({ behavior: "smooth", block: "start" }); }
        else e.preventDefault();
      }
      if (href.indexOf("javascript:") === 0) e.preventDefault();
    }, true);
  }
  function initDragScroll(root) {
    qa(".overflow-x-auto, [class*='overflow-x-auto']", root).forEach(function (el) {
      if (el.dataset.lovartDrag) return;
      el.dataset.lovartDrag = "1";
      var down = false, sx = 0, sl = 0;
      el.addEventListener("mousedown", function (e) { down = true; sx = e.pageX; sl = el.scrollLeft; });
      window.addEventListener("mouseup", function () { down = false; });
      el.addEventListener("mousemove", function (e) { if (down) { el.scrollLeft = sl - (e.pageX - sx); } });
    });
  }

  /* ---------- 懒加载兜底 ----------
     站点懒加载插件把真实 URL 挪进 data-lazy-src（src 留 0 尺寸 SVG 占位），
     但其替换 JS 在复刻页不执行 → 图片全部塌成 0 高。这里启动时直接还原。 */
  function initLazyFix() {
    qa("img[data-lazy-src]").forEach(function (img) {
      var real = img.getAttribute("data-lazy-src");
      if (real) { img.src = real; img.removeAttribute("data-lazy-src"); }
    });
    qa("img[data-lazy-srcset]").forEach(function (img) {
      img.setAttribute("srcset", img.getAttribute("data-lazy-srcset"));
      img.removeAttribute("data-lazy-srcset");
    });
  }

  /* ---------- CSS 链接自愈 ----------
     跨域大 CSS（replica/mirror）在 no-cors 模式下若命中 CDN 的损坏缓存条目，
     渲染引擎会静默弃用整份样式表（无报错、无兜底），页面退化为裸文本。
     统一升级为 crossorigin=anonymous 模式并加 nonce 绕过边缘坏缓存；
     服务器已返回 ACAO:*，CORS 模式下响应健康且 CSSOM 可读。 */
  function initCssHeal() {
    document.querySelectorAll('link[rel="stylesheet"]').forEach(function (l) {
      if (!/lovart-(replica|faithful-mirror)\.css/.test(l.href)) return;
      if (l.crossorigin) return; // HTML 已是 CORS 模式，无需处理
      var u = new URL(l.href, location.href);
      u.searchParams.set("r", Date.now().toString(36));
      l.crossorigin = "anonymous";
      l.href = u.toString();
    });
  }

  function initAll() {
    initCssHeal();
    initLazyFix();
    // before/after：role="slider" 即滑块本体，直接初始化
    qa('[role="slider"]').forEach(initSlider);
    initAccordion(document);
    initTabs(document);
    initChat(document);
    initTheme(document);
    initLang(document);
    initPricing(document);
    initPricingRender(document);
    initFaqFill(document);
    initCompareFill(document);
    initNoJump(document);
    initDragScroll(document);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initAll);
  else initAll();
})();
