# Usage Guide for AI Assistants

This skill enables AI assistants (Claude, Codex, OpenClaw, etc.) to query Interactive Brokers data.

## Quick Start for AIs

1. **Read SKILL.md first** - Contains when to use, workflows, and tips
2. **Check user's environment** - Gateway host/port, installation path
3. **Run commands via shell** - Use `ib-options` CLI or direct Python script
4. **Present results** - Parse and explain output to user

## Integration Methods

### Method 1: Direct Shell Execution

Most AI assistants can execute shell commands:

```python
import subprocess

result = subprocess.run(
    ['ib-options', 'MSFT', '--quote'],
    capture_output=True,
    text=True
)
print(result.stdout)
```

### Method 2: OpenClaw Tool Integration

For OpenClaw/similar systems with tool definitions:

```json
{
  "name": "ib_options",
  "description": "Query IB Gateway for stocks and options chains",
  "parameters": {
    "symbol": {"type": "string", "required": true},
    "action": {"type": "string", "enum": ["quote", "chain"]},
    "filters": {"type": "object"}
  }
}
```

### Method 3: Claude/Codex Function Calling

Define as a tool/function:

```python
def query_ib_options(
    symbol: str,
    action: str = "quote",
    right: str = "P",
    min_delta: float = None,
    max_delta: float = None,
    otm_only: bool = False
) -> str:
    """Query Interactive Brokers for stock/options data"""
    
    cmd = ['ib-options', symbol, f'--{action}']
    if action == 'chain':
        cmd.extend(['--right', right])
        if min_delta:
            cmd.extend(['--min-delta', str(min_delta)])
        if max_delta:
            cmd.extend(['--max-delta', str(max_delta)])
        if otm_only:
            cmd.append('--otm-only')
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout
```

## Common Patterns

### Pattern 1: Stock Quote

```
User: "What's MSFT trading at?"

AI Action:
1. Execute: ib-options MSFT --quote
2. Parse output for price
3. Respond: "MSFT is trading at $401.88"
```

### Pattern 2: Options Chain Query

```
User: "Show me put options for AAPL"

AI Actions:
1. Execute: ib-options AAPL --chain --right P --min-volume 100
2. Parse and filter results
3. Present table with analysis
```

### Pattern 3: Multi-Symbol Scan

```
User: "Compare put opportunities in MSFT, AAPL, NVDA"

AI Actions:
1. Loop through symbols
2. Execute ib-options for each
3. Aggregate and compare results
4. Recommend best opportunities
```

## Environment Detection

Before using, detect the user's setup:

```python
import os
import subprocess

def detect_ib_setup():
    """Detect user's IB Gateway configuration"""
    
    # Check if command exists
    if subprocess.run(['which', 'ib-options'], capture_output=True).returncode == 0:
        # Check config or ask user
        config = {
            'host': os.getenv('IB_HOST', '127.0.0.1'),
            'port': os.getenv('IB_PORT', '4001'),
            'available': True
        }
    else:
        config = {'available': False}
    
    return config
```

## Output Parsing

Parse the tool's output:

### Quote Output

```
📊 MSFT Quote
   Last:   $401.88
   Bid:    $401.80
   Ask:    $402.14
   Close:  $401.84
   Volume: 567
```

Parse with regex or split by lines:

```python
import re

def parse_quote(output):
    last = re.search(r'Last:\s+\$(\d+\.\d+)', output)
    bid = re.search(r'Bid:\s+\$(\d+\.\d+)', output)
    ask = re.search(r'Ask:\s+\$(\d+\.\d+)', output)
    
    return {
        'last': float(last.group(1)) if last else None,
        'bid': float(bid.group(1)) if bid else None,
        'ask': float(ask.group(1)) if ask else None,
    }
```

### Options Chain Output

The output is a formatted table. Parse by:
1. Skip header lines (connection status, descriptions)
2. Find the table header row
3. Parse data rows with consistent column positions

