import time
from typing import Dict

class LiquidityMining:
    def __init__(self, reward_token: str, reward_per_second: float):
        self.reward_token = reward_token
        self.reward_per_second = reward_per_second
        self.stakers: Dict[str, Dict] = {}
        self.total_staked = 0.0

    def stake_lp(self, user: str, lp_amount: float) -> None:
        if lp_amount <= 0:
            raise Exception("数量必须大于0")
        now = time.time()
        if user in self.stakers:
            self._update_reward(user)
            self.stakers[user]["lp_amount"] += lp_amount
        else:
            self.stakers[user] = {
                "lp_amount": lp_amount,
                "reward_debt": 0.0,
                "last_update": now
            }
        self.total_staked += lp_amount

    def _update_reward(self, user: str) -> None:
        data = self.stakers[user]
        now = time.time()
        duration = now - data["last_update"]
        reward = (data["lp_amount"] / self.total_staked) * self.reward_per_second * duration
        data["reward_debt"] += reward
        data["last_update"] = now

    def claim_reward(self, user: str) -> float:
        if user not in self.stakers:
            return 0.0
        self._update_reward(user)
        reward = self.stakers[user]["reward_debt"]
        self.stakers[user]["reward_debt"] = 0.0
        return reward

    def unstake_lp(self, user: str, lp_amount: float) -> None:
        if user not in self.stakers:
            raise Exception("无质押")
        data = self.stakers[user]
        if data["lp_amount"] < lp_amount:
            raise Exception("LP不足")
        self._update_reward(user)
        data["lp_amount"] -= lp_amount
        self.total_staked -= lp_amount
        if data["lp_amount"] == 0:
            del self.stakers[user]

    def get_user_info(self, user: str) -> Dict:
        if user not in self.stakers:
            return {"lp": 0, "pending_reward": 0}
        self._update_reward(user)
        data = self.stakers[user]
        return {"lp": data["lp_amount"], "pending_reward": data["reward_debt"]}

if __name__ == "__main__":
    lm = LiquidityMining("TOKEN", 0.01)
    print("挖矿合约已启动")
