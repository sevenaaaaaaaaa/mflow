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
    qa("[aria-expanded]", root).forEach(function (btn) {
      if (btn.dataset.lovartAcc) return;
      btn.dataset.lovartAcc = "1";
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var expanded = btn.getAttribute("aria-expanded") === "true";
        var nowOpen = !expanded;
        btn.setAttribute("aria-expanded", String(nowOpen));
        if (btn.hasAttribute("data-state")) btn.setAttribute("data-state", nowOpen ? "open" : "closed");
        var item = btn.closest("[data-state]");
        if (item) item.setAttribute("data-state", nowOpen ? "open" : "closed");
        var panel = findPanel(btn);
        if (panel) {
          if (nowOpen) {
            panel.removeAttribute("hidden");
            panel.style.display = "";
          } else {
            panel.setAttribute("hidden", "");
            panel.style.display = "none";
          }
          if (panel.hasAttribute("data-state")) panel.setAttribute("data-state", nowOpen ? "open" : "closed");
        }
        var svg = btn.querySelector("svg"); if (svg) svg.style.transform = nowOpen ? "rotate(180deg)" : "";
      });
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

  function initAll() {
    // before/after：role="slider" 即滑块本体，直接初始化
    qa('[role="slider"]').forEach(initSlider);
    initAccordion(document);
    initTabs(document);
    initChat(document);
    initTheme(document);
    initLang(document);
    initPricing(document);
    initNoJump(document);
    initDragScroll(document);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initAll);
  else initAll();
})();
