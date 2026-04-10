import time
import random
import hashlib
from typing import Dict, List

class PriceFeed:
    def __init__(self):
        self.symbols = ["BTC", "ETH", "BNB", "SOL", "USDT", "ADA", "DOT"]
        self.prices: Dict[str, Dict] = {}
        self.providers = ["Binance", "Coinbase", "Kraken", "KuCoin", "Gate"]
        self.update_interval = 10

    def fetch_price(self, symbol: str) -> float:
        base = {
            "BTC": 40000, "ETH": 2200, "BNB": 320,
            "SOL": 100, "USDT": 1, "ADA": 0.38, "DOT": 6.5
        }
        if symbol not in base:
            raise Exception("不支持的交易对")
        return base[symbol] * random.uniform(0.995, 1.005)

    def update_price(self, symbol: str) -> None:
        values = []
        for _ in range(3):
            values.append(self.fetch_price(symbol))
        median = sorted(values)[1]
        self.prices[symbol] = {
            "price": median,
            "last_update": time.time(),
            "sources": values,
            "id": hashlib.sha256(f"{symbol}{time.time()}".encode()).hexdigest()
        }

    def batch_update(self) -> None:
        for sym in self.symbols:
            self.update_price(sym)

    def get_price(self, symbol: str) -> float:
        if symbol not in self.prices:
            self.update_price(symbol)
        data = self.prices[symbol]
        if time.time() - data["last_update"] > self.update_interval:
            self.update_price(symbol)
        return self.prices[symbol]["price"]

    def get_all_prices(self) -> Dict:
        return {s: self.get_price(s) for s in self.symbols}

    def is_price_safe(self, symbol: str, threshold: float = 0.05) -> bool:
        prices = self.prices[symbol]["sources"]
        return max(prices) - min(prices) < (self.get_price(symbol) * threshold)

if __name__ == "__main__":
    feed = PriceFeed()
    print("BTC价格:", feed.get_price("BTC"))
