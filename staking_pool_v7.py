import time
from typing import Dict, List

class StakingPool:
    def __init__(self, reward_rate: float = 0.1):
        self.stakers: Dict[str, Dict] = {}
        self.total_staked = 0.0
        self.reward_rate = reward_rate
        self.lock_period = 86400 * 7

    def stake(self, user: str, amount: float) -> None:
        if amount <= 0:
            raise Exception("质押金额必须大于0")
        now = time.time()
        if user in self.stakers:
            self.stakers[user]["amount"] += amount
            self.stakers[user]["update_time"] = now
        else:
            self.stakers[user] = {
                "amount": amount,
                "start_time": now,
                "update_time": now,
                "claimed_rewards": 0.0
            }
        self.total_staked += amount

    def calculate_reward(self, user: str) -> float:
        if user not in self.stakers:
            return 0.0
        data = self.stakers[user]
        duration = time.time() - data["update_time"]
        reward = data["amount"] * self.reward_rate * (duration / 86400)
        return reward

    def claim_reward(self, user: str) -> float:
        reward = self.calculate_reward(user)
        if reward <= 0:
            return 0.0
        self.stakers[user]["claimed_rewards"] += reward
        self.stakers[user]["update_time"] = time.time()
        return reward

    def unstake(self, user: str, amount: float) -> None:
        if user not in self.stakers:
            raise Exception("无质押资产")
        data = self.stakers[user]
        if time.time() - data["start_time"] < self.lock_period:
            raise Exception("仍在锁仓期")
        if data["amount"] < amount:
            raise Exception("解押金额不足")
        data["amount"] -= amount
        self.total_staked -= amount
        if data["amount"] == 0:
            del self.stakers[user]

    def get_pool_info(self) -> Dict:
        return {
            "total_staked": self.total_staked,
            "staker_count": len(self.stakers),
            "reward_rate": self.reward_rate,
            "lock_period_seconds": self.lock_period
        }

if __name__ == "__main__":
    pool = StakingPool()
    pool.stake("user1", 1000)
    print("质押池信息:", pool.get_pool_info())
