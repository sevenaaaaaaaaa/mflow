#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the LPagery v1 Elementor-native seed and three boundary CSV rows."""
from __future__ import print_function

import csv
import importlib.util
import io
import json
import os


ROOT = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    "lr_native", os.path.join(ROOT, "build-elementor-native.py"))
N = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(N)


def native_section(ids, kind, children, title):
    return N.native_root(ids, kind, children, title)


def build_seed():
    ids = N.IdFactory("lp-lr-native-v1")

    hero_copy = N.container(ids, [
        N.text(ids, "{hero_eyebrow}", "Hero eyebrow"),
        N.heading(ids, "{hero_title}", "h1", "Hero title"),
        N.heading(ids, "{hero_subtitle}", "h2", "Hero subtitle"),
        N.text(ids, "{hero_body}", "Hero body"),
        N.container(ids, [
            N.button(ids, "{primary_cta_label}", "{primary_cta_url}",
                     "Primary CTA", "primary"),
            N.button(ids, "{secondary_cta_label}", "{secondary_cta_url}",
                     "Secondary CTA", "secondary"),
        ], "lr-native-buttons", "row"),
    ], "lr-native-copy")
    hero_media = N.container(ids, [
        N.image(ids, "{hero_media_url}", "{hero_media_alt}", "Hero image")
    ], "lr-native-media")
    hero = native_section(ids, "hero-split", [
        N.container(ids, [hero_copy, hero_media],
                    "lr-native-columns", "row")
    ], "LPagery Hero")

    stat_cards = []
    for i in range(1, 5):
        stat_cards.append(N.container(ids, [
            N.heading(ids, "{stat_%d_value}" % i, "div",
                      "Stat %d value" % i),
            N.text(ids, "{stat_%d_label}" % i, "Stat %d label" % i),
        ], "lr-native-card lr-native-stat"))
    stats = native_section(ids, "stats", [
        N.container(ids, stat_cards, "lr-native-grid lr-native-grid-4", "row")
    ], "LPagery Stats")

    proof_cards = []
    for i in range(1, 5):
        proof_cards.append(N.container(ids, [
            N.heading(ids, "{proof_%d_title}" % i, "h3",
                      "Proof %d title" % i),
            N.text(ids, "{proof_%d_body}" % i, "Proof %d body" % i),
        ], "lr-native-card"))
    proof = native_section(ids, "proof-block", [
        N.heading(ids, "{proof_title}", "h2", "Proof title"),
        N.container(ids, proof_cards, "lr-native-grid lr-native-grid-4", "row"),
    ], "LPagery Proof")

    review_cards = []
    for i in range(1, 5):
        review_cards.append(N.container(ids, [
            N.text(ids, "{review_%d_quote}" % i, "Review %d quote" % i),
            N.heading(ids, "{review_%d_name}" % i, "h3",
                      "Review %d name" % i),
            N.text(ids, "{review_%d_role}" % i, "Review %d role" % i),
        ], "lr-native-card"))
    reviews = native_section(ids, "review-grid-4col", [
        N.heading(ids, "{reviews_title}", "h2", "Reviews title"),
        N.container(ids, review_cards, "lr-native-grid lr-native-grid-4", "row"),
    ], "LPagery Reviews")

    portrait_cards = []
    for i in range(1, 5):
        portrait_cards.append(N.container(ids, [
            N.image(ids, "{portrait_%d_image_url}" % i,
                    "{portrait_%d_image_alt}" % i,
                    "Portrait %d image" % i),
            N.heading(ids, "{portrait_%d_title}" % i, "h3",
                      "Portrait %d title" % i),
            N.text(ids, "{portrait_%d_body}" % i, "Portrait %d body" % i),
        ], "lr-native-card"))
    portraits = native_section(ids, "portrait-grid-4", [
        N.heading(ids, "{portraits_title}", "h2", "Portraits title"),
        N.container(ids, portrait_cards,
                    "lr-native-grid lr-native-grid-4", "row"),
    ], "LPagery Portraits")

    tabs = []
    for i in range(1, 7):
        tabs.append({
            "_id": ids.next(),
            "tab_title": "{faq_%d_question}" % i,
            "tab_content": "<p>{faq_%d_answer}</p>" % i,
        })
    faq = native_section(ids, "faq", [
        N.heading(ids, "{faq_title}", "h2", "FAQ title"),
        N.widget(ids, "accordion", {
            "tabs": tabs,
            "selected_icon": {"value": "fas fa-chevron-down",
                              "library": "fa-solid"},
            "title_html_tag": "h3",
        }, "FAQ accordion"),
    ], "LPagery FAQ")

    # ---- v2 扩展（契约 native-modules/csv-contract.md v2）----
    # workflow：HT Mega Vertical Timeline，repeater custom_content_list
    wf_rows = []
    for i in range(1, 5):
        wf_rows.append({
            "_id": ids.next(),
            "content_date": "{workflow_%d_step}" % i,
            "content_title": "{workflow_%d_title}" % i,
            "content_text": "{workflow_%d_desc}" % i,
        })
    workflow = native_section(ids, "workflow-vertical", [
        N.heading(ids, "{workflow_title}", "h2", "Workflow title"),
        N.widget(ids, "htmega-verticletimeline-addons", {
            "custom_content_list": wf_rows,
            "verticle_timeline_layout": "1",
        }, "Workflow timeline"),
    ], "LPagery Workflow")

    # capability-tabs：EA Advanced Tabs，repeater eael_adv_tabs_tab（4 面板必填）
    tab_rows = []
    for i in range(1, 5):
        tab_rows.append({
            "_id": ids.next(),
            "eael_adv_tabs_tab_title": "{tabs_%d_title}" % i,
            "eael_adv_tabs_tab_content": "{tabs_%d_html}" % i,
            "eael_adv_tabs_tab_id": "eael-tab-%d" % i,
            "eael_adv_tabs_tab_show_as_default":
                "active-default" if i == 1 else "inactive",
            "eael_adv_tabs_text_type": "content",
            "eael_adv_tabs_tab_title_html_tag": "span",
        })
    cap_tabs = native_section(ids, "capability-tabs", [
        N.heading(ids, "{tabs_title}", "h2", "Capability tabs title"),
        N.widget(ids, "eael-adv-tabs", {
            "eael_adv_tabs_tab": tab_rows,
        }, "Capability tabs"),
    ], "LPagery Capability Tabs")

    # testimonial：HT Mega 2026 Testimonials，repeater testimonial_items（3 条/页）
    tm_rows = []
    for i in range(1, 4):
        tm_rows.append({
            "_id": ids.next(),
            "quote_text": "{review_%d_quote}" % i,
            "rating": "5",
            "author_name": "{review_%d_name}" % i,
            "author_role": "{review_%d_role}" % i,
            "author_company": "",
        })
    testimonial = native_section(ids, "testimonial", [
        N.widget(ids, "htmega-2026-testimonials", {
            "testimonial_items": tm_rows,
        }, "Testimonials"),
    ], "LPagery Testimonials")

    # pricing：HT Mega 2026 Pricing，repeater plan_items —— 双价列（月/年同行）
    PLANS = ["starter", "basic", "pro", "ultimate"]
    plan_rows = []
    for plan in PLANS:
        featured = plan == "pro"
        plan_rows.append({
            "_id": ids.next(),
            "plan_name": "{pricing_%s_name}" % plan,
            "is_featured": "yes" if featured else "no",
            "featured_badge": "Most popular" if featured else "",
            "currency": "$",
            "price_monthly": "{pricing_%s_monthly}" % plan,
            "price_annual": "{pricing_%s_annual}" % plan,
            "period": "/month",
            "tagline": "{pricing_%s_tagline}" % plan,
            "features": "{pricing_%s_features}" % plan,
            "cta_text": "Get started",
            "cta_url": {"url": "https://www.lovart.ai/canvas",
                        "is_external": "", "nofollow": ""},
            "cta_variant": "primary",
        })
    pricing = native_section(ids, "pricing-block", [
        N.heading(ids, "{pricing_title}", "h2", "Pricing title"),
        N.widget(ids, "htmega-2026-pricing", {
            "plan_items": plan_rows,
        }, "Pricing"),
    ], "LPagery Pricing")

    # comparison-table：EA Advanced Data Table —— 单 blob（无行列级字段）
    comparison = native_section(ids, "comparison-table", [
        N.heading(ids, "{compare_title}", "h2", "Comparison title"),
        N.widget(ids, "eael-advanced-data-table", {
            "ea_adv_data_table_source": "static",
            "ea_adv_data_table_static_html": "{compare_rows_html}",
            "ea_adv_data_table_body_highlight": "last-col",
            "ea_adv_data_table_body_l_col_highlight_background": "#f2f1ee",
            "ea_adv_data_table_body_l_col_highlight_color": "#171612",
        }, "Comparison table"),
    ], "LPagery Comparison")

    cta = native_section(ids, "cta-default", [
        N.container(ids, [
            N.heading(ids, "{final_cta_title}", "h2", "Final CTA title"),
            N.text(ids, "{final_cta_body}", "Final CTA body"),
            N.button(ids, "{final_cta_label}", "{final_cta_url}",
                     "Final CTA", "primary"),
        ], "lr-native-cta-card")
    ], "LPagery Final CTA")

    return {"version": "3.35.7",
            "data": [hero, stats, proof, reviews, portraits, faq, workflow,
                     cap_tabs, testimonial, pricing, comparison, cta]}


