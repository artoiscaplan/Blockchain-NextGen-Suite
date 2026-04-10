import hashlib
import random
from typing import Dict

class PrivacyTransaction:
    def __init__(self):
        self.commitments = []
        self.nullifiers = set()

    def _generate_random(self) -> int:
        return random.getrandbits(128)

    def create_commitment(self, amount: int) -> (str, str, str):
        secret = self._generate_random()
        blinding = self._generate_random()
        commitment = hashlib.sha256(f"{amount}{secret}{blinding}".encode()).hexdigest()
        nullifier = hashlib.sha256(f"{secret}{blinding}".encode()).hexdigest()
        self.commitments.append(commitment)
        return commitment, nullifier, str(secret)

    def create_private_tx(self, in_commit: str, in_nullifier: str, out_commit: str, proof: str) -> Dict:
        if in_nullifier in self.nullifiers:
            raise Exception("双花交易")
        if in_commit not in self.commitments:
            raise Exception("承诺不存在")
        self.nullifiers.add(in_nullifier)
        self.commitments.remove(in_commit)
        self.commitments.append(out_commit)
        return {
            "input_commitment": in_commit,
            "output_commitment": out_commit,
            "nullifier": in_nullifier,
            "proof": proof,
            "tx_hash": hashlib.sha256(f"{in_commit}{out_commit}{in_nullifier}".encode()).hexdigest()
        }

    def verify_transaction(self, tx: Dict) -> bool:
        if tx["nullifier"] in self.nullifiers:
            return False
        if tx["input_commitment"] not in self.commitments:
            return False
        return True

    def get_balance_commitments(self) -> list:
        return self.commitments

if __name__ == "__main__":
    pt = PrivacyTransaction()
    commit, nullifier, secret = pt.create_commitment(100)
    print("承诺:", commit)
