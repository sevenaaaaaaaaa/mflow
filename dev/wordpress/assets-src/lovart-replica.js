/**
 * lovart-replica.js — blogs.lovart.ai 复刻页共享交互 bundle（v3）
 *
 * v1 来源：replica-homepage 已验证 inline JS（before/after 滑块、FAQ 手风琴、
 *          锚点防跳顶、横向拖拽）。
 * v3 增强（针对忠实模块页交互缺失）：
 * v16（2026-10-12）：FAQ 答案固化为真实数据——12 复刻页换 eael-adv-accordion、
 *     4 个 native demo 页答案服务端写入 accordion tab_content；
 *     据此删除运行时注入 initFaqFill 及数据表 LR_FAQ_ANSWERS。
 *     pageSlug 保留（initCompareFill 仍用）。
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

  /* ---------- 页面 slug（剥 replica- / lr-demo- 前缀，供 initCompareFill 取数据键） ---------- */
  function pageSlug() {
    // 支持 17 页（replica- / replica-solution-）与 demo 页（lr-demo-native- / lr-demo-faithful-）
    var m = location.pathname.match(/(?:replica-(?:solution-)?|lr-demo-(?:native|faithful)-)([a-z0-9-]+)\/?$/i);
    var slug = m ? m[1] : null;
    if (!slug) return null;
    // demo 页短别名 → 定制内容键
    var ALIAS = {
      "fitness": "ai-design-for-fitness-wellness-hub",
      "wellness": "ai-design-for-fitness-wellness-hub",
      "small-biz": "ai-design-for-small-business-hub",
      "small-business": "ai-design-for-small-business-hub",
      "shopify": "ai-design-solution-for-shopify",
      "saas": "ai-design-solution-for-saas",
      "agencies": "ai-design-solution-for-agencies",
      "creators": "ai-design-solution-for-creators",
      "marketing-teams": "ai-design-solution-for-marketing-teams",
      "nonprofits": "ai-design-solution-for-nonprofits",
      "business-owners": "good-design-for-business-owners",
      "marketers": "good-design-for-marketers"
    };
    return ALIAS[slug] || slug;
  }

  /* ---------- 对比表内容注入 ----------
     6 个 solution 页的 comparison-table 表体为空壳且每行缺 Lovart 高亮列。
     按 slug 注入 LR_COMPARE 内容；td 不足 4 个时补建 Lovart 列（沿用满表的
     高亮类名）；data 提供 h2/sub 时订正源站张冠李戴的标题文案。 */
  var LOVART_TD_CLASS = "h-[72px] px-3 align-middle font-sans text-[13px] md:px-6 md:text-[14px] bg-bg-base-secondary text-text-default font-medium border-border-neutral-l2 border-l border-b";
  function initCompareFill(root) {
    var data = (window.LR_COMPARE || {})[pageSlug()];
    if (!data || !data.rows || !data.rows.length) return;
    var sec = q('[data-lp-section="comparison-table"]', root) || q(".lr-native-comparison-table", root);
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
  var LR_PRICING = {
    "monthly": [
      {"name":"Starter","price":19,"original":19,"off":"","bill":"Billed monthly","save":"Save $36 with annual billing","feats":["2000 Credits monthly","2000 extra credits first month","~40 Agent conversations","~500 GPT images","~8000 Flux images","~111 Kling videos","Unlimited Trial Models","Commercial license"]},
      {"name":"Basic","price":32,"original":32,"off":"","bill":"Billed monthly","save":"Save $60 with annual billing","feats":["3500 Credits monthly","3500 extra credits first month","~35 Agent conversations","~438 GPT images","~7000 Flux images","~51 Kling videos","Unlimited Trial Models","Commercial license"]},
      {"name":"Pro","price":79,"original":90,"off":"12% off","bill":"Billed monthly, renews at $90/month next month","save":"Save $529 with annual billing","hot":true,"feats":["11000 Credits monthly","11000 extra credits first month","~110 Agent conversations","~1375 GPT images","~22000 Flux images","~162 Kling videos","Unlimited Trial Models","Commercial license"]},
      {"name":"Ultimate","price":169,"original":199,"off":"15% off","bill":"Billed monthly, renews at $199/month next month","save":"Save $1,050 with annual billing","feats":["22000 Credits monthly","22000 extra credits first month","~220 Agent conversations","~2750 GPT images","~44000 Flux images","~324 Kling videos","Unlimited Trial Models","Commercial license","Priority generation queue","Dedicated support"]}
    ],
    "yearly": [
      {"name":"Starter","price":16,"original":19,"off":"16% off","bill":"Billed annually, $192/year","save":"Save $36 compared to monthly","feats":["2000 Credits monthly","2000 extra credits first month","~40 Agent conversations","~500 GPT images","~8000 Flux images","~111 Kling videos","Unlimited Trial Models","Commercial license"]},
      {"name":"Basic","price":27,"original":32,"off":"16% off","bill":"Billed annually, $324/year","save":"Save $60 compared to monthly","feats":["3500 Credits monthly","3500 extra credits first month","~35 Agent conversations","~438 GPT images","~7000 Flux images","~51 Kling videos","Unlimited Trial Models","Commercial license"]},
      {"name":"Pro","price":45,"original":90,"off":"50% off","bill":"Billed annually, $540 first year, then $888/year","save":"Save $529 compared to monthly","hot":true,"feats":["11000 Credits monthly","11000 extra credits first month","~110 Agent conversations","~1375 GPT images","~22000 Flux images","~162 Kling videos","Unlimited Trial Models","Commercial license"]},
      {"name":"Ultimate","price":109,"original":199,"off":"45% off","bill":"Billed annually, $1,308 first year, then $1,992/year","save":"Save $1,050 compared to monthly","feats":["22000 Credits monthly","22000 extra credits first month","~220 Agent conversations","~2750 GPT images","~44000 Flux images","~324 Kling videos","Unlimited Trial Models","Commercial license","Priority generation queue","Dedicated support"]}
    ]
  };

  function pricingCard(plan, period) {
    var per = period === "yearly" ? "/mo" : "/month";
    var card = document.createElement("div");
    // 对齐真站：普通卡米白底；Pro 卡（hot）lime 高亮边框 + Most popular 徽章
    card.className = "relative mt-[30px] flex w-full flex-col gap-6 rounded-[16px] border pb-6 bg-bg-base-default " +
      (plan.hot ? "border-[#def479]" : "border-lo-border-neutral-l2");
    card.style.borderColor = plan.hot ? "rgb(222, 244, 121)" : "";
    var feats = plan.feats.map(function (f) {
      return '<div class="flex items-center gap-2">' +
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" class="shrink-0 text-text-default"><path d="M3 8.5l3.2 3L13 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
        '<span class="font-sans text-[13px] leading-[1.5] text-text-secondary">' + f + '</span></div>';
    }).join("");
    card.innerHTML =
      '<div class="border-lo-border-neutral-l2 flex flex-col gap-4 border-b p-6">' +
        '<div class="flex h-6 items-center gap-2"><span class="font-sans text-[16px] font-medium text-text-default">' + plan.name + '</span>' +
          (plan.off ? '<span class="font-sans text-[12px] font-medium text-text-secondary">' + plan.off + '</span>' : '') +
        '</div>' +
        '<div class="flex items-baseline gap-2"><span class="font-sans text-[32px] leading-none font-semibold text-text-default">$' + plan.price + '</span>' +
          (plan.original > plan.price ? '<span class="font-sans text-[16px] text-text-tertiary line-through">$' + plan.original + '</span>' : '') +
          '<span class="font-sans text-[13px] text-text-tertiary">' + per + '</span></div>' +
        '<div class="font-sans text-[12px] leading-[1.5] text-text-tertiary">' + plan.bill + '</div>' +
        (plan.hot ? '<span class="absolute left-1/2 -top-3 -translate-x-1/2 whitespace-nowrap rounded-full px-3 py-1 font-sans text-[12px] font-medium" style="background:rgb(222, 244, 121);color:#111">Most popular</span>' : '') +
        '<button type="button" class="mt-2 inline-flex h-10 w-full cursor-pointer items-center justify-center rounded-full border border-lo-border-neutral-l2 bg-bg-special-white font-sans text-[14px] font-medium text-text-default transition-colors hover:bg-lo-bg-overlay-hover">Get ' + plan.name + ' now</button>' +
      '</div>' +
      '<div class="flex flex-col gap-3 px-6">' +
        '<div class="font-sans text-[13px] font-medium text-text-default">' + plan.save + '</div>' + feats +
      '</div>';
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
      // 真站默认 annual（折扣展示态）
      renderPricing(sec, "yearly");
      // 月/年切换联动
      var monBtn = q("[data-testid='paywall-tab-monthly']", sec);
      var yrBtn = q("[data-testid='paywall-tab-annually']", sec);
      function setActive(btn, other) {
        if (btn) btn.classList.add("lr-paywall-active");
        if (other) other.classList.remove("lr-paywall-active");
      }
      if (monBtn) monBtn.addEventListener("click", function (e) { e.preventDefault(); setActive(monBtn, yrBtn); renderPricing(sec, "monthly"); });
      if (yrBtn) yrBtn.addEventListener("click", function (e) { e.preventDefault(); setActive(yrBtn, monBtn); renderPricing(sec, "yearly"); });
      if (yrBtn) yrBtn.classList.add("lr-paywall-active");
    });
  }

  /* ---------- 链接与 CTA 生产化 ----------
     1) 无跳转的 CTA button（Get started / Get X now / Try Lovart today）→ 跳 lovart.ai/canvas
     2) href="#" 死链：试用意图跳 /canvas；指引意图滚动到工作流/能力展示区块
     3) 外链清理：?cb= 缓存参数移除；真站 404 死链改道
     4) 源模板设计说明文字泄漏（"cta · bgStyle: ..."）藏除 */
  var LR_CANVAS = "https://www.lovart.ai/canvas";
  var LR_LINK_REDIRECT = {
    "https://www.lovart.ai/blog/shopify-ai-design-agent-vs-generator": "https://www.lovart.ai/blog",
    "https://www.lovart.ai/blog/shopify-pdp-creative-refresh-plan": "https://www.lovart.ai/blog",
    "https://www.lovart.ai/blog/shopify-brand-kit-consistency": "https://www.lovart.ai/blog",
    "https://www.lovart.ai/nonprofit": "https://www.lovart.ai/solutions/ai-design-solution-for-nonprofits"
  };
  function initLinkFix(root) {
    // 只处理复刻内容（scope 或 .lr 容器内），不动 WordPress 界面元素
    var scopes = qa(".lovart-replica-scope, .lr", root);
    scopes.forEach(function (scope) {
      // 1) CTA button
      qa("button", scope).forEach(function (b) {
        if (b.dataset.lovartCta) return;
        var t = (b.textContent || "").trim();
        if (!/^(get started|get started for free|get [\w ]+ now|try lovart today|start free)$/i.test(t)) return;
        b.dataset.lovartCta = "1";
        b.style.cursor = "pointer";
        b.addEventListener("click", function (e) { e.preventDefault(); window.location.href = LR_CANVAS; });
      });
      // 2) 死链 #
      qa('a[href="#"], a[href=""]', scope).forEach(function (a) {
        if (a.dataset.lovartLink) return;
        a.dataset.lovartLink = "1";
        var t = (a.textContent || "").trim();
        if (/try|pick a|start/i.test(t)) {
          a.setAttribute("href", LR_CANVAS);
        } else {
          a.style.cursor = "pointer";
          a.addEventListener("click", function (e) {
            e.preventDefault();
            var target = q('[data-lp-section="workflow-horizontal"], [data-lp-section="workflow-vertical"], [data-lp-section="capability-tabs"], [data-lp-section="showcase-stacked"]', document);
            if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
            else window.location.href = LR_CANVAS;
          });
        }
      });
      // 3) 外链清理与改道
      qa("a[href]", scope).forEach(function (a) {
        if (a.dataset.lovartLink) return;
        var raw = a.getAttribute("href") || "";
        if (LR_LINK_REDIRECT[raw]) { a.setAttribute("href", LR_LINK_REDIRECT[raw]); a.dataset.lovartLink = "1"; return; }
        if (/[?&]cb=\d+/.test(raw)) { a.setAttribute("href", raw.replace(/[?&]cb=\d+/g, "")); a.dataset.lovartLink = "1"; }
      });
      // 4) 设计说明文字泄漏
      qa("p, span, div", scope).forEach(function (p) {
        if (p.dataset.lovartLeak || p.children.length) return;
        var t = (p.textContent || "").trim();
        if (/^(cta|section|block|hero|card)\s*[·・:\-]\s*(bgStyle|bg|style|layout)\s*:/i.test(t)) {
          p.dataset.lovartLeak = "1";
          p.style.display = "none";
        }
      });
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
    initLinkFix(document);
    // before/after：role="slider" 即滑块本体，直接初始化
    qa('[role="slider"]').forEach(initSlider);
    initAccordion(document);
    initTabs(document);
    initChat(document);
    initTheme(document);
    initLang(document);
    initPricing(document);
    initPricingRender(document);
    initCompareFill(document);
    initNoJump(document);
    initDragScroll(document);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initAll);
  else initAll();
})();
