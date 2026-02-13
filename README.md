# IB Options CLI

Query Interactive Brokers Gateway for stock quotes and options chains via command line.

**AI-Assistant Compatible:** Works with Claude, Codex, OpenClaw, and other AI coding assistants.

**Version:** 1.1.0  
**License:** MIT

![PyPI - Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- ✅ Real-time stock quotes from IB Gateway
- ✅ Options chain data (puts & calls)
- ✅ Filter by delta, volume, open interest, DTE
- ✅ Filter by moneyness (ITM/OTM)
- ✅ Greeks (delta, implied volatility)
- ✅ Specific expiration queries
- ✅ Read-only connection (safe)
- ✅ AI assistant integration ready

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ib-options-cli.git
cd ib-options-cli

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install ib_insync

# Copy script to your PATH
cp scripts/ib-options.py ~/bin/ib-options
chmod +x ~/bin/ib-options
```

### Basic Usage

```bash
# Stock quote
ib-options MSFT --quote

# Put options chain
ib-options MSFT --chain --right P

# Filter for put selling (delta 0.20-0.35, 30-45 DTE, OTM)
ib-options AAPL --chain --right P \
  --min-delta 0.20 --max-delta 0.35 \
  --min-dte 30 --max-dte 45 \
  --otm-only --min-volume 100
```

## Prerequisites

1. **IB Gateway** running and accessible (local, k8s, or remote)
2. **Python 3.10+**
3. **ib_insync** library

## Command Reference

### Stock Quote

```bash
ib-options SYMBOL --quote

# Example
ib-options MSFT --quote
```

Output:
```
📊 MSFT Quote
   Last:   $401.88
   Bid:    $401.80
   Ask:    $402.14
   Close:  $401.84
   Volume: 567
```

### Options Chain

```bash
ib-options SYMBOL --chain --right [P|C] [filters]

# Examples
ib-options MSFT --chain --right P                    # All puts
ib-options MSFT --chain --right P --min-delta 0.25   # Delta filter
ib-options MSFT --chain --right P --min-dte 30 --max-dte 45  # DTE filter
```

### Filters

| Filter | Description |
|--------|-------------|
| `--min-delta FLOAT` | Minimum delta (absolute value) |
| `--max-delta FLOAT` | Maximum delta (absolute value) |
| `--min-dte INT` | Minimum days to expiration |
| `--max-dte INT` | Maximum days to expiration |
| `--min-volume INT` | Minimum daily volume |
| `--min-oi INT` | Minimum open interest |
| `--otm-only` | Only out-of-the-money options |
| `--itm-only` | Only in-the-money options |
| `--expiration YYYYMMDD` | Specific expiration date |

### Connection

| Option | Description |
|--------|-------------|
| `--host HOST` | IB Gateway host (default: localhost) |
| `--port PORT` | Port: 4001=paper, 4002=live (default: 4001) |
| `--client-id ID` | Client ID (default: random) |

## Common Use Cases

### Options Selling

Find put selling opportunities:

```bash
# Conservative: 30-45 DTE, delta 0.20-0.30, OTM, liquid
ib-options MSFT --chain --right P \
  --min-delta 0.20 --max-delta 0.30 \
  --min-dte 30 --max-dte 45 \
  --otm-only \
  --min-volume 100 --min-oi 500
```

### Options Buying

Find specific strikes:

```bash
# Calls with high volume
ib-options AAPL --chain --right C \
  --min-volume 500 \
  --min-dte 30
```

### Multi-Stock Scan

```bash
for stock in MSFT AAPL NVDA GOOGL; do
  echo "=== $stock ==="
  ib-options $stock --chain --right P --min-delta 0.25 --otm-only
done
```

## Paper vs Live Trading

| Feature | Paper (4001) | Live (4002) |
|---------|--------------|-------------|
| Stock quotes | ✅ | ✅ |
| Options chains | ⚠️ Limited | ✅ Full |
| Requires 2FA | ❌ | ✅ |
| Greeks | ⚠️ Partial | ✅ Full |

**Note:** Paper trading has limited options data. For comprehensive chains, use live connection.

## Configuration

### Environment Variables

```bash
export IB_HOST="192.168.1.100"  # Gateway host
export IB_PORT="4001"            # Port
```

### Custom Config

Copy and customize:

```bash
cp config.example.sh config.sh
# Edit config.sh with your settings
source config.sh
```

## AI Assistant Integration

This tool is designed to work with AI coding assistants:

### For OpenClaw/Kai

Already integrated via skill system. The AI will use it automatically.

### For Claude

```markdown
You have access to the ib-options tool. See SKILL.md for usage.
Connection: host:4001
```

### For Codex

```python
import subprocess
result = subprocess.run(['ib-options', 'MSFT', '--quote'], 
                       capture_output=True, text=True)
```

See [USAGE_FOR_AI.md](USAGE_FOR_AI.md) for detailed integration guide.

## Documentation

- **[SKILL.md](SKILL.md)** - AI assistant instructions
- **[QUICKREF.md](QUICKREF.md)** - Quick command reference
- **[INSTALL.md](INSTALL.md)** - Installation guide
- **[CUSTOMIZATION.md](CUSTOMIZATION.md)** - Environment customization
- **[USAGE_FOR_AI.md](USAGE_FOR_AI.md)** - AI integration patterns

## Examples

See [examples/](examples/) directory for working scripts:

- `basic-usage.sh` - Basic query examples
- `put-selling-scan.sh` - Watchlist scanner

## Troubleshooting

### Connection Failed

```bash
# Check if gateway is running
# Kubernetes:
kubectl get pods -l app=ib-gateway

# Systemd:
systemctl status ib-gateway

# Docker:
docker ps | grep ib-gateway
```

### No Options Found

**Cause:** Paper trading has limited options data.

**Solution:** Use live connection (`--port 4002`)

### Client ID Already in Use

The tool uses random client IDs. This should be rare. Simply retry.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file.

## Support

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/ib-options-cli/issues)
- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/ib-options-cli/discussions)

## Credits

Built with:
- [ib_insync](https://github.com/erdewit/ib_insync) - Interactive Brokers API wrapper
- Python 3.10+

---

**Star ⭐ this repo if you find it useful!**
