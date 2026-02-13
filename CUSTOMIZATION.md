# Customization Guide

This skill is designed to be reusable across different environments and AI assistants.

## Environment-Specific Configuration

### IB Gateway Connection

Update the default connection settings based on your setup:

**Edit the script** (`ib-options.py`):

```python
# Default connection parameters
def connect_ib(host='YOUR_HOST', port=YOUR_PORT, client_id=None):
```

Common configurations:

| Setup | Host | Port |
|-------|------|------|
| Local IB Gateway | `127.0.0.1` | 4001 (paper) / 4002 (live) |
| Kubernetes | Service IP or DNS | 4001 / 4002 |
| Remote | Specific IP | 4001 / 4002 |
| Docker | Container IP or `localhost` | Mapped port |

### Installation Paths

Adjust installation paths to match your project structure:

**Current setup example:**
- Script: `~/clawd/trading/ib-options.py`
- CLI wrapper: `~/clawd/bin/ib-options`
- Venv: `~/clawd/trading/venv/`

**Customize for your project:**
```bash
# Set your project directory
PROJECT_DIR=~/your-project

# Install script
cp scripts/ib-options.py $PROJECT_DIR/

# Create wrapper
cat > ~/bin/ib-options <<EOF
#!/bin/bash
source $PROJECT_DIR/venv/bin/activate
python3 $PROJECT_DIR/ib-options.py "\$@"
EOF
chmod +x ~/bin/ib-options
```

## Gateway Management Commands

Customize the gateway check commands based on your deployment:

### For Kubernetes

Update SKILL.md references:
```bash
# Status check
kubectl get pods -l app=YOUR_GATEWAY_LABEL

# Start
kubectl scale deployment YOUR_DEPLOYMENT --replicas=1
```

### For Systemd

```bash
# Status check
systemctl status your-ib-gateway.service

# Start/stop
systemctl start your-ib-gateway.service
systemctl stop your-ib-gateway.service
```

### For Docker

```bash
# Status check
docker ps -f name=your-ib-gateway

# Start/stop
docker start your-ib-gateway
docker stop your-ib-gateway
```

## User-Specific Workflows

### Trading Style Filters

Customize default filters for your trading approach:

**Options Sellers:**
```python
# Add to script or wrapper
DEFAULT_SELLER_ARGS = [
    '--right', 'P',
    '--min-delta', '0.20',
    '--max-delta', '0.35',
    '--otm-only',
    '--min-volume', '100'
]
```

**Options Buyers:**
```python
DEFAULT_BUYER_ARGS = [
    '--min-volume', '500',
    '--min-oi', '1000'
]
```

### Watchlists

Create custom scan scripts for your watchlist:

```bash
#!/bin/bash
# my-watchlist-scan.sh

WATCHLIST="TICKER1 TICKER2 TICKER3"
FILTERS="--min-delta 0.25 --otm-only --min-volume 100"

for ticker in $WATCHLIST; do
  echo "=== $ticker ==="
  ib-options $ticker --chain --right P $FILTERS
done
```

## AI Assistant Context

When using with different AI assistants, provide context:

### For Claude

```markdown
You have access to the ib-options tool for querying Interactive Brokers data.
See ~/path/to/skills/ib-options/SKILL.md for usage.

Gateway connection: host.example.com:4001
My trading focus: [options selling/buying/other]
```

### For Codex

```python
# Tool: ib-options
# Purpose: Query IB Gateway for stock quotes and options chains
# Location: /path/to/ib-options
# Connection: host:port (see environment)
```

### For OpenClaw/Kai

Add to `TOOLS.md` or skill system as documented.

## Output Format Customization

### Add Custom Columns

Edit the `format_option_table()` function to add fields:

```python
def format_option_table(options):
    # Add your custom columns
    print(f"{'Exp':<10} {'Strike':<8} {'YOUR_FIELD':<10} ...")
```

### Export to CSV

Add CSV export option:

```python
import csv

def export_csv(options, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=options[0].keys())
        writer.writeheader()
        writer.writerows(options)
```

## Integration with Other Tools

### Barchart Screener Integration

```bash
# Fetch Barchart results, then validate with IB
barchart_symbols="MSFT AAPL NVDA"
for sym in $barchart_symbols; do
  ib-options $sym --chain --right P --min-delta 0.25
done
```

### Trade Journal Integration

```bash
# Log options data to your journal
ib-options MSFT --chain --right P > trades/$(date +%Y-%m-%d)-MSFT-scan.txt
```

## Security & Privacy

### Sensitive Defaults

If sharing the skill:
- Remove any hardcoded IPs/hosts
- Use environment variables for connection details
- Don't include account-specific data

### Environment Variables

Make connection configurable:

```python
import os

def connect_ib(
    host=os.getenv('IB_HOST', 'localhost'),
    port=int(os.getenv('IB_PORT', '4001')),
    client_id=None
):
    # ...
```

Then users can set:
```bash
export IB_HOST=192.168.1.100
export IB_PORT=4001
ib-options MSFT --quote
```

## Testing

Customize test cases for your environment:

```bash
# Test connection
ib-options YOUR_SYMBOL --quote

# Test with your typical filters
ib-options YOUR_SYMBOL --chain --right P --YOUR_FILTERS

# Test gateway auto-detection
./scripts/check-gateway-status.sh
```

## Documentation

When customizing, update:
- `README.md` - User-facing examples
- `SKILL.md` - AI assistant instructions  
- `QUICKREF.md` - Common commands
- `INSTALL.md` - Setup steps

Keep customization notes in this file for reference.
