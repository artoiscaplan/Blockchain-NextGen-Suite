import requests
import time
import json
from typing import Callable, Dict

class EthereumEventListener:
    def __init__(self, rpc_url: str, contract_address: str):
        self.rpc_url = rpc_url
        self.contract = contract_address.lower()
        self.last_block = 0

    def _get_block_number(self) -> int:
        payload = {"jsonrpc": "2.0", "id": 1, "method": "eth_blockNumber", "params": []}
        resp = requests.post(self.rpc_url, json=payload).json()
        return int(resp["result"], 16)

    def _get_logs(self, from_block: int, to_block: int) -> list:
        f_hex = hex(from_block)
        t_hex = hex(to_block)
        payload = {
            "jsonrpc": "2.0", "id": 1,
            "method": "eth_getLogs",
            "params": [{
                "address": self.contract,
                "fromBlock": f_hex,
                "toBlock": t_hex
            }]
        }
        resp = requests.post(self.rpc_url, json=payload).json()
        return resp.get("result", [])

    def start_listen(self, callback: Callable[[Dict], None], interval: int = 5) -> None:
        self.last_block = self._get_block_number()
        while True:
            try:
                current = self._get_block_number()
                if current > self.last_block:
                    logs = self._get_logs(self.last_block + 1, current)
                    for log in logs:
                        callback(log)
                    self.last_block = current
            except Exception as e:
                print("监听错误:", e)
            time.sleep(interval)

    def parse_transfer_event(self, log: Dict) -> Dict:
        topics = log["topics"]
        data = log["data"]
        from_addr = "0x" + topics[1][26:] if len(topics) > 1 else ""
        to_addr = "0x" + topics[2][26:] if len(topics) > 2 else ""
        value = int(data, 16) / 1e18
        return {
            "from": from_addr,
            "to": to_addr,
            "value": value,
            "tx_hash": log["transactionHash"],
            "block": int(log["blockNumber"], 16)
        }

if __name__ == "__main__":
    listener = EthereumEventListener("https://ethereum-rpc.publicnode.com", "0x...")
    print("事件监听器就绪")
