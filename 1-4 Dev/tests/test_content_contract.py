#!/usr/bin/env python3
"""内容契约单元测试（离线、无网络）：section 注册表 / 故事线顺序校验 / MD→PT 转换 /
blog 文档模型（_id 命名空间 + 三时间 + status）/ PT→MD 镜像。

运行：bash "1-4 Dev/scripts/run-tests.sh"（或 python3 "1-4 Dev/tests/test_content_contract.py"）
"""
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / "1-4 Dev" / "scripts" / "publish_adapters"
LIB = ROOT / "1-4 Dev" / "scripts" / "library"
sys.path.insert(0, str(PUB))
sys.path.insert(0, str(LIB))

from section_registry import validate_sections_full, validate_sections  # noqa: E402
import storylines  # noqa: E402
from sanity_publisher import (build_blog_doc, doc_id, md_to_sections, _iso,  # noqa: E402
                              registry_warnings)
from md_to_portable_text import md_to_portable_text, validate_portable_text_body  # noqa: E402
from pt_to_md import portable_text_to_md  # noqa: E402


def _write_md(case, fm_body, body):
    f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    f.write(f"---\n{fm_body}\n---\n\n{body}")
    f.close()
    case.addCleanup(os.unlink, f.name)
    return f.name


class TestSectionRegistry(unittest.TestCase):
    """注册表逐型字段校验：BLOCK 拦契约破坏，warnings 只建议。"""

    def test_good_minimal_page_zero_errors(self):
        sections = [
            {"type": "hero-split", "title": "T", "description": "d" * 30,
             "media": {"src": "https://cdn.example.com/a.jpg", "alt": "a"},
             "buttons": [{"text": "Go", "href": "/x", "variant": "primary"}]},
            {"type": "feature-grid", "columns": 3,
             "features": [{"title": "f1", "description": "x" * 20, "media": {"src": "https://cdn.example.com/b.jpg", "alt": "b"}},
                          {"title": "f2", "description": "y" * 20, "media": {"src": "https://cdn.example.com/c.jpg", "alt": "c"}}]},
            {"type": "faq", "title": "FAQ", "items": [{"question": "Q?", "answer": "A." * 10},
                                                      {"question": "Q2?", "answer": "B." * 10},
                                                      {"question": "Q3?", "answer": "C." * 10}]},
            {"type": "cta-default", "title": "Ready?",
             "buttons": [{"text": "Start", "href": "/go", "variant": "primary"}]},
        ]
        r = validate_sections_full(sections)
        self.assertEqual(r["errors"], [], r["errors"])

    def test_unknown_type_blocked_with_camelcase_hint(self):
        r = validate_sections_full([{"type": "comparisonTable", "title": "t"}])
        self.assertTrue(any("未注册" in e and "comparison-table" in e for e in r["errors"]))

    def test_legacy_type_blocked(self):
        r = validate_sections_full([{"type": "heroSection", "title": "t"}])
        self.assertTrue(any("legacy" in e for e in r["errors"]))

    def test_faq_pair_list_blocked(self):
        r = validate_sections_full([{"type": "faq", "title": "F", "items": [["q", "a"]]}])
        self.assertTrue(any("数对嵌套" in e for e in r["errors"]))

    def test_proof_block_with_stats_field_blocked(self):
        """实测错配形态：proof-block 误用 stats 字段（stats 是独立 type）。"""
        r = validate_sections_full([{"type": "proof-block", "title": "t",
                                     "stats": [{"value": "10", "label": "x"}]}])
        self.assertTrue(any("缺 cards" in e for e in r["errors"]))

    def test_pricing_plans_forbidden(self):
        r = validate_sections_full([{"type": "pricing-block", "title": "t", "plans": [{"name": "pro"}]}])
        self.assertTrue(any("plans" in e and "后端 SDK" in e for e in r["errors"]))

    def test_icon_whitelist_enforced(self):
        r = validate_sections_full([{"type": "cluster-block-dense", "title": "t",
                                     "cards": [{"icon": "sparkles", "title": "x", "description": "y"}]}])
        self.assertTrue(any("icon" in e and "sparkles" in e for e in r["errors"]))
        ok = validate_sections_full([{"type": "cluster-block-dense", "title": "t",
                                      "cards": [{"icon": "sparkle", "title": "x", "description": "y"}]}])
        self.assertEqual([e for e in ok["errors"] if "icon" in e], [])

    def test_relative_media_src_blocked_and_missing_alt_is_warning(self):
        r = validate_sections_full([{"type": "hero-mosaic", "title": "t",
                                     "mosaicTiles": [{"title": "m", "media": {"src": "images/rel.png"}}]}])
        self.assertTrue(any("非绝对 URL" in e for e in r["errors"]))
        self.assertTrue(any("alt" in w for w in r["warnings"]))

    def test_columns_enum_and_canvas_wall_are_warnings(self):
        r = validate_sections_full([{"type": "feature-grid", "columns": 5,
                                     "features": [{"title": "f", "media": {"src": "https://cdn.example.com/a.jpg", "alt": "a"}}]}])
        self.assertTrue(any("columns" in w for w in r["warnings"]))
        self.assertEqual(r["errors"], [])
        r2 = validate_sections_full([{"type": "canvas-wall", "title": "t",
                                      "items": [{"media": {"src": "https://cdn.example.com/a.jpg", "alt": "a"}}]}])
        self.assertTrue(any("10" in w for w in r2["warnings"]))

    def test_image_only_type_rejects_video(self):
        r = validate_sections_full([{"type": "media-marquee", "title": "t",
                                     "items": [{"src": "https://cdn.example.com/a.mp4"}]}])
        self.assertTrue(any("仅支持图片" in e for e in r["errors"]))

    def test_buttons_contract(self):
        base = {"type": "cta-default", "title": "t"}
        r = validate_sections_full([dict(base, buttons=[{"href": "/x"}])])
        self.assertTrue(any("缺 text" in e for e in r["errors"]))
        r2 = validate_sections_full([dict(base, buttons=[{"text": "a", "variant": "ghost", "href": "/x"}])])
        self.assertTrue(any("variant" in e for e in r2["errors"]))
        r3 = validate_sections_full([dict(base, buttons=[{"text": "a"}])])
        self.assertTrue(any("#" in w for w in r3["warnings"]))
        r4 = validate_sections_full([{"type": "hero-split", "title": "t",
                                      "buttons": [{"text": "a", "action": "openLogin"}]}])
        self.assertTrue(any("openLogin" in w for w in r4["warnings"]))

    def test_errors_only_wrapper_matches(self):
        self.assertEqual(validate_sections([{"type": "no-such-type"}]),
                         validate_sections_full([{"type": "no-such-type"}])["errors"])

    def test_registered_types_count(self):
        from section_registry import SPECS
        # README 逐型枚举 34 型（33 演示型 + feature-grid 共享底层）
        self.assertEqual(len(SPECS), 34)


