# IB Options Skill

Query Interactive Brokers Gateway for stock quotes and options chains via CLI.

## When to Use This Skill

Use when the user asks to:
- Get current stock quotes from Interactive Brokers
- Query options chains (puts/calls) for a specific stock
- Filter options by delta, volume, open interest, or moneyness
- Find option opportunities matching specific criteria
- Check real-time market data via IB Gateway

## Prerequisites

1. **IB Gateway** running and accessible (local, k8s, or remote)
2. **Python 3.10+** with `ib_insync` installed
3. **Network access** to IB Gateway (default port: 4001 for paper, 4002 for live)

## Installation

See `INSTALL.md` for detailed setup instructions.

The tool can be installed as:
- System-wide CLI: `ib-options`
- Direct Python script: `python3 ib-options.py`
- Wrapper with venv: Custom wrapper script (recommended)

## Command Reference

### Basic Usage

```bash
# Stock quote
ib-options SYMBOL --quote

# Options chain
ib-options SYMBOL --chain --right [P|C]

# Combined
ib-options SYMBOL --quote --chain --right P
```

### Connection Options

```bash
--host HOST          # IB Gateway host (default: localhost or check user's setup)
--port PORT          # Port: 4001=paper, 4002=live (default: 4001)
--client-id ID       # Client ID (default: random to avoid conflicts)
```

**Note:** Check the user's environment for the actual gateway host and port. Common setups:
- Local: `localhost` or `127.0.0.1`
- Kubernetes: Service IP or DNS name
- Remote: Specific IP address

### Options Chain Filters

```bash
--right [P|C]        # P=Put, C=Call (default: P)
--expiration DATE    # Specific expiration (YYYYMMDD format)
--min-delta FLOAT    # Minimum delta (absolute value)
--max-delta FLOAT    # Maximum delta (absolute value)
--min-volume INT     # Minimum daily volume
--min-oi INT         # Minimum open interest
--otm-only           # Only out-of-the-money options
--itm-only           # Only in-the-money options
```

## Common Workflows

### 1. Check Stock Price

```bash
ib-options MSFT --quote
```

### 2. Find Put Selling Opportunities

```bash
# OTM puts with delta 0.20-0.35, decent volume
ib-options MSFT --chain --right P \
  --min-delta 0.20 --max-delta 0.35 \
  --otm-only --min-volume 100 --min-oi 500
```

### 3. Check Specific Expiration

```bash
# March 20, 2026 puts
ib-options AAPL --chain --right P --expiration 20260320
```

### 4. Scan Multiple Stocks

```bash
for ticker in MSFT AAPL NVDA AMZN; do
  echo "=== $ticker ==="
  ib-options $ticker --chain --right P --min-delta 0.25 --otm-only
done
```

## Important Notes

### Paper vs Live Trading

- **Paper account (port 4001):** Limited options data, many strikes unavailable
- **Live account (port 4002):** Full options data, requires active session + 2FA

### Gateway Management

Gateway management depends on the user's setup:

**Kubernetes (k8s):**
```bash
kubectl get pods -l app=ib-gateway          # Check status
kubectl scale deployment ib-gateway --replicas=1  # Start
```

**Systemd (Linux service):**
```bash
systemctl status ib-gateway    # Check status
systemctl start ib-gateway     # Start service
```

**Docker:**
```bash
docker ps | grep ib-gateway    # Check status
docker start ib-gateway        # Start container
```

**Manual:**
Check if IB Gateway application is running on the system.

### Client ID Conflicts

The tool uses random client IDs by default. If you get "client id already in use" errors, the tool will auto-retry with a different ID.

## Output Format

### Stock Quote

```
📊 MSFT Quote
   Last:   $401.88
   Bid:    $401.80
   Ask:    $402.14
   Close:  $401.84
   Volume: 567
```

### Options Chain

