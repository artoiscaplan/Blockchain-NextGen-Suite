import hashlib
import time
from typing import Dict, List

class MultiSignWallet:
    def __init__(self, owners: list, required: int):
        self.owners = set(owners)
        self.required = required
        self.transactions: Dict[str, Dict] = {}
        self.balances: Dict[str, float] = {}

    def deposit(self, sender: str, amount: float) -> None:
        if amount <= 0:
            raise Exception("金额必须大于0")
        self.balances[sender] = self.balances.get(sender, 0) + amount

    def create_transaction(self, creator: str, to: str, amount: float) -> str:
        if creator not in self.owners:
            raise Exception("非钱包所有者")
        tx_id = hashlib.sha256(f"{creator}{to}{amount}{time.time()}".encode()).hexdigest()
        self.transactions[tx_id] = {
            "to": to,
            "amount": amount,
            "signatures": [],
            "executed": False
        }
        return tx_id

    def sign_transaction(self, signer: str, tx_id: str) -> None:
        if signer not in self.owners:
            raise Exception("无签名权限")
        if tx_id not in self.transactions:
            raise Exception("交易不存在")
        tx = self.transactions[tx_id]
        if tx["executed"]:
            raise Exception("交易已执行")
        if signer in tx["signatures"]:
            raise Exception("已签名")
        tx["signatures"].append(signer)

    def execute_transaction(self, tx_id: str) -> None:
        if tx_id not in self.transactions:
            raise Exception("交易不存在")
        tx = self.transactions[tx_id]
        if len(tx["signatures"]) < self.required:
            raise Exception("签名不足")
        if tx["executed"]:
            raise Exception("已执行")
        tx["executed"] = True

    def get_transaction(self, tx_id: str) -> Dict:
        return self.transactions.get(tx_id, {})

    def get_wallet_info(self) -> Dict:
        return {
            "owners": list(self.owners),
            "required_signatures": self.required,
            "pending_txs": len([t for t in self.transactions.values() if not t["executed"]])
        }

if __name__ == "__main__":
    wallet = MultiSignWallet(["user1", "user2", "user3"], 2)
    print("多签钱包信息:", wallet.get_wallet_info())