FIELDNAMES = [
    "page_title", "slug", "industry", "audience",
    "hero_eyebrow", "hero_title", "hero_subtitle", "hero_body",
    "hero_media_url", "hero_media_alt",
    "primary_cta_label", "primary_cta_url",
    "secondary_cta_label", "secondary_cta_url",
    "proof_title", "reviews_title", "portraits_title", "faq_title",
    "final_cta_title", "final_cta_body", "final_cta_label", "final_cta_url",
    "seo_title", "meta_description", "canonical_url",
] + sum((["stat_%d_value" % i, "stat_%d_label" % i] for i in range(1, 5)), []) \
  + sum((["proof_%d_title" % i, "proof_%d_body" % i] for i in range(1, 5)), []) \
  + sum((["review_%d_quote" % i, "review_%d_name" % i,
          "review_%d_role" % i] for i in range(1, 5)), []) \
  + sum((["portrait_%d_image_url" % i, "portrait_%d_image_alt" % i,
          "portrait_%d_title" % i, "portrait_%d_body" % i]
         for i in range(1, 5)), []) \
  + sum((["faq_%d_question" % i, "faq_%d_answer" % i]
         for i in range(1, 7)), []) \
  + ["workflow_title"] \
  + sum((["workflow_%d_step" % i, "workflow_%d_title" % i, "workflow_%d_desc" % i]
         for i in range(1, 5)), []) \
  + ["tabs_title"] \
  + sum((["tabs_%d_title" % i, "tabs_%d_html" % i] for i in range(1, 5)), []) \
  + sum((["review_%d_quote" % i, "review_%d_name" % i, "review_%d_role" % i]
         for i in range(1, 4)), []) \
  + ["pricing_title"] \
  + sum((["pricing_%s_name" % p, "pricing_%s_monthly" % p, "pricing_%s_annual" % p,
          "pricing_%s_tagline" % p, "pricing_%s_features" % p]
         for p in ("starter", "basic", "pro", "ultimate")), []) \
  + ["compare_title", "compare_rows_html"]  # v2（csv-contract.md v2）


