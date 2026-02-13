# Installation Guide

## Prerequisites

1. **IB Gateway running on k8s**
   ```bash
   kubectl get pods -l app=ib-gateway
   ```

2. **Python 3.14+**
   ```bash
   python3 --version
   ```

## Quick Install

Already installed! The skill is located at:
- CLI: `~/clawd/bin/ib-options`
- Script: `~/clawd/trading/ib-options.py`
- Venv: `~/clawd/trading/venv/`

## Manual Installation (if needed)

### 1. Create Python Virtual Environment

```bash
cd ~/clawd/trading
python3 -m venv venv
source venv/bin/activate
pip install ib_insync
```

### 2. Copy Script

```bash
cp ~/clawd/skills/ib-options/scripts/ib-options.py ~/clawd/trading/
chmod +x ~/clawd/trading/ib-options.py
```

### 3. Create Wrapper

```bash
cat > ~/clawd/bin/ib-options <<'EOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TRADING_DIR="$SCRIPT_DIR/../trading"
source "$TRADING_DIR/venv/bin/activate"
python3 "$TRADING_DIR/ib-options.py" "$@"
EOF

chmod +x ~/clawd/bin/ib-options
```

### 4. Test

```bash
ib-options MSFT --quote
```

## Configuration

### Default Connection

The tool connects to:
- **Host:** 192.168.11.206 (IB Gateway k8s service)
- **Port:** 4001 (paper trading)
- **Client ID:** Random (to avoid conflicts)

### Custom Connection

```bash
# Live trading
ib-options MSFT --quote --port 4002

# Different host
ib-options MSFT --quote --host 192.168.1.100 --port 4001
```

## Verification

```bash
# Check gateway is running
kubectl get pods -l app=ib-gateway

# Test stock quote
ib-options MSFT --quote

# Test options chain (may have limited data on paper)
ib-options AAPL --chain --right P
```

## Updating

```bash
cd ~/clawd/trading
source venv/bin/activate
pip install --upgrade ib_insync
```

## Uninstall

```bash
rm ~/clawd/bin/ib-options
rm ~/clawd/trading/ib-options.py
rm -rf ~/clawd/trading/venv
rm -rf ~/clawd/skills/ib-options
```

## Troubleshooting

### Python Event Loop Error

Fixed in Python 3.14+ by the script. If you see event loop errors:
```bash
# Recreate venv
cd ~/clawd/trading
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install ib_insync
```

### Connection Refused

```bash
# Check gateway
kubectl get svc ib-gateway
kubectl get pods -l app=ib-gateway

# Scale up if needed
kubectl scale deployment ib-gateway --replicas=1
```

### No Options Data

Paper trading accounts have limited options chains. Use live connection:
```bash
ib-options MSFT --chain --port 4002 --right P
```
