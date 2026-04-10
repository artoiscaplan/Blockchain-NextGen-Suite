import hashlib
import random
from typing import Tuple, Dict

class ZKProof:
    def __init__(self):
        self.prime = 104729

    def _mod(self, x: int) -> int:
        return x % self.prime

    def generate_proof(self, secret: int, public: int) -> Tuple[Dict, int]:
        r = random.randint(1, self.prime-1)
        a = self._mod(r * public)
        c = random.randint(1, self.prime-1)
        s = self._mod(r + c * secret)
        proof = {
            "a": a,
            "c": c,
            "s": s,
            "public": public
        }
        return proof, secret

    def verify_proof(self, proof: Dict) -> bool:
        a = proof["a"]
        c = proof["c"]
        s = proof["s"]
        public = proof["public"]
        left = self._mod(s * public)
        right = self._mod(a + c * self._mod(public * public))
        return left == right

    def create_private_transaction(self, sender: str, receiver: str, amount: int) -> Dict:
        secret = random.getrandbits(64)
        public = self._mod(secret * random.randint(2, 100))
        proof, _ = self.generate_proof(secret, public)
        return {
            "sender_hash": hashlib.sha256(sender.encode()).hexdigest(),
            "receiver_hash": hashlib.sha256(receiver.encode()).hexdigest(),
            "amount_commitment": hashlib.sha256(str(amount).encode()).hexdigest(),
            "zk_proof": proof,
            "valid": self.verify_proof(proof)
        }

if __name__ == "__main__":
    zk = ZKProof()
    proof, secret = zk.generate_proof(12345, 6789)
    print("验证结果:", zk.verify_proof(proof))
