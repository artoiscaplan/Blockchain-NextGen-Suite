import requests
import json
from typing import Dict, Optional

class SolanaRPCClient:
    def __init__(self, rpc_url: str = "https://api.mainnet-beta.solana.com"):
        self.rpc_url = rpc_url
        self.headers = {"Content-Type": "application/json"}

    def _call(self, method: str, params: list) -> Optional[Dict]:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        try:
            resp = requests.post(self.rpc_url, headers=self.headers, data=json.dumps(payload))
            return resp.json().get("result")
        except:
            return None

    def get_slot(self) -> Optional[int]:
        res = self._call("getSlot", [])
        return res if res else None

    def get_balance(self, address: str) -> Optional[float]:
        res = self._call("getBalance", [address])
        if res and "value" in res:
            return res["value"] / 1e9
        return None

    def get_block_time(self, slot: int) -> Optional[int]:
        return self._call("getBlockTime", [slot])

    def get_transaction(self, tx_sig: str) -> Optional[Dict]:
        return self._call("getTransaction", [tx_sig, {"encoding": "json"}])

    def send_transaction(self, signed_tx: str) -> Optional[str]:
        res = self._call("sendTransaction", [signed_tx, {"encoding": "base64"}])
        return res if res else None

    def get_latest_blockhash(self) -> Optional[str]:
        res = self._call("getLatestBlockhash", [])
        if res:
            return res["value"]["blockhash"]
        return None

    def get_account_info(self, address: str) -> Optional[Dict]:
        return self._call("getAccountInfo", [address, {"encoding": "base64"}])

if __name__ == "__main__":
    client = SolanaRPCClient()
    print("当前Slot:", client.get_slot())
