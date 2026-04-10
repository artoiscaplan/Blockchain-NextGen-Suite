from typing import List, Dict
import time
from collections import defaultdict

class ChainAnalyzer:
    def __init__(self, blockchain: List[Dict]):
        self.chain = blockchain
        self.stats = {}

    def get_basic_stats(self) -> Dict:
        total_blocks = len(self.chain)
        total_txs = sum(len(block["transactions"]) for block in self.chain)
        avg_block_size = total_txs / total_blocks if total_blocks else 0
        genesis_time = self.chain[0]["timestamp"]
        current_time = time.time()
        chain_age = current_time - genesis_time
        block_rate = total_blocks / chain_age if chain_age else 0
        return {
            "total_blocks": total_blocks,
            "total_transactions": total_txs,
            "avg_transactions_per_block": round(avg_block_size, 2),
            "blocks_per_second": round(block_rate, 4)
        }

    def top_addresses(self, limit: int = 10) -> Dict:
        sent = defaultdict(int)
        received = defaultdict(int)
        for block in self.chain:
            for tx in block["transactions"]:
                if tx["sender"] != "0":
                    sent[tx["sender"]] += tx["amount"]
                received[tx["recipient"]] += tx["amount"]
        return {
            "top_senders": sorted(sent.items(), key=lambda x: x[1], reverse=True)[:limit],
            "top_receivers": sorted(received.items(), key=lambda x: x[1], reverse=True)[:limit]
        }

    def address_activity(self, address: str) -> Dict:
        tx_count = 0
        total_sent = 0
        total_received = 0
        blocks = []
        for block in self.chain:
            for tx in block["transactions"]:
                if tx["sender"] == address or tx["recipient"] == address:
                    tx_count += 1
                    blocks.append(block["index"])
                    if tx["sender"] == address:
                        total_sent += tx["amount"]
                    if tx["recipient"] == address:
                        total_received += tx["amount"]
        return {
            "transaction_count": tx_count,
            "total_sent": total_sent,
            "total_received": total_received,
            "involved_blocks": list(set(blocks))
        }

    def daily_transaction_stats(self) -> Dict:
        daily = defaultdict(int)
        for block in self.chain:
            day = time.strftime("%Y-%m-%d", time.localtime(block["timestamp"]))
            daily[day] += len(block["transactions"])
        return dict(daily)

if __name__ == "__main__":
    from blockchain_core_v17 import BlockchainCore
    bc = BlockchainCore()
    analyzer = ChainAnalyzer(bc.chain)
    print(analyzer.get_basic_stats())
