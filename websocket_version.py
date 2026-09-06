#!/usr/bin/env python3
"""
WebSocket Real-time Crypto Trading Dashboard
For ultra-fast real-time data updates (every tick)
"""

import websocket
import json
import threading
import time
from datetime import datetime
from collections import deque
from colorama import Fore, Back, Style, init

init(autoreset=True)

class RealtimeDashboard:
    def __init__(self):
        self.ws = None
        self.running = True
        self.order_book = {'bids': {}, 'asks': {}}
        self.recent_trades = deque(maxlen=100)
        self.whale_threshold = 0.5  # BTC
        
    def on_message(self, ws, message):
        """
        Handle incoming WebSocket messages
        """
        try:
            data = json.loads(message)
            
            if 'e' in data:
                event_type = data['e']
                
                # Depth (order book) updates
                if event_type == 'depthUpdate':
                    self.process_depth_update(data)
                
                # Trade updates
                elif event_type == 'trade':
                    self.process_trade(data)
                
                # Kline (candlestick) updates
                elif event_type == 'kline':
                    self.process_kline(data)
        
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(f"{Fore.RED}Error processing message: {e}")
    
    def process_depth_update(self, data):
        """
        Process order book update
        """
        # Update bids
        for bid in data.get('b', []):
            price, qty = float(bid[0]), float(bid[1])
            if qty == 0:
                self.order_book['bids'].pop(price, None)
            else:
                self.order_book['bids'][price] = qty
        
        # Update asks
        for ask in data.get('a', []):
            price, qty = float(ask[0]), float(ask[1])
            if qty == 0:
                self.order_book['asks'].pop(price, None)
            else:
                self.order_book['asks'][price] = qty
    
    def process_trade(self, data):
        """
        Process trade data
        """
        trade = {
            'time': datetime.fromtimestamp(data['T'] / 1000),
            'price': float(data['p']),
            'quantity': float(data['q']),
            'value': float(data['p']) * float(data['q']),
            'buyer_maker': data['m'],
            'trade_id': data['t']
        }
        
        self.recent_trades.append(trade)
        
        # Alert for whale transactions
        if trade['quantity'] >= self.whale_threshold:
            self.alert_whale(trade)
    
    def process_kline(self, data):
        """
        Process candlestick data
        """
        kline = data['k']
        print(f"\n{Fore.CYAN}Kline: {kline['c']} (Close: {kline['C']})")
    
    def alert_whale(self, trade):
        """
        Alert for whale transactions
        """
        trade_type = f"{Fore.GREEN}BUY" if not trade['buyer_maker'] else f"{Fore.RED}SELL"
        print(f"\n{Fore.MAGENTA}🐋 WHALE ALERT! {trade_type}")
        print(f"{Fore.MAGENTA}Price: ${trade['price']:.2f} | Qty: {trade['quantity']:.4f} BTC | Value: ${trade['value']:.2f}")
    
    def on_error(self, ws, error):
        print(f"{Fore.RED}WebSocket Error: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        print(f"{Fore.YELLOW}WebSocket closed")
        self.running = False
    
    def on_open(self, ws):
        print(f"{Fore.GREEN}WebSocket connected!")
    
    def connect(self):
        """
        Connect to Binance WebSocket streams
        """
        # Multiple streams: depth, trades, klines
        streams = [
            'btcusdt@depth@100ms',  # Order book depth updates
            'btcusdt@trade',         # Trade updates
            'btcusdt@kline_1s'       # 1-second candles
        ]
        
        url = f"wss://stream.binance.com:9443/stream?streams={''.join([s + '/' for s in streams[:-1]])} + streams[2]"
        
        print(f"{Fore.CYAN}Connecting to Binance WebSocket...")
        
        self.ws = websocket.WebSocketApp(
            url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        
        self.ws.run_forever()

def main():
    dashboard = RealtimeDashboard()
    dashboard.connect()

if __name__ == "__main__":
    main()