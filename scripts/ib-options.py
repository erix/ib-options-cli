#!/usr/bin/env python3
"""
IB Options Chain CLI Tool
Query stocks and options chains via Interactive Brokers Gateway
"""

import argparse
import sys
from datetime import datetime
import asyncio

# Fix for Python 3.14 event loop
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from ib_insync import IB, Stock, Option, util

def connect_ib(host='192.168.11.206', port=4001, client_id=None):
    """Connect to IB Gateway"""
    import random
    if client_id is None:
        client_id = random.randint(100, 9999)
    
    ib = IB()
    try:
        ib.connect(host, port, clientId=client_id, readonly=True)
        return ib
    except Exception as e:
        print(f"❌ Failed to connect to IB Gateway at {host}:{port}")
        print(f"   Error: {e}")
        print(f"\n💡 Make sure IB Gateway is running:")
        print(f"   kubectl get pods -l app=ib-gateway")
        sys.exit(1)

def get_stock_quote(ib, symbol):
    """Get current stock quote"""
    stock = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(stock)
    ticker = ib.reqMktData(stock, '', False, False)
    ib.sleep(2)  # Wait for data
    
    return {
        'symbol': symbol,
        'last': ticker.last,
        'bid': ticker.bid,
        'ask': ticker.ask,
        'close': ticker.close,
        'volume': ticker.volume,
    }

def get_option_chain(ib, symbol, expiration=None, right='P', strikes=None):
    """Get option chain for a symbol"""
    stock = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(stock)
    
    # Get option chain details
    chains = ib.reqSecDefOptParams(stock.symbol, '', stock.secType, stock.conId)
    
    if not chains:
        print(f"❌ No option chains found for {symbol}")
        return []
    
    chain = chains[0]
    
    # Use specified expiration or get the nearest one
    if expiration:
        if expiration not in chain.expirations:
            print(f"❌ Expiration {expiration} not found")
            print(f"   Available: {', '.join(chain.expirations[:10])}")
            sys.exit(1)
        expirations = [expiration]
    else:
        # Get next 5 expirations
        expirations = sorted(chain.expirations)[:5]
    
    # Get strikes if not specified
    if strikes is None:
        # Get strikes around current price
        ticker = ib.reqMktData(stock, '', False, False)
        ib.sleep(1)
        current_price = ticker.last or ticker.close
        
        # Get strikes within 20% of current price
        available_strikes = sorted([float(s) for s in chain.strikes])
        strikes = [s for s in available_strikes 
                  if abs(s - current_price) / current_price < 0.20]
    
    # Build option contracts
    contracts = []
    for exp in expirations:
        for strike in strikes:
            opt = Option(symbol, exp, strike, right, 'SMART')
            contracts.append(opt)
    
    # Qualify contracts
    qualified = ib.qualifyContracts(*contracts)
    
    # Get market data
    options_data = []
    for contract in qualified:
        ticker = ib.reqMktData(contract, '', False, False)
        ib.sleep(0.1)  # Small delay between requests
    
    # Wait for data to populate
    ib.sleep(2)
    
    # Collect data
    for i, contract in enumerate(qualified):
        ticker = ib.ticker(contract)
        
        # Calculate Greeks if available
        greeks = ticker.modelGreeks
        delta = greeks.delta if greeks else None
        
        # Calculate days to expiration
        exp_date = datetime.strptime(contract.lastTradeDateOrContractMonth, '%Y%m%d')
        dte = (exp_date - datetime.now()).days
        
        # Calculate moneyness (for puts: (strike - stock) / stock)
        stock_ticker = ib.reqMktData(stock, '', False, False)
        ib.sleep(0.1)
        stock_price = stock_ticker.last or stock_ticker.close
        
        if right == 'P':
            moneyness = ((contract.strike - stock_price) / stock_price) * 100
        else:
            moneyness = ((stock_price - contract.strike) / stock_price) * 100
        
        options_data.append({
            'symbol': contract.symbol,
            'expiration': contract.lastTradeDateOrContractMonth,
            'dte': dte,
            'strike': contract.strike,
            'right': contract.right,
            'bid': ticker.bid,
            'ask': ticker.ask,
            'last': ticker.last,
            'volume': ticker.volume,
            'openInterest': ticker.open,
            'delta': delta,
            'impliedVol': ticker.impliedVolatility,
            'moneyness': moneyness,
            'stock_price': stock_price,
        })
    
    return options_data

def filter_options(options, args):
    """Filter options based on criteria"""
    filtered = options
    
    if args.min_delta:
        filtered = [o for o in filtered if o['delta'] and abs(o['delta']) >= args.min_delta]
    
    if args.max_delta:
        filtered = [o for o in filtered if o['delta'] and abs(o['delta']) <= args.max_delta]
    
    if args.min_volume:
        filtered = [o for o in filtered if o['volume'] and o['volume'] >= args.min_volume]
    
    if args.min_oi:
        filtered = [o for o in filtered if o['openInterest'] and o['openInterest'] >= args.min_oi]
    
    if args.min_dte:
        filtered = [o for o in filtered if o['dte'] >= args.min_dte]
    
    if args.max_dte:
        filtered = [o for o in filtered if o['dte'] <= args.max_dte]
    
    if args.otm_only:
        filtered = [o for o in filtered if o['moneyness'] < 0]
    
    if args.itm_only:
        filtered = [o for o in filtered if o['moneyness'] > 0]
    
    return filtered