class TestMdToSections(unittest.TestCase):
    """生成端契约：md_to_sections 输出必须过注册表（先修校验再修生成的验收面）。"""

    def test_faq_objects_stats_type_and_registry_clean(self):
        body = ("## 为什么更快\n\n效率提升 30%。\n\n吞吐翻倍，节省 2 倍人力。\n\n"
                "这套流程把多个耗时步骤合并成一次提交，并保留字段契约与审计记录，方便事后追溯每一次变更。"
                "在多语言场景下它按语言独立成档，失败重试有明确边界，不会把半成品推到线上。\n\n"
                "## 适用哪些团队\n\n内容团队可以用它统一管理选题、生产、质检与发布四段流程，减少人工交接。"
                "运营团队可以跟踪引用与排名回流，把洞察回灌到下一次选题决策里，形成复利。"
                "工程团队可以通过适配器把产物推到任意无头 CMS，不需要改动前端渲染层。\n\n"
                "## 常见问题\n\n### 这是什么？\n\n这是一个测试用的说明段落。")
        secs = md_to_sections(body, title="T", cover_url="https://cdn.example.com/c.jpg", cover_alt="c")
        faq = [s for s in secs if s["type"] == "faq"][0]
        self.assertIsInstance(faq["items"][0], dict)
        self.assertIn("question", faq["items"][0])
        self.assertTrue([s for s in secs if s["type"] == "stats"], "数字证据应生成 stats 型")
        self.assertEqual(validate_sections(secs), [])
        self.assertEqual(registry_warnings(secs), [])


