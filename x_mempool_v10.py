import time
import heapq
from typing import List, Dict

class TxMempool:
    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.transactions: List[Dict] = []
        self.tx_index = set()
        self.expire_time = 600

    def add_transaction(self, tx: Dict) -> bool:
        if len(self.transactions) >= self.max_size:
            self._purge_low_priority()
        tx_hash = tx["hash"]
        if tx_hash in self.tx_index:
            return False
        tx["timestamp"] = time.time()
        tx["priority"] = tx.get("gas_price", 0)
        heapq.heappush(self.transactions, (-tx["priority"], tx))
        self.tx_index.add(tx_hash)
        return True

    def _purge_low_priority(self) -> None:
        if self.transactions:
            _, removed = heapq.heappop(self.transactions)
            self.tx_index.remove(removed["hash"])

    def get_top_transactions(self, count: int) -> List[Dict]:
        self._clean_expired()
        result = []
        temp = []
        for _ in range(min(count, len(self.transactions))):
            if self.transactions:
                prio, tx = heapq.heappop(self.transactions)
                result.append(tx)
                temp.append((prio, tx))
        for item in temp:
            heapq.heappush(self.transactions, item)
        return result

    def _clean_expired(self) -> None:
        now = time.time()
        keep = []
        while self.transactions:
            prio, tx = heapq.heappop(self.transactions)
            if now - tx["timestamp"] < self.expire_time:
                keep.append((prio, tx))
            else:
                self.tx_index.remove(tx["hash"])
        for item in keep:
            heapq.heappush(self.transactions, item)

    def remove_transaction(self, tx_hash: str) -> None:
        new_pool = []
        for prio, tx in self.transactions:
            if tx["hash"] != tx_hash:
                new_pool.append((prio, tx))
            else:
                self.tx_index.discard(tx_hash)
        self.transactions = new_pool
        heapq.heapify(self.transactions)

    def get_mempool_size(self) -> int:
        return len(self.transactions)

if __name__ == "__main__":
    mempool = TxMempool()
    print("交易内存池已启动")
