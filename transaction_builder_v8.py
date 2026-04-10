import json
import time
import hashlib
from typing import Optional, Dict

class TransactionBuilder:
    def __init__(self, chain_id: int = 1):
        self.chain_id = chain_id
        self.nonce = 0

    def build_transfer_tx(self, sender: str, to: str, value: float, gas: int = 21000, gas_price: float = 1e-9) -> Dict:
        tx = {
            "type": "transfer",
            "sender": sender,
            "to": to,
            "value": value,
            "gas": gas,
            "gas_price": gas_price,
            "nonce": self.nonce,
            "chain_id": self.chain_id,
            "timestamp": time.time()
        }
        self.nonce += 1
        tx["hash"] = self._tx_hash(tx)
        return tx

    def build_contract_tx(self, sender: str, contract: str, data: str, value: float = 0) -> Dict:
        tx = {
            "type": "contract_call",
            "sender": sender,
            "contract": contract,
            "data": data,
            "value": value,
            "nonce": self.nonce,
            "chain_id": self.chain_id,
            "timestamp": time.time()
        }
        self.nonce += 1
        tx["hash"] = self._tx_hash(tx)
        return tx

    def build_multisig_tx(self, owners: list, to: str, value: float, required: int) -> Dict:
        tx = {
            "type": "multisig",
            "owners": owners,
            "to": to,
            "value": value,
            "required_signatures": required,
            "signatures": [],
            "nonce": self.nonce,
            "timestamp": time.time()
        }
        self.nonce += 1
        tx["hash"] = self._tx_hash(tx)
        return tx

    def serialize_tx(self, tx: Dict) -> str:
        return json.dumps(tx, sort_keys=True)

    def deserialize_tx(self, raw: str) -> Dict:
        return json.loads(raw)

    def _tx_hash(self, tx: Dict) -> str:
        raw = json.dumps(tx, sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()

if __name__ == "__main__":
    tb = TransactionBuilder()
    tx = tb.build_transfer_tx("addr1", "addr2", 1.5)
    print("交易哈希:", tx["hash"])