def row(name, audience, slug, long=False):
    image = "https://www.lovart.ai/assets/use-cases/social-media/how-to.png"
    r = {key: "" for key in FIELDNAMES}
    r.update({
        "page_title": "The Best AI Design Agent for %s" % name,
        "slug": slug, "industry": name, "audience": audience,
        "hero_eyebrow": "%s DESIGN SYSTEM" % name.upper(),
        "hero_title": "Turn one %s brief into a complete campaign" % name,
        "hero_subtitle": "Native Elementor modules, powered by Lovart",
        "hero_body": ("A deliberately long boundary paragraph that verifies responsive "
                      "wrapping, card growth, and LPagery replacement without clipping. "
                      "Every word remains editable in Elementor after generation."
                      if long else
                      "Create on-brand assets for %s without rebuilding every page." % audience),
        "hero_media_url": image, "hero_media_alt": "%s campaign example" % name,
        "primary_cta_label": "Start designing", "primary_cta_url": "https://www.lovart.ai/",
        "secondary_cta_label": "See examples", "secondary_cta_url": "https://www.lovart.ai/explore",
        "proof_title": "Built for %s" % audience,
        "reviews_title": "What %s say" % audience,
        "portraits_title": "Four workflows to launch faster",
        "faq_title": "Frequently asked questions",
        "final_cta_title": "Ready to scale your %s creative?" % name,
        "final_cta_body": "Use one reusable Elementor system for every campaign.",
        "final_cta_label": "Build the campaign", "final_cta_url": "https://www.lovart.ai/",
        "seo_title": "AI Design Agent for %s | Lovart" % name,
        "meta_description": "Create editable %s campaign assets with Lovart." % name,
        "canonical_url": "https://blogs.lovart.ai/%s" % slug,
    })
    for i in range(1, 5):
        r["stat_%d_value" % i] = [ "1", "10+", "4", "∞" ][i - 1]
        r["stat_%d_label" % i] = [
            "Shared context", "Asset formats", "Editable modules", "Variants"
        ][i - 1]
        r["proof_%d_title" % i] = "Proof point %d" % i
        r["proof_%d_body" % i] = "A native Elementor proof card for %s." % name
        r["review_%d_quote" % i] = "Lovart shortened our creative cycle."
        r["review_%d_name" % i] = "Customer %d" % i
        r["review_%d_role" % i] = "%s team" % name
        r["portrait_%d_image_url" % i] = image
        r["portrait_%d_image_alt" % i] = "%s workflow %d" % (name, i)
        r["portrait_%d_title" % i] = "Workflow %d" % i
        r["portrait_%d_body" % i] = "Editable content slot for %s." % audience
    for i in range(1, 7):
        r["faq_%d_question" % i] = "How does workflow %d help %s?" % (i, audience)
        r["faq_%d_answer" % i] = "It keeps content editable and reusable."
    # ---- v2 默认值 ----
    r["workflow_title"] = "How %s teams ship with Lovart" % name
    for i in range(1, 5):
        r["workflow_%d_step" % i] = str(i)
        r["workflow_%d_title" % i] = "Step %d" % i
        r["workflow_%d_desc" % i] = ("Describe step %d for %s — short noun phrases, "
                                     "Touch/Edit terms." % (i, name))
    r["tabs_title"] = "What %s teams make" % name
    for i in range(1, 5):
        r["tabs_%d_title" % i] = "Capability %d" % i
        r["tabs_%d_html" % i] = ('<div class="lr dark"><h3>Capability %d</h3>'
                                 '<p>Editable panel HTML for %s.</p></div>' % (i, name))
    for i in range(1, 4):
        r["review_%d_quote" % i] = "Lovart shortened our %s creative cycle." % name
        r["review_%d_name" % i] = "Customer %d" % i
        r["review_%d_role" % i] = "%s team" % name
    r["pricing_title"] = "Simple pricing for %s" % name
    plans = {"starter": ("19", "16", "Save $36 compared to monthly",
                         "Billed annually, $192/year\n2000 Credits monthly"),
             "basic": ("32", "27", "Save $60 compared to monthly",
                       "Billed annually, $324/year\n3500 Credits monthly"),
             "pro": ("79", "45", "<s>$90</s> 12% off \u00b7 Save $529 compared to monthly",
                     "Billed annually, $540 first year\n11000 Credits monthly"),
             "ultimate": ("169", "99", "<s>$199</s> \u00b7 Save $1,059 compared to monthly",
                          "Billed annually, $1,188 first year\n26000 Credits monthly")}
    for p_, (mo, an, tg, ft) in plans.items():
        r["pricing_%s_name" % p_] = p_.capitalize()
        r["pricing_%s_monthly" % p_] = mo
        r["pricing_%s_annual" % p_] = an
        r["pricing_%s_tagline" % p_] = tg
        r["pricing_%s_features" % p_] = ft
    r["compare_title"] = "Lovart vs common ways to produce %s creative" % name
    r["compare_rows_html"] = ("<thead><tr><th>Need</th><th>Old way</th><th>Tools</th>"
                              "<th>Lovart</th></tr></thead><tbody>"
                              "<tr><td>Brief to draft</td><td>Days</td><td>Manual</td>"
                              "<td>Minutes</td></tr></tbody>")
    return r


