# IB Options Quick Reference

## Stock Quote

```bash
ib-options MSFT --quote
```

## Options Chain

### Basic
```bash
ib-options MSFT --chain --right P     # All puts
ib-options MSFT --chain --right C     # All calls
```

### Filtered
```bash
# Delta range
ib-options MSFT --chain --right P --min-delta 0.20 --max-delta 0.35

# DTE range (30-60 days)
ib-options MSFT --chain --right P --min-dte 30 --max-dte 60

# Volume + OI
ib-options MSFT --chain --right P --min-volume 100 --min-oi 500

# OTM only
ib-options MSFT --chain --right P --otm-only

# Combine all
ib-options MSFT --chain --right P \
  --min-delta 0.20 --max-delta 0.35 \
  --min-dte 30 --max-dte 60 \
  --otm-only --min-volume 100 --min-oi 500
```

### Specific Expiration
```bash
ib-options AAPL --chain --right P --expiration 20260320
```

## Connection

```bash
# Paper (default)
ib-options MSFT --quote

# Live
ib-options MSFT --quote --port 4002

# Custom
ib-options MSFT --quote --host 192.168.1.100 --port 4001
```

## Common Workflows

### Put Selling Scan
```bash
ib-options MSFT --chain --right P \
  --min-delta 0.20 --max-delta 0.35 \
  --otm-only \
  --min-volume 100
```

### Multi-Stock Scan
```bash
for stock in MSFT AAPL NVDA; do
  ib-options $stock --chain --right P --otm-only
done
```

### Check Gateway Status
```bash
kubectl get pods -l app=ib-gateway
```

## Ports

- **4001** = Paper trading (limited options data)
- **4002** = Live trading (full options data, requires 2FA)

## Output Columns

| Column | Meaning |
|--------|---------|
| Exp | Expiration date (YYYYMMDD) |
| DTE | Days to expiration |
| Strike | Option strike price |
| Type | P=Put, C=Call |
| Money% | Moneyness (% OTM/ITM) |
| Bid | Bid price |
| Ask | Ask price |
| Last | Last trade price |
| Vol | Volume (today) |
| OI | Open interest |
| Delta | Delta (Greek) |
| IV | Implied volatility |
