class BlockReward:
    def __init__(self, initial_reward: float = 10.0, halving_interval: int = 210000):
        self.initial_reward = initial_reward
        self.halving_interval = halving_interval
        self.treasury_ratio = 0.1
        self.burn_ratio = 0.05

    def calculate_base_reward(self, block_height: int) -> float:
        halvings = block_height // self.halving_interval
        return self.initial_reward / (2 ** halvings)

    def distribute_reward(self, block_height: int, miner: str, validators: list) -> dict:
        base = self.calculate_base_reward(block_height)
        treasury = base * self.treasury_ratio
        burn = base * self.burn_ratio
        remaining = base - treasury - burn
        validator_reward = remaining * 0.3
        miner_reward = remaining * 0.7
        per_validator = validator_reward / len(validators) if validators else 0
        return {
            "miner": miner,
            "miner_reward": miner_reward,
            "validators": {v: per_validator for v in validators},
            "treasury": treasury,
            "burned": burn,
            "total": base
        }

    def get_total_supply(self, max_height: int) -> float:
        supply = 0.0
        height = 0
        while height < max_height:
            reward = self.calculate_base_reward(height)
            supply += reward
            height += 1
            if reward == 0:
                break
        return supply

    def halving_count(self, block_height: int) -> int:
        return block_height // self.halving_interval

if __name__ == "__main__":
    br = BlockReward()
    print("区块1奖励:", br.calculate_base_reward(1))