```
Exp        DTE   Strike   Type Money%   Bid      Ask      Last     Vol      OI       Delta    IV      
--------------------------------------------------------------------------------------------------------------
20260320   45    $385.00  P    -6.00%   $5.70    $5.85    $5.78    1,899    7,391    -0.3486  42.02%
20260320   45    $380.00  P    -7.50%   $4.40    $4.60    $4.50    1,143    2,524    -0.2233  41.50%
```

## Error Handling

### Connection Failed

```
❌ Failed to connect to IB Gateway at 192.168.11.206:4001
```

**Fix:** Check gateway is running and port is correct.

### No Options Found

**Cause:** Paper trading account has limited options data.
**Fix:** Use live account (port 4002) or reduce filters.

### Security Definition Not Found

**Cause:** Strike/expiration combination doesn't exist or isn't available.
**Fix:** Use broader search or check available expirations.

## Integration with Trading Workflows

Use this tool to:
1. Validate opportunities from external screeners (Barchart, ThinkorSwim, etc.)
2. Get real-time Greeks and pricing before trades
3. Check actual bid-ask spreads to assess liquidity
4. Monitor existing positions
5. Compare options across different symbols or expirations

## Files & Locations

Check the user's environment for actual file locations. Common patterns:

- **Main script:** `ib-options.py` (in project/trading directory)
- **CLI wrapper:** System PATH or `~/bin/` directory
- **Python venv:** Isolated in project directory (recommended)
- **Skill docs:** In skills directory or alongside script

Consult `INSTALL.md` for the specific installation used.

## Tips for AI Assistants

### Before Using
- Check if IB Gateway is running (method depends on user's setup: k8s, systemd, manual)
- Verify connection details (host, port) from user's environment
- Paper trading (4001) has limited options data - suggest live (4002) for comprehensive chains

### Query Optimization
- Use filters to narrow results (delta, volume, OI) - makes output more useful
- Suggest specific expirations when user mentions dates or timeframes
- For options sellers: filter by OTM and appropriate delta ranges
- For options buyers: filter by ITM or specific strikes

### Common Workflows
1. **Options Selling:** Query OTM puts/calls with conservative delta (0.20-0.35)
2. **Options Buying:** Query specific strikes and expirations
3. **Market Analysis:** Scan multiple tickers for comparison
4. **Pre-trade Validation:** Check real-time pricing before executing

### Error Handling
- Connection failures → Check gateway status
- No options found → May need live connection or broader filters
- "Security definition not found" → Strike/expiration doesn't exist or unavailable

## Example Sessions

### Options Selling Workflow

```
User: "Check MSFT options for selling puts"

AI Actions:
1. Verify gateway is running (method depends on setup)
2. Get current price: ib-options MSFT --quote
3. Query put chain with filters:
   ib-options MSFT --chain --right P --min-delta 0.20 --max-delta 0.35 --otm-only
4. Present results with analysis

User: "What about the March 20 expiration specifically?"

AI Action:
ib-options MSFT --chain --right P --expiration 20260320 --min-delta 0.20 --max-delta 0.35
```

### Options Buying Workflow

```
User: "Show me AAPL call options for next month"

AI Actions:
1. Get current price: ib-options AAPL --quote
2. Query call chain:
   ib-options AAPL --chain --right C --min-volume 100
3. Filter and explain key strikes

User: "What's the $240 strike look like?"

AI Action: Filter output for $240 strike from previous results or re-query with expiration
```

### Multi-Symbol Comparison

```
User: "Compare put opportunities across MSFT, AAPL, GOOGL"

AI Action: Loop through symbols with consistent filters:
for ticker in MSFT AAPL GOOGL; do
  ib-options $ticker --chain --right P --min-delta 0.25 --otm-only
done
```

## Maintenance

The venv and dependencies are isolated in `~/clawd/trading/`. To update:

```bash
cd ~/clawd/trading
source venv/bin/activate
pip install --upgrade ib_insync
```

## Security

- Read-only connection to IB Gateway
- No order placement capability
- Unique client IDs prevent conflicts
- Connection automatically disconnects after query
