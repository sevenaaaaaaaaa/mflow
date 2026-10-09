#!/usr/bin/env node
// faithful-batch-import.js — 幂等批量导入忠实页面（经 ego-browser 运行）。
// 用法：把批次写入 /tmp/faithful-batch.txt（逗号分隔 name），然后
//   ego-browser nodejs < faithful-batch.importer
// 或在本文件内联 NAMES 变量后用 ego-browser nodejs -e "$(cat faithful-batch-import.js)"
const task = await taskSpace(28);
const page = task.page("p1");
await page.goto("https://blogs.lovart.ai/wp-admin/");
await page.waitForLoadState();
const names = (process.env.NAMES || "").split(",").filter(Boolean);
if (!names.length) { console.log("用法: NAMES=name1,name2 ... ego-browser nodejs < faithful-batch-import.js"); process.exit(0); }
const r = await page.evaluate(async (names) => {
  const n = await fetch("/wp-admin/admin-ajax.php?action=rest-nonce").then(r => r.text());
  const H = { "Content-Type": "application/json", "X-WP-Nonce": n };
  const out = [];
  for (const name of names) {
    const title = "LR Faithful — " + name.replace("replica-", "").replace(/-/g, " ");
    const q = await fetch("/wp-json/wp/v2/pages?search=" + encodeURIComponent(title) + "&status=draft&per_page=5&_fields=id,title", { headers: H });
    const hits = (await q.json()).filter(p => p.title === title);
    let id = hits[0]?.id;
    let created = false;
    if (!id) {
      const cr = await fetch("/wp-json/wp/v2/pages", { method: "POST", headers: H, body: JSON.stringify({ title, status: "draft" }) });
      const pj = await cr.json();
      if (!pj.id) { out.push({ name, error: "create failed" }); continue; }
      id = pj.id; created = true;
    }
    const rd = await fetch("/wp-admin/admin-ajax.php", {
      method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: "action=lr_elem_read&page_id=" + id + "&secret=lrb-2026-x7k9"
    });
    const rj = await rd.json();
    const hasData = !!(rj.success && rj.data && rj.data.data && JSON.stringify(rj.data.data).length > 500);
    if (hasData) { out.push({ name, id, status: "已导入" }); continue; }
    const imp = await fetch("/wp-admin/admin-ajax.php", {
      method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: "action=lr_elem_import&page_id=" + id + "&url=" + encodeURIComponent("https://nownexts.com/lr-assets/elem/faithful/" + name + ".json?cb=" + Date.now()) + "&nomark=1&secret=lrb-2026-x7k9"
    });
    out.push({ name, id, created, ok: (await imp.text()).includes("success") });
  }
  return out;
}, names);
console.log(JSON.stringify(r));