class TestPortableText(unittest.TestCase):
    """MD→PT：独立行图片保留为 image block；行内图片降级为链接（embed→链接 降级规则）。"""

    def test_standalone_image_becomes_image_block(self):
        blocks = md_to_portable_text("段落一。\n\n![示意图](https://cdn.example.com/img.png)\n\n段落二。")
        imgs = [b for b in blocks if b.get("_type") == "image"]
        self.assertEqual(len(imgs), 1)
        self.assertEqual(imgs[0]["src"], "https://cdn.example.com/img.png")
        self.assertEqual(imgs[0]["alt"], "示意图")
        self.assertTrue(imgs[0].get("_key"))
        self.assertEqual(validate_portable_text_body(blocks)["issues"], [])

    def test_no_more_image_text_placeholder(self):
        blocks = md_to_portable_text("![alt 文本](https://cdn.example.com/x.png)")
        texts = [c.get("text", "") for b in blocks for c in b.get("children", [])]
        self.assertFalse(any("[Image:" in t for t in texts))

    def test_inline_image_degrades_to_link(self):
        blocks = md_to_portable_text("看这张 ![图](https://cdn.example.com/in.png) 很好")
        para = blocks[0]
        links = para.get("markDefs", [])
        self.assertTrue(any(l.get("href") == "https://cdn.example.com/in.png" for l in links))

    def test_validator_flags_image_missing_src(self):
        blocks = [{"_type": "image", "_key": "k1", "src": "", "alt": "a"}]
        issues = validate_portable_text_body(blocks)["issues"]
        self.assertTrue(any("缺 src" in i for i in issues))

    def test_table_cells_stay_strings(self):
        blocks = md_to_portable_text("| a | **b** |\n| --- | --- |\n| 1 | 2 |")
        t = [b for b in blocks if b.get("_type") == "table"][0]
        self.assertTrue(all(isinstance(c, str) for r in t["rows"] for c in r["cells"]))


