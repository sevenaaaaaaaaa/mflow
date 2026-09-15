#!/bin/bash
# Lovart Trident Data Engine — 一键三引擎采集 + 统一摘要
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCAL_DEV_ROOT="${LOVART_LOCAL_DEV_ROOT:-$HOME/Documents/Lovart Local Dev}"
OUT_DIR="${LOVART_TRIDENT_OUTPUT_DIR:-$LOCAL_DEV_ROOT/Output/Data Ingestion}"
WAREHOUSE_DIR="${LOVART_TRIDENT_WAREHOUSE_DIR:-$LOCAL_DEV_ROOT/Output/Warehouse}"
mkdir -p "$OUT_DIR" "$WAREHOUSE_DIR"

echo "═══════════════════════════════════════════"
echo "  🔱 Lovart Trident Data Engine"
echo "  GSC + GA4 + Bing → Unified Brief"
echo "═══════════════════════════════════════════"

echo ""
echo "[1/4] GSC — Google Search Console..."
python3 "$SCRIPT_DIR/gsc_fetch.py" 2>&1 | grep -v "FutureWarning\|warnings.warn\|google.auth\|NotOpenSSL\|urllib3\|non-supported\|google.api_core\|urllib3" || echo "  ⚠️ GSC fetch had warnings (data may still be OK)"

echo ""
echo "[2/4] GA4 — Google Analytics 4..."
python3 "$SCRIPT_DIR/ga4_fetch.py" 2>&1 | grep -v "FutureWarning\|warnings.warn\|google.auth\|NotOpenSSL\|urllib3\|non-supported\|google.api_core\|urllib3" || echo "  ⚠️ GA4 fetch had warnings"

echo ""
echo "[3/4] Bing — Bing Webmaster..."
python3 "$SCRIPT_DIR/bing_fetch.py" 2>&1 | grep -v "NotOpenSSL\|urllib3\|warnings.warn" || echo "  ⚠️ Bing fetch had warnings"

echo ""
echo "[4/6] 生成统一情报摘要..."
python3 "$SCRIPT_DIR/unified_brief.py"

echo ""
echo "[5/6] 数据入仓 (SQLite + CSV/Parquet)..."
python3 "$SCRIPT_DIR/push_to_warehouse.py" || echo "  ⚠️ Warehouse push had issues"

echo ""
echo "[6/6] 推送到飞书多维表..."
python3 "$SCRIPT_DIR/push_to_feishu.py" || echo "  ⚠️ Feishu push skipped (credentials may not be configured)"

echo ""
echo "═══════════════════════════════════════════"
echo "  ✅ 完成"
echo "  📁 数据:  $OUT_DIR"
ls -lh "$OUT_DIR/gsc-full.json" "$OUT_DIR/ga4-full.json" "$OUT_DIR/bing-full.json" "$OUT_DIR/intelligence-brief.md" 2>/dev/null
echo "  🗄️  数仓:  $WAREHOUSE_DIR/trident_data.db"
echo "  📤 导出:  $WAREHOUSE_DIR/$(date +%Y-%m-%d)/"
echo "═══════════════════════════════════════════"