def format_option_table(options):
    """Format options as a table"""
    if not options:
        print("No options match the criteria")
        return
    
    # Header
    print(f"\n{'Exp':<10} {'DTE':<5} {'Strike':<8} {'Type':<4} {'Money%':<8} "
          f"{'Bid':<8} {'Ask':<8} {'Last':<8} {'Vol':<8} {'OI':<8} {'Delta':<8} {'IV':<8}")
    print("-" * 110)
    
    # Rows
    for opt in options:
        exp = opt['expiration']
        dte = opt['dte']
        strike = f"${opt['strike']:.2f}"
        right = opt['right']
        moneyness = f"{opt['moneyness']:+.2f}%"
        bid = f"${opt['bid']:.2f}" if opt['bid'] else "—"
        ask = f"${opt['ask']:.2f}" if opt['ask'] else "—"
        last = f"${opt['last']:.2f}" if opt['last'] else "—"
        vol = f"{int(opt['volume'])}" if opt['volume'] else "—"
        oi = f"{int(opt['openInterest'])}" if opt['openInterest'] else "—"
        delta = f"{opt['delta']:.4f}" if opt['delta'] else "—"
        iv = f"{opt['impliedVol']*100:.2f}%" if opt['impliedVol'] else "—"
        
        print(f"{exp:<10} {dte:<5} {strike:<8} {right:<4} {moneyness:<8} "
              f"{bid:<8} {ask:<8} {last:<8} {vol:<8} {oi:<8} {delta:<8} {iv:<8}")

def main():
    parser = argparse.ArgumentParser(
        description='Query IB Gateway for stock quotes and options chains',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get stock quote
  %(prog)s MSFT --quote
  
  # Get put options chain
  %(prog)s MSFT --chain --right P
  
  # Filter by delta and volume
  %(prog)s MSFT --chain --right P --min-delta 0.20 --max-delta 0.35 --min-volume 100
  
  # Filter by days to expiration (30-60 DTE)
  %(prog)s MSFT --chain --right P --min-dte 30 --max-dte 60
  
  # Specific expiration
  %(prog)s MSFT --chain --right P --expiration 20260320
  
  # OTM puts only
  %(prog)s AAPL --chain --right P --otm-only --min-volume 500
        """
    )
    
    parser.add_argument('symbol', help='Stock symbol (e.g., MSFT, AAPL)')
    parser.add_argument('--quote', action='store_true', help='Get stock quote')
    parser.add_argument('--chain', action='store_true', help='Get options chain')
    
    # Connection
    parser.add_argument('--host', default='192.168.11.206', help='IB Gateway host (default: 192.168.11.206)')
    parser.add_argument('--port', type=int, default=4001, help='IB Gateway port (default: 4001 for paper)')
    parser.add_argument('--client-id', type=int, help='Client ID (default: random)')
    
    # Option chain params
    parser.add_argument('--right', choices=['P', 'C'], default='P', help='Option type: P=Put, C=Call (default: P)')
    parser.add_argument('--expiration', help='Specific expiration date (YYYYMMDD)')
    
    # Filters
    parser.add_argument('--min-delta', type=float, help='Minimum delta (absolute value)')
    parser.add_argument('--max-delta', type=float, help='Maximum delta (absolute value)')
    parser.add_argument('--min-volume', type=int, help='Minimum volume')
    parser.add_argument('--min-oi', type=int, help='Minimum open interest')
    parser.add_argument('--min-dte', type=int, help='Minimum days to expiration')
    parser.add_argument('--max-dte', type=int, help='Maximum days to expiration')
    parser.add_argument('--otm-only', action='store_true', help='Only out-of-the-money options')
    parser.add_argument('--itm-only', action='store_true', help='Only in-the-money options')
    
    args = parser.parse_args()
    
    # Validate
    if not args.quote and not args.chain:
        parser.error("Must specify --quote or --chain")
    
    # Connect to IB
    print(f"🔌 Connecting to IB Gateway at {args.host}:{args.port}...")
    ib = connect_ib(args.host, args.port, args.client_id)
    print(f"✅ Connected\n")
    
    try:
        # Get quote
        if args.quote:
            quote = get_stock_quote(ib, args.symbol)
            print(f"\n📊 {args.symbol} Quote")
            print(f"   Last:   ${quote['last']:.2f}")
            print(f"   Bid:    ${quote['bid']:.2f}")
            print(f"   Ask:    ${quote['ask']:.2f}")
            print(f"   Close:  ${quote['close']:.2f}")
            print(f"   Volume: {int(quote['volume']):,}")
        
        # Get chain
        if args.chain:
            print(f"\n🔍 Fetching {args.symbol} option chain...")
            options = get_option_chain(ib, args.symbol, args.expiration, args.right)
            
            if options:
                print(f"   Found {len(options)} contracts")
                
                # Filter
                filtered = filter_options(options, args)
                print(f"   {len(filtered)} match filters")
                
                # Display
                format_option_table(filtered)
            else:
                print("   No options found")
    
    finally:
        ib.disconnect()
        print("\n👋 Disconnected")

if __name__ == '__main__':
    main()
