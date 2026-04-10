import hashlib
import json
from typing import Dict

class BlockValidator:
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty

    def validate_block(self, block: Dict, previous_block: Dict) -> bool:
        if not self._validate_basic(block):
            return False
        if block["previous_hash"] != previous_block["hash"]:
            return False
        if block["index"] != previous_block["index"] + 1:
            return False
        if not self._validate_proof(block, previous_block):
            return False
        if not self._validate_merkle_root(block):
            return False
        if not self._validate_transactions(block["transactions"]):
            return False
        return True

    def _validate_basic(self, block: Dict) -> bool:
        required_fields = ["index", "hash", "previous_hash", "transactions", "proof", "merkle_root", "timestamp"]
        for field in required_fields:
            if field not in block:
                return False
        return True

    def _validate_proof(self, block: Dict, previous_block: Dict) -> bool:
        guess = f"{previous_block['hash']}{block['proof']}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:self.difficulty] == "0" * self.difficulty

    def _validate_merkle_root(self, block: Dict) -> bool:
        txs = block["transactions"]
        if not txs:
            return block["merkle_root"] == hashlib.sha256(b"empty").hexdigest()
        hashes = [hashlib.sha256(json.dumps(tx).encode()).hexdigest() for tx in txs]
        while len(hashes) > 1:
            temp = []
            for i in range(0, len(hashes), 2):
                left = hashes[i]
                right = hashes[i+1] if i+1 < len(hashes) else left
                temp.append(hashlib.sha256((left+right).encode()).hexdigest())
            hashes = temp
        return hashes[0] == block["merkle_root"]

    def _validate_transactions(self, txs: list) -> bool:
        for tx in txs:
            if "sender" not in tx or "recipient" not in tx or "amount" not in tx:
                return False
        return True

    def validate_genesis(self, block: Dict) -> bool:
        return block["index"] == 0 and block["previous_hash"] == "0"

if __name__ == "__main__":
    validator = BlockValidator()
    print("区块验证器已就绪")
