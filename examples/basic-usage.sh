#!/bin/bash
# IB Options - Basic Usage Examples

echo "=== Stock Quote ==="
ib-options MSFT --quote

echo ""
echo "=== Put Options Chain ==="
ib-options MSFT --chain --right P --min-delta 0.20 --max-delta 0.35 --otm-only

echo ""
echo "=== Specific Expiration ==="
ib-options AAPL --chain --right P --expiration 20260320

echo ""
echo "=== Scan Multiple Stocks ==="
for ticker in MSFT AAPL NVDA; do
  echo "--- $ticker ---"
  ib-options $ticker --quote
done
