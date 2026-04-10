import random
import time
from typing import Dict, List

class PoSConsensus:
    def __init__(self):
        self.validators: Dict[str, float] = {}
        self.min_stake = 100.0
        self.current_validator = None
        self.block_interval = 3

    def stake(self, address: str, amount: float) -> None:
        if amount < self.min_stake:
            raise Exception("质押金额低于最低要求")
        if address in self.validators:
            self.validators[address] += amount
        else:
            self.validators[address] = amount

    def unstake(self, address: str, amount: float) -> None:
        if address not in self.validators:
            raise Exception("地址无质押资产")
        if self.validators[address] < amount:
            raise Exception("解押金额超过质押总额")
        self.validators[address] -= amount
        if self.validators[address] == 0:
            del self.validators[address]

    def select_validator(self) -> str:
        if not self.validators:
            raise Exception("无可用验证节点")
        total_stake = sum(self.validators.values())
        selector = random.uniform(0, total_stake)
        current = 0
        for addr, stake in self.validators.items():
            current += stake
            if current >= selector:
                self.current_validator = addr
                return addr

    def create_block(self, validator: str, txs: List[Dict]) -> Dict:
        if validator != self.current_validator:
            raise Exception("非当前出块节点")
        block = {
            "validator": validator,
            "timestamp": time.time(),
            "transactions": txs,
            "stake_weight": self.validators[validator],
            "signature": f"SIG_{random.getrandbits(128)}"
        }
        time.sleep(self.block_interval)
        return block

    def slash(self, address: str) -> None:
        if address in self.validators:
            penalty = self.validators[address] * 0.5
            self.validators[address] -= penalty

    def get_validator_list(self) -> Dict:
        return self.validators

if __name__ == "__main__":
    pos = PoSConsensus()
    pos.stake("node1", 200)
    pos.stake("node2", 300)
    print("选中验证节点:", pos.select_validator())
