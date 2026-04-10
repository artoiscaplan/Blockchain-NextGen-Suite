import json
import gzip
import os
import time
from typing import Dict, List

class ChainSnapshot:
    def __init__(self, blockchain: List[Dict], snapshot_dir: str = "snapshots"):
        self.blockchain = blockchain
        self.snapshot_dir = snapshot_dir
        os.makedirs(snapshot_dir, exist_ok=True)

    def create_full_snapshot(self) -> str:
        snapshot_data = {
            "snapshot_time": time.time(),
            "block_height": len(self.blockchain) - 1,
            "chain_data": self.blockchain,
            "metadata": {
                "version": "1.0",
                "compression": "gzip"
            }
        }
        filename = f"snapshot_full_{int(time.time())}_{len(self.blockchain)-1}.json.gz"
        path = os.path.join(self.snapshot_dir, filename)
        with gzip.open(path, 'wt', encoding='utf-8') as f:
            json.dump(snapshot_data, f)
        return path

    def create_state_snapshot(self, height: int) -> str:
        if height >= len(self.blockchain):
            raise Exception("高度超出链长度")
        state = {
            "block_height": height,
            "block_hash": self.blockchain[height]["hash"],
            "timestamp": time.time(),
            "balances": self._extract_balances(height)
        }
        filename = f"snapshot_state_{height}_{int(time.time())}.json"
        path = os.path.join(self.snapshot_dir, filename)
        with open(path, 'w') as f:
            json.dump(state, f)
        return path

    def _extract_balances(self, height: int) -> Dict:
        balances = {}
        for i in range(height + 1):
            for tx in self.blockchain[i]["transactions"]:
                sender = tx["sender"]
                recv = tx["recipient"]
                amt = tx["amount"]
                if sender != "0":
                    balances[sender] = balances.get(sender, 0) - amt
                balances[recv] = balances.get(recv, 0) + amt
        return balances

    def load_snapshot(self, path: str) -> List[Dict]:
        if not os.path.exists(path):
            raise Exception("快照不存在")
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            data = json.load(f)
        return data["chain_data"]

    def list_snapshots(self) -> List[str]:
        return [f for f in os.listdir(self.snapshot_dir)]

if __name__ == "__main__":
    from blockchain_core_v17 import BlockchainCore
    bc = BlockchainCore()
    snap = ChainSnapshot(bc.chain)
    print("快照文件:", snap.create_full_snapshot())
