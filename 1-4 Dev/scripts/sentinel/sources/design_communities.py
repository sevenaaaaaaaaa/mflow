"""
Lovart Sentinel - Design Communities Monitor
监测 Dribbble / Behance / Figma Community / 站酷 / 花瓣 等设计社区
"""
from ._common import banner

QUERIES = {
    "dribbble": "lovart site:dribbble.com",
    "behance": "lovart ai site:behance.net",
    "figma": "lovart site:figma.com/community",
    "civitai": "lovart site:civitai.com",
    "pixiv": "lovart AI site:pixiv.net",
    # 中国设计社区 via 百度
    "zcool": "lovart 站酷 site:zcool.com.cn",
    "huaban": "lovart 花瓣 site:huaban.com",
    "ui_cn": "lovart AI设计工具 site:ui.cn",
}


def collect() -> dict:
    data = dict(banner("Design Communities Monitor"))
    data["status"] = "delegated"
    data["queries"] = QUERIES
    data["_instructions"] = """
    1. webfetch DDG/百度 搜索各设计社区
    2. 提取：作品数量、作者类型、互动量（likes/views/saves）
    3. 检测Lovart产出的设计作品质量
    4. 对比竞品（Canva/MJ）在相同社区的活跃度
    5. 发现可合作的活跃设计师
    """
    return data