def main():
    out = os.path.join(ROOT, "native-modules")
    if not os.path.isdir(out):
        os.makedirs(out)
    full_seed = build_seed()
    with io.open(os.path.join(out, "lp-lr-native-v1-pro.json"),
                 "w", encoding="utf-8") as f:
        json.dump(full_seed, f, ensure_ascii=False)
    rows = [
        row("Bakery", "bakery owners", "lr-native-bakery-short"),
        row("SaaS", "growth teams", "lr-native-saas-long", long=True),
        row("Wellness", "studio owners", "lr-native-wellness-full"),
    ]
    with io.open(os.path.join(out, "lp-lr-native-v1-sample.csv"),
                 "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    # The installed LPagery Free build supports at most three source columns.
    # Keep industry/audience dynamic and use slug for URL generation; materialize
    # every other token with the first boundary row so no ignored token leaks.
    free_seed_text = json.dumps(full_seed, ensure_ascii=False)
    defaults = rows[0]
    for field, value in defaults.items():
        if field not in ("industry", "audience", "slug"):
            free_seed_text = free_seed_text.replace("{%s}" % field, value)
    free_seed_text = free_seed_text.replace(
        defaults["industry"], "{industry}").replace(
            defaults["audience"], "{audience}")
    with io.open(os.path.join(out, "lp-lr-native-v1-free.json"),
                 "w", encoding="utf-8") as f:
        f.write(free_seed_text)
    with io.open(os.path.join(out, "lp-lr-native-v1-free-sample.csv"),
                 "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["industry", "audience", "slug"])
        writer.writeheader()
        for source in rows:
            writer.writerow({key: source[key]
                             for key in ("industry", "audience", "slug")})

    # Materialized fixtures make the Free-plan output deterministic for audits
    # and provide a safe refresh path when Bulk Update (a Pro feature) is absent.
    fixtures = os.path.join(out, "lp-lr-native-v1-free-samples")
    if not os.path.isdir(fixtures):
        os.makedirs(fixtures)
    for source in rows:
        sample = free_seed_text
        for field in ("industry", "audience", "slug"):
            sample = sample.replace("{%s}" % field, source[field])
        with io.open(os.path.join(fixtures, source["slug"] + ".json"),
                     "w", encoding="utf-8") as f:
            f.write(sample)
    print("seed sections:", len(full_seed["data"]),
          "pro rows/columns:", len(rows), len(FIELDNAMES),
          "free rows/columns:", len(rows), 3)


if __name__ == "__main__":
    main()
