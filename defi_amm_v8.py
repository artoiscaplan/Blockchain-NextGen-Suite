from typing import Tuple
import math

class AMMExchange:
    def __init__(self, token_a_reserve: float, token_b_reserve: float, fee: float = 0.003):
        self.reserve_a = token_a_reserve
        self.reserve_b = token_b_reserve
        self.fee_rate = fee
        self.liquidity_providers = {}
        self.total_lp = 0

    def get_price(self) -> float:
        return self.reserve_b / self.reserve_a

    def add_liquidity(self, user: str, a_amount: float, b_amount: float) -> float:
        if self.reserve_a == 0 and self.reserve_b == 0:
            lp_tokens = math.sqrt(a_amount * b_amount)
        else:
            lp_tokens = min(a_amount * self.total_lp / self.reserve_a, b_amount * self.total_lp / self.reserve_b)
        self.reserve_a += a_amount
        self.reserve_b += b_amount
        self.total_lp += lp_tokens
        self.liquidity_providers[user] = self.liquidity_providers.get(user, 0) + lp_tokens
        return lp_tokens

    def remove_liquidity(self, user: str, lp_amount: float) -> Tuple[float, float]:
        if self.liquidity_providers.get(user, 0) < lp_amount:
            raise Exception("LP代币不足")
        share = lp_amount / self.total_lp
        a_out = share * self.reserve_a
        b_out = share * self.reserve_b
        self.reserve_a -= a_out
        self.reserve_b -= b_out
        self.total_lp -= lp_amount
        self.liquidity_providers[user] -= lp_amount
        return a_out, b_out

    def swap_a_to_b(self, a_in: float) -> float:
        a_in_with_fee = a_in * (1 - self.fee_rate)
        b_out = (a_in_with_fee * self.reserve_b) / (self.reserve_a + a_in_with_fee)
        self.reserve_a += a_in
        self.reserve_b -= b_out
        return b_out

    def swap_b_to_a(self, b_in: float) -> float:
        b_in_with_fee = b_in * (1 - self.fee_rate)
        a_out = (b_in_with_fee * self.reserve_a) / (self.reserve_b + b_in_with_fee)
        self.reserve_b += b_in
        self.reserve_a -= a_out
        return a_out

    def get_reserves(self) -> Tuple[float, float]:
        return self.reserve_a, self.reserve_b

if __name__ == "__main__":
    amm = AMMExchange(1000, 1000)
    print("初始价格:", amm.get_price())
