"""
Lovart Sentinel - Email Health Monitor
读取邮件复盘报告并提取关键健康指标
"""
from pathlib import Path
from ._common import banner
import re, glob

EMAIL_REPORT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "Lovart"


def collect() -> dict:
    data = dict(banner("Email Health Monitor"))
    md_files = sorted(glob.glob(str(EMAIL_REPORT_DIR / "邮件复盘*.md")))
    data["available_reports"] = [Path(f).name for f in md_files]

    if not md_files:
        data["status"] = "no_data"
        return data

    latest = Path(md_files[-1])
    content = latest.read_text(encoding="utf-8")
    data["latest_report"] = str(latest.name)

    metrics = {}
    patterns = {
        "delivery_rate": r'投递率[^:]*[→]*[:\s]*([\d.]+)%',
        "open_rate": r'打开率[^:]*[→]*[:\s]*([\d.]+)%',
        "ctor": r'CTOR[^:]*[→]*[:\s]*([\d.]+)%',
        "bounce_rate": r'跳出率[^:]*[→]*[:\s]*([\d.]+)%',
        "unsub_per_10k": r'退订[^\d]*([\d.]+)[^\d]*万',
        "total_sent": r'发送量[^:]*[→]*[:\s]*([\d.]+)万',
    }
    for key, pattern in patterns.items():
        m = re.search(pattern, content)
        if m:
            metrics[key] = m.group(1)

    # fallback: look for percentage patterns in table rows
    if not metrics.get("delivery_rate"):
        # try to find 投递/送达 rates in the mail report
        for line in content.split("\n"):
            if "投递" in line or "送达" in line:
                nums = re.findall(r'([\d.]+)%', line)
                if nums:
                    metrics["delivery_rate"] = nums[-1]  # last percentage is usually delivery rate
                    break

    # fallback for unsub
    if not metrics.get("unsub_per_10k"):
        for line in content.split("\n"):
            if "退订" in line:
                nums = re.findall(r'([\d.]+)', line)
                if len(nums) >= 2:
                    metrics["unsub_per_10k"] = nums[-1]
                    break

    data["extracted_metrics"] = metrics

    # 告警检查
    alerts = []
    delivery = float(metrics.get("delivery_rate", 100))
    if delivery < 85:
        alerts.append({"level": "critical", "msg": f"邮件送达率降至 {delivery}%，低于85%阈值"})
    elif delivery < 90:
        alerts.append({"level": "warning", "msg": f"邮件送达率 {delivery}% 偏低"})
    unsub = float(metrics.get("unsub_per_10k", 0))
    if unsub > 40:
        alerts.append({"level": "critical", "msg": f"退订率 {unsub}/万 严重超标"})
    elif unsub > 20:
        alerts.append({"level": "warning", "msg": f"退订率 {unsub}/万 偏高"})
    data["alerts"] = alerts

    return data
