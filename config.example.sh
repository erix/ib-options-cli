#!/bin/bash
# IB Options Configuration Example
# Copy to config.sh and customize for your environment

# IB Gateway Connection
export IB_HOST="${IB_HOST:-127.0.0.1}"      # Gateway host
export IB_PORT="${IB_PORT:-4001}"           # Port (4001=paper, 4002=live)
export IB_CLIENT_ID="${IB_CLIENT_ID:-}"     # Client ID (empty=random)

# Default Filters (optional)
export IB_MIN_DELTA="${IB_MIN_DELTA:-0.20}"
export IB_MAX_DELTA="${IB_MAX_DELTA:-0.35}"
export IB_MIN_VOLUME="${IB_MIN_VOLUME:-100}"
export IB_MIN_OI="${IB_MIN_OI:-500}"

# Gateway Management (customize for your deployment)
# Uncomment and customize the method that matches your setup

# Kubernetes
# export GATEWAY_CHECK_CMD="kubectl get pods -l app=ib-gateway"
# export GATEWAY_START_CMD="kubectl scale deployment ib-gateway --replicas=1"
# export GATEWAY_STOP_CMD="kubectl scale deployment ib-gateway --replicas=0"

# Systemd
# export GATEWAY_CHECK_CMD="systemctl status ib-gateway.service"
# export GATEWAY_START_CMD="systemctl start ib-gateway.service"
# export GATEWAY_STOP_CMD="systemctl stop ib-gateway.service"

# Docker
# export GATEWAY_CHECK_CMD="docker ps -f name=ib-gateway"
# export GATEWAY_START_CMD="docker start ib-gateway"
# export GATEWAY_STOP_CMD="docker stop ib-gateway"

# Watchlist (optional - for scanning scripts)
export IB_WATCHLIST="${IB_WATCHLIST:-MSFT AAPL NVDA GOOGL AMZN}"

# Output preferences
export IB_OUTPUT_FORMAT="${IB_OUTPUT_FORMAT:-table}"  # table|json|csv