```python
def parse_options_chain(output):
    lines = output.strip().split('\n')
    
    # Find table start (after "---" separator)
    data_start = None
    for i, line in enumerate(lines):
        if line.startswith('---'):
            data_start = i + 1
            break
    
    if data_start is None:
        return []
    
    options = []
    for line in lines[data_start:]:
        if not line.strip():
            continue
        
        # Parse columns (adjust based on actual format)
        # Example: exp, dte, strike, type, moneyness, etc.
        fields = line.split()
        options.append({
            'expiration': fields[0],
            'dte': int(fields[1]),
            'strike': fields[2],
            # ... parse other fields
        })
    
    return options
```

## Error Handling

Handle common errors gracefully:

```python
def query_with_error_handling(symbol, action='quote'):
    try:
        result = subprocess.run(
            ['ib-options', symbol, f'--{action}'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            error = result.stderr
            
            if 'Failed to connect' in error:
                return "IB Gateway is not running. Please start it first."
            elif 'No options found' in error:
                return "No options data available (paper trading limitation). Try live mode."
            else:
                return f"Error: {error}"
        
        return result.stdout
        
    except subprocess.TimeoutExpired:
        return "Query timed out. IB Gateway may be unresponsive."
    except FileNotFoundError:
        return "ib-options command not found. Please install the tool."
```

## Best Practices for AI Assistants

1. **Always verify gateway is running** before querying
2. **Cache results** if making multiple queries (avoid rate limits)
3. **Parse and summarize** - don't just dump raw output
4. **Explain context** - tell user what the numbers mean
5. **Suggest next steps** - "Would you like me to check other strikes?"
6. **Handle limitations** - Explain when paper trading lacks data

## Example Integration (Full Flow)

```python
class IBOptionsAssistant:
    """AI assistant with IB Options integration"""
    
    def handle_query(self, user_message):
        """Handle user query about stocks/options"""
        
        # Detect intent
        if 'quote' in user_message.lower() or 'price' in user_message.lower():
            symbol = self.extract_symbol(user_message)
            return self.get_quote(symbol)
        
        elif 'option' in user_message.lower():
            symbol = self.extract_symbol(user_message)
            right = 'P' if 'put' in user_message.lower() else 'C'
            return self.get_options_chain(symbol, right)
    
    def get_quote(self, symbol):
        """Get stock quote"""
        output = subprocess.run(
            ['ib-options', symbol, '--quote'],
            capture_output=True, text=True
        ).stdout
        
        # Parse and present
        quote = self.parse_quote(output)
        return f"{symbol} is trading at ${quote['last']:.2f}"
    
    def get_options_chain(self, symbol, right='P'):
        """Get options chain with smart filtering"""
        output = subprocess.run([
            'ib-options', symbol, '--chain', '--right', right,
            '--min-delta', '0.20', '--max-delta', '0.35',
            '--otm-only', '--min-volume', '100'
        ], capture_output=True, text=True).stdout
        
        # Parse and analyze
        options = self.parse_options_chain(output)
        
        # Present best opportunities
        return self.format_opportunities(symbol, options)
```

## Tips for Different AI Platforms

### Claude
- Use function calling with structured parameters
- Stream long outputs progressively
- Provide contextual explanations

### Codex
- Generate code snippets that call ib-options
- Show examples of parsed data structures
- Suggest refinements to filters

### OpenClaw/Kai
- Integrate via skill system (SKILL.md)
- Use exec tool for shell commands
- Log queries to user's trading journal

### Custom Assistants
- Adapt to your platform's tool/function system
- Read SKILL.md for comprehensive guidance
- Customize CUSTOMIZATION.md for your setup

## Testing Your Integration

```python
def test_integration():
    """Test AI integration with ib-options"""
    
    tests = [
        ('MSFT', 'quote'),
        ('AAPL', 'chain', {'right': 'P', 'min-delta': 0.25}),
    ]
    
    for test in tests:
        symbol = test[0]
        action = test[1]
        filters = test[2] if len(test) > 2 else {}
        
        print(f"Testing {symbol} {action}...")
        result = query_ib_options(symbol, action, **filters)
        assert result is not None, f"Failed for {symbol} {action}"
        print(f"✓ Success")
```

## Further Reading

- **SKILL.md** - Full workflow examples
- **CUSTOMIZATION.md** - Environment-specific setup
- **README.md** - User-facing documentation

---

*This skill is designed to be AI-assistant agnostic. Adapt as needed for your platform.*
