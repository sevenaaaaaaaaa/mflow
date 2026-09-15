"""
Lovart Sentinel - Bing SERP Scanner
通过 webfetch 实时扫描 Bing 搜索结果页
注意：需要在 opencode agent 上下文中运行，调用 webfetch
"""
from ._common import banner

# 寄生域名列表
PARASITES = [
    "lovart-ai.com", "lovart.pro", "lovart.io",
    "lovart.info", "lovart.me", "lovart.fyi"
]

QUERIES = {
    "brand": "lovart ai",
    "brand_variant": "lovart ai design agent",
    "competitor": "lovart vs canva vs midjourney ai design tool",
    "review": "lovart ai review 2025 2026",
    "chinese": "lovart ai 使用 体验 评价",
}


def collect() -> dict:
    """
    此 source 需要在 opencode agent 中通过 webfetch 实时采集。
    当作为独立脚本运行时，返回采集指令。
    """
    data = dict(banner("Bing SERP Scan"))
    data["status"] = "delegated"
    data["instructions"] = "Run webfetch for each query below and parse results"
    data["queries"] = QUERIES
    data["parasite_domains_to_watch"] = PARASITES
    data["_note"] = "此 source 需 opencode agent 使用 webfetch 工具逐条查询并解析 SERP"

    # 内置模拟结果供本地测试
    data["_serp_results"] = {}
    for name, query in QUERIES.items():
        data["_serp_results"][name] = {
            "query": query,
            "url": f"https://www.bing.com/search?q={query.replace(' ', '+')}",
            "status": "pending_agent_fetch",
        }
    return data


# 辅助：解析 Bing SERP 结果的函数（供 agent 调用后使用）
def parse_bing_serp(markdown_content: str, query_name: str) -> dict:
    """从 webfetch 返回的 markdown 内容中提取 SERP 数据"""
    import re
    result = {"query": query_name, "total_results": 0, "top_domains": [], "has_parasites": False, "lovart_position": None}

    # 提取 URL 模式
    url_pattern = re.findall(r'https?://([^/\s\)]+)', markdown_content)
    domains = []
    seen = set()
    for domain in url_pattern:
        domain = domain.replace("www.", "")
        if domain not in seen:
            seen.add(domain)
            domains.append(domain)

    result["top_domains"] = domains[:10]

    # 检查寄生域名
    parasites_found = []
    for i, d in enumerate(domains):
        if any(p in d for p in PARASITES):
            parasites_found.append({"position": i + 1, "domain": d})
    result["parasites_in_serp"] = parasites_found
    result["has_parasites"] = len(parasites_found) > 0

    # Lovart 官方排名
    for i, d in enumerate(domains):
        if "lovart.ai" in d:
            result["lovart_position"] = i + 1
            break

    return result
