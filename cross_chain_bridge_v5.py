import hashlib
import time
from typing import Dict, List, Optional

class CrossChainBridge:
    def __init__(self):
        self.supported_chains = ["ETH", "BSC", "SOL", "TRON"]
        self.locked_assets: Dict[str, Dict] = {}
        self.minted_wrapped: Dict[str, Dict] = {}
        self.validators = ["validator1", "validator2", "validator3"]
        self.required_signs = 2

    def lock_asset(self, user: str, from_chain: str, to_chain: str, symbol: str, amount: float) -> str:
        if from_chain not in self.supported_chains or to_chain not in self.supported_chains:
            raise Exception("链不支持")
        tx_id = hashlib.sha256(f"{user}{from_chain}{to_chain}{amount}{time.time()}".encode()).hexdigest()
        self.locked_assets[tx_id] = {
            "user": user,
            "from_chain": from_chain,
            "to_chain": to_chain,
            "symbol": symbol,
            "amount": amount,
            "status": "locked",
            "timestamp": time.time()
        }
        return tx_id

    def mint_wrapped(self, tx_id: str, signatures: List[str]) -> None:
        if tx_id not in self.locked_assets:
            raise Exception("交易不存在")
        valid_signs = [s for s in signatures if s in self.validators]
        if len(valid_signs) < self.required_signs:
            raise Exception("签名不足")
        data = self.locked_assets[tx_id]
        data["status"] = "minted"
        self.minted_wrapped[tx_id] = data
        self.locked_assets[tx_id]["status"] = "minted"

    def unlock_asset(self, user: str, tx_id: str, signatures: List[str]) -> None:
        if tx_id not in self.minted_wrapped:
            raise Exception("无映射资产")
        valid_signs = [s for s in signatures if s in self.validators]
        if len(valid_signs) < self.required_signs:
            raise Exception("签名不足")
        self.minted_wrapped[tx_id]["status"] = "unlocked"
        self.locked_assets[tx_id]["status"] = "unlocked"

    def get_tx_status(self, tx_id: str) -> Optional[Dict]:
        if tx_id in self.locked_assets:
            return self.locked_assets[tx_id]
        return None

    def get_supported_chains(self) -> List[str]:
        return self.supported_chains

if __name__ == "__main__":
    bridge = CrossChainBridge()
    tx = bridge.lock_asset("user", "ETH", "BSC", "USDT", 100)
    print("跨链交易ID:", tx)
