import hashlib
from typing import Dict

class ERC20Token:
    def __init__(self, name: str, symbol: str, total_supply: float, decimals: int = 18):
        self.name = name
        self.symbol = symbol
        self.decimals = decimals
        self.total_supply = total_supply * (10 ** decimals)
        self.balances: Dict[str, int] = {}
        self.allowances: Dict[str, Dict[str, int]] = {}
        self.balances["owner"] = self.total_supply

    def transfer(self, sender: str, recipient: str, amount: int) -> bool:
        if self.balances.get(sender, 0) < amount:
            return False
        self.balances[sender] -= amount
        self.balances[recipient] = self.balances.get(recipient, 0) + amount
        return True

    def approve(self, owner: str, spender: str, amount: int) -> bool:
        if owner not in self.allowances:
            self.allowances[owner] = {}
        self.allowances[owner][spender] = amount
        return True

    def transfer_from(self, spender: str, owner: str, recipient: str, amount: int) -> bool:
        if self.allowances.get(owner, {}).get(spender, 0) < amount:
            return False
        if self.balances.get(owner, 0) < amount:
            return False
        self.allowances[owner][spender] -= amount
        self.balances[owner] -= amount
        self.balances[recipient] = self.balances.get(recipient, 0) + amount
        return True

    def balance_of(self, account: str) -> int:
        return self.balances.get(account, 0)

    def allowance(self, owner: str, spender: str) -> int:
        return self.allowances.get(owner, {}).get(spender, 0)

    def burn(self, owner: str, amount: int) -> bool:
        if self.balances.get(owner, 0) < amount:
            return False
        self.balances[owner] -= amount
        self.total_supply -= amount
        return True

    def mint(self, to: str, amount: int) -> bool:
        self.balances[to] = self.balances.get(to, 0) + amount
        self.total_supply += amount
        return True

if __name__ == "__main__":
    token = ERC20Token("TestToken", "TT", 1000000)
    print("总供应量:", token.total_supply)
