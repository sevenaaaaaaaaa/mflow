"""qa_compare — 静态断言（渲染 HTML vs 预期）。"""
import re


def assert_sections(rendered_html, expected_types):
    """组件覆盖断言：expected_types 中每个 type 都应在渲染 HTML 中出现。"""
    found = {t for t in expected_types
             if re.search(r'data-lp-section="%s"' % re.escape(t), rendered_html)
             or re.search(r'wp-block-lovart-' + re.escape(t), rendered_html)}
    missing = [t for t in expected_types if t not in found]
    return {"pass": not missing, "found": sorted(found), "missing": missing}


def assert_keywords(rendered_html, keywords):
    """关键词在渲染输出中存在（文案级抽查）。"""
    missing = [k for k in keywords if k not in rendered_html]
    return {"pass": not missing, "missing": missing}


def assert_no_scripts(rendered_html):
    """体验约束：预览工具/水合脚本不应出现在复刻输出。"""
    scripts = re.findall(r"<script\b", rendered_html)
    return {"pass": len(scripts) == 0, "count": len(scripts)}


def assert_css_loaded(rendered_html, marker="lovart-site"):
    """主题 CSS 已加载。"""
    return {"pass": marker in rendered_html}
