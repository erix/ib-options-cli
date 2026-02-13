#!/bin/bash
# Scan for put selling opportunities across watchlist

WATCHLIST="MSFT AAPL NVDA GOOGL AMZN AVGO"

echo "🔍 Scanning for Put Selling Opportunities"
echo "Delta: 0.20-0.35 | OTM | Volume >100 | OI >500"
echo ""

for ticker in $WATCHLIST; do
  echo "=== $ticker ==="
  ib-options $ticker --chain --right P \
    --min-delta 0.20 --max-delta 0.35 \
    --otm-only \
    --min-volume 100 --min-oi 500 \
    2>/dev/null || echo "  (No matches)"
  echo ""
done
