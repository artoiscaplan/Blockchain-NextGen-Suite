import hashlib
import json
import time
from typing import List, Dict

class BlockchainCore:
    def __init__(self):
        self.chain: List[Dict] = []
        self.pending_transactions: List[Dict] = []
        self.difficulty = 4
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        genesis_block = {
            "index": 0,
            "timestamp": time.time(),
            "transactions": [],
            "proof": 100,
            "previous_hash": "0",
            "merkle_root": self.calculate_merkle_root([])
        }
        genesis_block["hash"] = self.hash_block(genesis_block)
        self.chain.append(genesis_block)

    @staticmethod
    def hash_block(block: Dict) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_last_block(self) -> Dict:
        return self.chain[-1]

    def add_transaction(self, sender: str, recipient: str, amount: float, data: str = "") -> int:
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "data": data,
            "tx_time": time.time()
        })
        return self.get_last_block()["index"] + 1

    def calculate_merkle_root(self, transactions: List[Dict]) -> str:
        if not transactions:
            return hashlib.sha256(b"empty").hexdigest()
        tx_hashes = [hashlib.sha256(json.dumps(tx).encode()).hexdigest() for tx in transactions]
        while len(tx_hashes) > 1:
            temp = []
            for i in range(0, len(tx_hashes), 2):
                left = tx_hashes[i]
                right = tx_hashes[i+1] if i+1 < len(tx_hashes) else left
                combined = hashlib.sha256((left+right).encode()).hexdigest()
                temp.append(combined)
            tx_hashes = temp
        return tx_hashes[0]

    def mine_block(self, miner_address: str) -> Dict:
        if not self.pending_transactions:
            raise Exception("无待处理交易")
        self.add_transaction(
            sender="0",
            recipient=miner_address,
            amount=5.0,
            data="区块奖励"
        )
        last_block = self.get_last_block()
        proof = self.proof_of_work(last_block)
        block = {
            "index": last_block["index"] + 1,
            "timestamp": time.time(),
            "transactions": self.pending_transactions,
            "proof": proof,
            "previous_hash": last_block["hash"],
            "merkle_root": self.calculate_merkle_root(self.pending_transactions)
        }
        block["hash"] = self.hash_block(block)
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def proof_of_work(self, last_block: Dict) -> int:
        proof = 0
        while not self.valid_proof(last_block["hash"], proof, self.difficulty):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_hash: str, proof: int, difficulty: int) -> bool:
        guess = f"{last_hash}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:difficulty] == "0" * difficulty

    def validate_chain(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current["previous_hash"] != previous["hash"]:
                return False
            if not self.valid_proof(previous["hash"], current["proof"], self.difficulty):
                return False
            if current["merkle_root"] != self.calculate_merkle_root(current["transactions"]):
                return False
        return True

if __name__ == "__main__":
    bc = BlockchainCore()
    print("创世区块链已创建")
