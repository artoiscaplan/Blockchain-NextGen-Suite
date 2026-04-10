import hashlib
import time
from typing import Dict

class MetaTransaction:
    def __init__(self):
        self.nonce = {}

    def get_nonce(self, user: str) -> int:
        return self.nonce.get(user, 0)

    def sign_meta_tx(self, user: str, to: str, value: float, data: str, private_key: str) -> str:
        nonce = self.get_nonce(user)
        msg = f"{user}{to}{value}{data}{nonce}"
        signature = hashlib.sha256((private_key + msg).encode()).hexdigest()
        return signature

    def execute_meta_tx(self, user: str, to: str, value: float, data: str, signature: str, relayer: str) -> Dict:
        nonce = self.get_nonce(user)
        expected = self.sign_meta_tx(user, to, value, data, "fake_pk")
        if signature != expected:
            raise Exception("签名无效")
        self.nonce[user] = nonce + 1
        return {
            "success": True,
            "tx_hash": hashlib.sha256(f"{user}{to}{time.time()}".encode()).hexdigest(),
            "relayer": relayer,
            "gas_paid": True
        }

    def create_relay_request(self, user: str, tx_data: Dict) -> Dict:
        return {
            "user": user,
            "tx": tx_data,
            "nonce": self.get_nonce(user),
            "request_time": time.time(),
            "relay_fee": 0.001
        }

    def verify_relay_request(self, req: Dict, signature: str) -> bool:
        msg = f"{req['user']}{req['tx']}{req['nonce']}"
        expected = hashlib.sha256(msg.encode()).hexdigest()
        return signature == expected

if __name__ == "__main__":
    meta = MetaTransaction()
    sig = meta.sign_meta_tx("user1", "contract1", 0, "0x1234", "pk123")
    print("元交易签名:", sig)
