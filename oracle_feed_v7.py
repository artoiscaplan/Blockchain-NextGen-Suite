import hashlib
import time
import random
from typing import Dict, List

class OracleFeed:
    def __init__(self):
        self.sources = ["source1", "source2", "source3", "source4", "source5"]
        self.data: Dict[str, Dict] = {}
        self.threshold = 3

    def request_data(self, data_type: str, callback_id: str) -> None:
        self.data[callback_id] = {
            "type": data_type,
            "status": "pending",
            "values": [],
            "result": None,
            "timestamp": time.time()
        }

    def submit_data(self, source: str, callback_id: str, value: float) -> None:
        if source not in self.sources:
            raise Exception("非法数据源")
        if callback_id not in self.data:
            raise Exception("请求ID不存在")
        req = self.data[callback_id]
        if req["status"] != "pending":
            return
        req["values"].append(value)
        if len(req["values"]) >= self.threshold:
            req["result"] = self._aggregate(req["values"])
            req["status"] = "fulfilled"

    def _aggregate(self, values: List[float]) -> float:
        values.sort()
        mid = len(values) // 2
        return values[mid]

    def get_result(self, callback_id: str) -> Dict:
        return self.data.get(callback_id, {})

    def get_price_feed(self, symbol: str) -> float:
        req_id = hashlib.sha256(symbol.encode()).hexdigest()
        self.request_data("price", req_id)
        for src in self.sources[:3]:
            val = random.uniform(1000, 1050)
            self.submit_data(src, req_id, val)
        return self.get_result(req_id)["result"]

if __name__ == "__main__":
    oracle = OracleFeed()
    print("BTC价格:", oracle.get_price_feed("BTC"))
