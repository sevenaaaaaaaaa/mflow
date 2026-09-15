"""
Lovart Sentinel - Content Production Monitor
读取内容日历和产出报告
"""
from pathlib import Path
import glob
from ._common import banner

CONTENT_DIR = Path(__file__).resolve().parents[4] / "1-3 Content Gen" / "Content Calendar"


def collect() -> dict:
    data = dict(banner("Content Production Monitor"))

    # 查找最新每日产出报告
    dailies = sorted(glob.glob(str(CONTENT_DIR / "daily-link-summary-*.md")))
    if dailies:
        latest = Path(dailies[-1])
        content = latest.read_text(encoding="utf-8")
        data["latest_daily_file"] = latest.name
        # 提取产出数量
        import re
        articles = re.findall(r'^\d+\.\s+(.+)$', content, re.MULTILINE)
        data["latest_articles"] = articles
        data["latest_article_count"] = len(articles)

    # 查找内容日历全景
    calendars = sorted(glob.glob(str(CONTENT_DIR / "00-内容日历全景清单*.md")))
    data["calendar_files"] = [Path(f).name for f in calendars]

    # 安全备份备注
    # TODO(reorg 2026-06-03): 灾备备忘.md 在结构优化中已删除，暂无替代源；保留 .exists() 守卫避免报错
    dr_notes = Path(__file__).resolve().parent.parent.parent.parent / "Sanity Blog" / "灾备备忘.md"
    if dr_notes.exists():
        data["dr_notes_updated"] = dr_notes.stat().st_mtime

    return data