class TestBlogDocModel(unittest.TestCase):
    """PRD 内容模型：_id=(type,slug,language) 唯一键 + 三时间 + status 五态。"""

    def _doc(self, fm, body="## 一节\n\n正文。"):
        path = _write_md(self, fm, body)
        return build_blog_doc(path)

    def test_doc_id_namespaced(self):
        self.assertEqual(doc_id("blog", "my-post", "zh"), "blog-my-post-zh")
        self.assertEqual(doc_id("tool", "logo-maker", "en"), "tool-logo-maker-en")

    def test_id_three_times_status(self):
        doc = self._doc("slug: test-geo-post\nlanguage: zh\nstatus: scheduled\n"
                        "published: 2026-09-01\ndate: 2026-09-02\nno_index: true")
        self.assertEqual(doc["_id"], "blog-test-geo-post-zh")
        self.assertEqual(doc["status"], "scheduled")
        self.assertTrue(doc["publishedAt"].startswith("2026-09-01"))
        self.assertTrue(doc["displayedAt"].startswith("2026-09-02"))
        self.assertIs(doc["noIndex"], True)
        # JSON-LD datePublished 用对外显示时间（PRD C5）
        self.assertIn("2026-09-02", doc["seo"]["structuredData"]["json"])

    def test_displayed_falls_back_to_published(self):
        doc = self._doc("slug: a\nlanguage: en\npublished: 2026-01-02")
        self.assertTrue(doc["displayedAt"].startswith("2026-01-02"))
        self.assertEqual(doc["status"], "draft")

    def test_invalid_status_falls_back_to_draft(self):
        doc = self._doc("slug: a\nlanguage: en\nstatus: pending-review")
        self.assertEqual(doc["status"], "draft")

    def test_status_enum_all_valid(self):
        for st in ("draft", "scheduled", "published", "unpublished", "archived"):
            doc = self._doc(f"slug: a\nlanguage: en\nstatus: {st}")
            self.assertEqual(doc["status"], st)

    def test_legacy_id_param_overrides(self):
        path = _write_md(self, "slug: legacy-x\nlanguage: en", "正文。")
        self.assertEqual(build_blog_doc(path, legacy_id=True)["_id"], "legacy-x")
        self.assertEqual(build_blog_doc(path, legacy_id=False)["_id"], "blog-legacy-x-en")

    def test_iso_normalization(self):
        self.assertTrue(_iso("2026-01-02", "x").endswith("+08:00"))
        self.assertEqual(_iso("", "fb"), "fb")
        self.assertEqual(_iso("2026-01-02T03:04:05Z", "fb"), "2026-01-02T03:04:05Z")


class TestStorylines(unittest.TestCase):
    """故事线顺序校验：族内变体可替换；跨族错位 BLOCK；T-long 无固定序列。
    开源版/服务器部署不带 1-3 GenFlow SSOT（零品牌内容）→ load 为空是合法降级，跳过本组。"""

    _SSOT = storylines.load_storylines()

    @classmethod
    def setUpClass(cls):
        if not cls._SSOT:
            raise unittest.SkipTest("故事线 SSOT（1-3 GenFlow/Page Gen/Refresh-Page）不在本部署")

    def test_load_storylines_nonempty(self):
        sl = self._SSOT
        self.assertIn("F1", sl)
        self.assertIn("landing-brand-trust", sl)
        self.assertIn("solution-team", sl)

    def test_f1_match_ok_and_mismatch_blocked(self):
        f1 = self._SSOT["F1"]["sections"]
        self.assertTrue(storylines.check_storyline(f1, "F1")["ok"])
        swapped = [f1[1], f1[0]] + f1[2:]
        chk = storylines.check_storyline(swapped, "F1")
        self.assertFalse(chk["ok"])
        self.assertTrue(any("位置 1" in p for p in chk["problems"]))

    def test_variant_substitution_within_family_ok(self):
        t1 = self._SSOT["T1"]["sections"]
        # bento-2 → bento-6：同族变体替换，顺序校验必须放行
        sub = ["bento-6" if t == "bento-2" else t for t in t1]
        self.assertTrue(storylines.check_storyline(sub, "T1")["ok"])

    def test_t_long_has_no_fixed_sequence(self):
        chk = storylines.check_storyline(["anything"], "T-long")
        self.assertTrue(chk["known"] and chk["fixed"] is False and chk["ok"])

    def test_unknown_storyline_marked_not_known(self):
        chk = storylines.check_storyline(["x"], "no-such-line")
        self.assertFalse(chk["known"])


class TestPtToMdMirror(unittest.TestCase):
    """PT→MD 镜像：image block 输出保留 URL（此前丢失，MD 版本与页面不一致）。"""

    def test_image_roundtrip_keeps_url(self):
        md = portable_text_to_md([{"_type": "image", "_key": "k", "src": "https://cdn.example.com/i.png", "alt": "图"}])
        self.assertIn("![图](https://cdn.example.com/i.png)", md)


if __name__ == "__main__":
    unittest.main(verbosity=2)
