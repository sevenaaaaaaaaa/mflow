/**
 * lovart-replica.js — blogs.lovart.ai 复刻页共享交互 bundle（v1）
 * 来源：replica-homepage 已验证的 inline JS（4088 字节，原样保留）。
 * 覆盖：before/after 滑块、FAQ 手风琴（aria-expanded）、# 锚点防跳顶、
 *       横向滚动区拖拽。solutions 页此前完全没有 JS——点击 bug 的直接修复。
 */

(function () {
  function q(sel, root) { return (root || document).querySelector(sel); }
  function initSlider(sec) {
    if (!sec || sec.dataset.lovartSlider) return;
    var slider = q('[role="slider"]', sec);
    if (!slider) return;
    sec.dataset.lovartSlider = "1";
    var clipLayer = null, line = null;
    sec.querySelectorAll("[style*='clip-path']").forEach(function (el) { clipLayer = el; });
    sec.querySelectorAll("[style*='left:50%'], [style*='left: 50%']").forEach(function (el) { line = el; });
    function setPct(pct) {
      if (!isFinite(pct)) return;
      pct = Math.min(100, Math.max(0, pct));
      slider.setAttribute("aria-valuenow", pct.toFixed(0));
      if (clipLayer) clipLayer.style.clipPath = "inset(0 " + (100 - pct).toFixed(2) + "% 0 0)";
      if (line) line.style.left = pct.toFixed(2) + "%";
    }
    var dragging = false;
    slider.addEventListener("pointerdown", function (e) {
      dragging = true;
      try { slider.setPointerCapture(e.pointerId); } catch (err) {}
      setPct(((e.clientX || rect().left+1) - rect().left) / (rect().width || 1) * 100);
    });
    slider.addEventListener("pointermove", function (e) { if (dragging) { e.preventDefault(); setPct(((e.clientX || 0) - rect().left) / (rect().width || 1) * 100); } });
    function rect() { return sec.getBoundingClientRect(); }
    slider.addEventListener("pointerup", function () { dragging = false; });
    slider.addEventListener("pointercancel", function () { dragging = false; });
  }
  function initAccordion(root) {
    (root || document).querySelectorAll("[aria-expanded]").forEach(function (btn) {
      if (btn.dataset.lovartAcc) return;
      btn.dataset.lovartAcc = "1";
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var expanded = btn.getAttribute("aria-expanded") === "true";
        btn.setAttribute("aria-expanded", String(!expanded));
        var item = btn.closest("[data-state]") || btn.parentElement;
        if (item && item.hasAttribute("data-state")) item.setAttribute("data-state", expanded ? "closed" : "open");
        var ctrl = btn.getAttribute("aria-controls");
        var panel = ctrl ? document.getElementById(ctrl) : (btn.parentElement.nextElementSibling || null);
        if (panel) {
          if (expanded) { panel.style.display = "none"; panel.setAttribute("hidden", ""); }
          else { panel.style.display = ""; panel.removeAttribute("hidden"); }
        }
        var svg = btn.querySelector("svg"); if (svg) svg.style.transform = expanded ? "" : "rotate(180deg)";
      });
    });
  }
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
    (root || document).querySelectorAll(".overflow-x-auto, [class*='overflow-x-auto']").forEach(function (el) {
      if (el.dataset.lovartDrag) return;
      el.dataset.lovartDrag = "1";
      var down = false, sx = 0, sl = 0;
      el.addEventListener("mousedown", function (e) { down = true; sx = e.pageX; sl = el.scrollLeft; });
      window.addEventListener("mouseup", function () { down = false; });
      el.addEventListener("mousemove", function (e) { if (down) { el.scrollLeft = sl - (e.pageX - sx); } });
    });
  }
  function initAll() {
    document.querySelectorAll('[data-lp-section="comparison-before-after"]').forEach(initSlider);
    initAccordion(document);
    initNoJump(document);
    initDragScroll(document);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initAll);
  else initAll();
})();

