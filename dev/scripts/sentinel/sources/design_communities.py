"""
品牌方 Sentinel - Design Communities Monitor
监测 Dribbble / Behance / Figma Community / 站酷 / 花瓣 等设计社区
"""
from ._common import banner

QUERIES = {
    "dribbble": "品牌 site:dribbble.com",
    "behance": "品牌 ai site:behance.net",
    "figma": "品牌 site:figma.com/community",
    "civitai": "品牌 site:civitai.com",
    "pixiv": "品牌 AI site:pixiv.net",
    # 中国设计社区 via 百度
    "zcool": "品牌 站酷 site:zcool.com.cn",
    "huaban": "品牌 花瓣 site:huaban.com",
    "ui_cn": "品牌 AI设计工具 site:ui.cn",
}


def collect() -> dict:
    data = dict(banner("Design Communities Monitor"))
    data["status"] = "delegated"
    data["queries"] = QUERIES
    data["_instructions"] = """
    1. webfetch DDG/百度 搜索各设计社区
    2. 提取：作品数量、作者类型、互动量（likes/views/saves）
    3. 检测品牌方产出的设计作品质量
    4. 对比竞品（Canva/MJ）在相同社区的活跃度
    5. 发现可合作的活跃设计师
    """
    return data
