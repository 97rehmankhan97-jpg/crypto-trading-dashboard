#!/usr/bin/env python3
"""
Professional Cryptocurrency Trading Dashboard
Binance BTC/USDT Real-time Analysis
Author: Crypto Trading Team
"""

import asyncio
import json
import time
from datetime import datetime
from collections import deque, defaultdict
import pandas as pd
import numpy as np
from binance.client import Client
from binance.exceptions import BinanceAPIException
from colorama import Fore, Back, Style, init
import websocket
import threading

# Initialize colorama for colored output
init(autoreset=True)

class CryptoTradingDashboard:
    def __init__(self, api_key, api_secret):
        """
        Initialize trading dashboard with Binance API credentials
        """
        self.client = Client(api_key, api_secret)
        self.symbol = 'BTCUSDT'
        self.ws = None
        self.running = True
        
        # Data storage
        self.order_book = {'bids': [], 'asks': []}
        self.trade_history = deque(maxlen=1000)
        self.whale_transactions = deque(maxlen=500)
        self.price_data = deque(maxlen=100)
        self.volume_profile = defaultdict(float)
        self.inflow_outflow = {'inflow': 0, 'outflow': 0}
        
        # Market data
        self.current_price = 0
        self.bid_ask_spread = 0
        self.volume_24h = 0
        self.high_24h = 0
        self.low_24h = 0
        
        print(f"{Fore.GREEN}{'='*80}")
        print(f"{Fore.CYAN}Professional Crypto Trading Dashboard - BTC/USDT")
        print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
    
    def get_order_book(self, limit=20):
        """
        Fetch real-time order book data from Binance
        """
        try:
            depth = self.client.get_order_book(symbol=self.symbol, limit=limit)
            self.order_book['bids'] = depth['bids']
            self.order_book['asks'] = depth['asks']
            return depth
        except BinanceAPIException as e:
            print(f"{Fore.RED}Error fetching order book: {e}{Style.RESET_ALL}")
            return None
    
    def get_recent_trades(self, limit=100):
        """
        Fetch recent trades and analyze for whale transactions
        """
        try:
            trades = self.client.get_recent_trades(symbol=self.symbol, limit=limit)
            
            for trade in trades:
                trade_data = {
                    'time': datetime.fromtimestamp(trade['time']/1000),
                    'price': float(trade['price']),
                    'quantity': float(trade['qty']),
                    'value': float(trade['price']) * float(trade['qty']),
                    'buyer_maker': trade['isBuyerMaker']
                }
                self.trade_history.append(trade_data)
                
                # Detect whale transactions (large orders > 0.5 BTC)
                if trade_data['quantity'] > 0.5:
                    self.whale_transactions.append(trade_data)
            
            return trades
        except BinanceAPIException as e:
            print(f"{Fore.RED}Error fetching trades: {e}{Style.RESET_ALL}")
            return None
    
    def get_24h_stats(self):
        """
        Fetch 24-hour ticker statistics
        """
        try:
            stats = self.client.get_ticker(symbol=self.symbol)
            self.current_price = float(stats['lastPrice'])
            self.volume_24h = float(stats['volume'])
            self.high_24h = float(stats['highPrice'])
            self.low_24h = float(stats['lowPrice'])
            self.bid_ask_spread = float(stats['askPrice']) - float(stats['bidPrice'])
            return stats
        except BinanceAPIException as e:
            print(f"{Fore.RED}Error fetching stats: {e}{Style.RESET_ALL}")
            return None
    
    def calculate_volume_profile(self):
        """
        Calculate volume profile based on price levels
        """
        self.volume_profile.clear()
        
        for trade in self.trade_history:
            # Round price to nearest $100 for profile
            price_level = round(trade['price'] / 100) * 100
            self.volume_profile[price_level] += trade['quantity']
        
        return dict(sorted(self.volume_profile.items()))
    
    def analyze_inflow_outflow(self):
        """
        Analyze inflow (buy) and outflow (sell) based on recent trades
        """
        inflow = 0
        outflow = 0
        
        for trade in self.trade_history:
            if trade['buyer_maker']:
                outflow += trade['value']
            else:
                inflow += trade['value']
        
        self.inflow_outflow = {'inflow': inflow, 'outflow': outflow}
        return self.inflow_outflow
    
    def display_order_book(self):
        """
        Display formatted order book
        """
        print(f"\n{Fore.YELLOW}{'='*80}")
        print(f"{Fore.CYAN}ORDER BOOK - BTC/USDT (Top 10)")
        print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}")
        
        # Display asks (sell orders)
        print(f"\n{Fore.RED}ASKS (Sell Orders):")
        print(f"{Fore.WHITE}{'Price (USDT)':<20} {'Quantity (BTC)':<20} {'Total (USDT)':<20}")
        print(f"{Fore.RED}{'-'*60}")
        
        if self.order_book['asks']:
            for ask in reversed(self.order_book['asks'][:10]):
                price = float(ask[0])
                qty = float(ask[1])
                total = price * qty
                print(f"{Fore.RED}{price:<20.2f} {qty:<20.4f} {total:<20.2f}")
        
        # Display current price
        print(f"\n{Fore.GREEN}Current Price: {Fore.YELLOW}${self.current_price:.2f}")
        print(f"{Fore.CYAN}Bid-Ask Spread: {Fore.YELLOW}${self.bid_ask_spread:.2f}")
        
        # Display bids (buy orders)
        print(f"\n{Fore.GREEN}BIDS (Buy Orders):")
        print(f"{Fore.WHITE}{'Price (USDT)':<20} {'Quantity (BTC)':<20} {'Total (USDT)':<20}")
        print(f"{Fore.GREEN}{'-'*60}")
        
        if self.order_book['bids']:
            for bid in self.order_book['bids'][:10]:
                price = float(bid[0])
                qty = float(bid[1])
                total = price * qty
                print(f"{Fore.GREEN}{price:<20.2f} {qty:<20.4f} {total:<20.2f}")
    
    def display_whale_transactions(self):
        """
        Display recent whale transactions (>0.5 BTC)
        """
        print(f"\n{Fore.YELLOW}{'='*80}")
        print(f"{Fore.MAGENTA}WHALE TRANSACTIONS (>0.5 BTC)")
        print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'Time':<25} {'Price':<15} {'Quantity':<15} {'Value (USDT)':<20} {'Type':<10}")
        print(f"{Fore.MAGENTA}{'-'*85}")
        
        if self.whale_transactions:
            for trade in list(self.whale_transactions)[-10:]:
                trade_type = f"{Fore.GREEN}BUY" if not trade['buyer_maker'] else f"{Fore.RED}SELL"
                print(f"{Fore.WHITE}{str(trade['time']):<25} ${trade['price']:<14.2f} {trade['quantity']:<14.4f} ${trade['value']:<19.2f} {trade_type}")
        else:
            print(f"{Fore.YELLOW}No whale transactions detected recently")
    
    def display_volume_profile(self):
        """
        Display volume profile (volume by price level)
        """
        print(f"\n{Fore.YELLOW}{'='*80}")
        print(f"{Fore.CYAN}VOLUME PROFILE (Grouped by $100)")
        print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'Price Level':<20} {'Volume (BTC)':<20} {'Volume Chart':<40}")
        print(f"{Fore.CYAN}{'-'*80}")
        
        profile = self.calculate_volume_profile()
        if profile:
            max_volume = max(profile.values())
            for price_level in sorted(profile.keys(), reverse=True)[:20]:
                volume = profile[price_level]
                bar_length = int((volume / max_volume) * 30) if max_volume > 0 else 0
                bar = '█' * bar_length
                print(f"{Fore.CYAN}${price_level:<19.2f} {volume:<19.4f} {Fore.GREEN}{bar}")
    
    def display_inflow_outflow(self):
        """
        Display inflow/outflow analysis
        """
        print(f"\n{Fore.YELLOW}{'='*80}")
        print(f"{Fore.CYAN}INFLOW / OUTFLOW ANALYSIS")
        print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}")
        
        inflow = self.inflow_outflow['inflow']
        outflow = self.inflow_outflow['outflow']
        net_flow = inflow - outflow
        
        print(f"{Fore.GREEN}Inflow (Buying):  ${inflow:>20,.2f}")
        print(f"{Fore.RED}Outflow (Selling): ${outflow:>20,.2f}")
        print(f"{Fore.CYAN}Net Flow:         ${net_flow:>20,.2f}")
        
        if net_flow > 0:
            print(f"{Fore.GREEN}Status: BULLISH (More buying than selling)")
        else:
            print(f"{Fore.RED}Status: BEARISH (More selling than buying)")
        
        inflow_pct = (inflow / (inflow + outflow) * 100) if (inflow + outflow) > 0 else 0
        print(f"{Fore.CYAN}Inflow Percentage: {inflow_pct:.2f}%")
    
    def display_market_stats(self):
        """
        Display 24-hour market statistics
        """
        print(f"\n{Fore.YELLOW}{'='*80}")
        print(f"{Fore.CYAN}24-HOUR MARKET STATISTICS")
        print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Current Price:    ${self.current_price:>20,.2f}")
        print(f"{Fore.CYAN}24H High:         ${self.high_24h:>20,.2f}")
        print(f"{Fore.CYAN}24H Low:          ${self.low_24h:>20,.2f}")
        print(f"{Fore.CYAN}24H Volume:       {self.volume_24h:>20,.2f} BTC")
        print(f"{Fore.MAGENTA}Bid-Ask Spread:   ${self.bid_ask_spread:>20,.4f}")
    
    def run_dashboard(self, refresh_interval=5):
        """
        Run the continuous dashboard update
        """
        try:
            while self.running:
                print(f"\n{Fore.YELLOW}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Updating data...{Style.RESET_ALL}")
                
                # Fetch all data
                self.get_24h_stats()
                self.get_order_book(limit=20)
                self.get_recent_trades(limit=100)
                self.analyze_inflow_outflow()
                
                # Clear screen and display dashboard
                print("\033[2J\033[H")  # Clear screen
                
                # Display all sections
                self.display_market_stats()
                self.display_order_book()
                self.display_whale_transactions()
                self.display_inflow_outflow()
                self.display_volume_profile()
                
                print(f"\n{Fore.YELLOW}Next update in {refresh_interval} seconds... (Press Ctrl+C to exit)")
                time.sleep(refresh_interval)
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Dashboard stopped by user{Style.RESET_ALL}")
            self.running = False
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            self.running = False


def main():
    """
    Main function to run the trading dashboard
    """
    # Binance API credentials (Replace with your actual keys)
    API_KEY = "your_binance_api_key_here"
    API_SECRET = "your_binance_api_secret_here"
    
    # For testing without real credentials, you can use empty strings
    # But API calls will fail - get real keys from https://www.binance.com/en/account/api-management
    
    dashboard = CryptoTradingDashboard(API_KEY, API_SECRET)
    dashboard.run_dashboard(refresh_interval=5)  # Update every 5 seconds


if __name__ == "__main__":
    main()