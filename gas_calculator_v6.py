class GasCalculator:
    def __init__(self, base_fee: float = 1e-9, priority_fee: float = 1e-10):
        self.base_fee = base_fee
        self.priority_fee = priority_fee
        self.tx_gas = 21000
        self.contract_gas = 100000

    def calculate_transfer_gas(self) -> int:
        return self.tx_gas

    def calculate_contract_deploy_gas(self, code_size: int) -> int:
        base = self.contract_gas
        size_gas = code_size * 200
        return base + size_gas

    def calculate_contract_call_gas(self, op_count: int, storage_write: int = 0) -> int:
        op_gas = op_count * 10
        store_gas = storage_write * 5000
        return self.tx_gas + op_gas + store_gas

    def calculate_total_fee(self, gas_used: int) -> float:
        return gas_used * (self.base_fee + self.priority_fee)

    def estimate_max_fee(self, gas_limit: int) -> float:
        return gas_limit * (self.base_fee * 2 + self.priority_fee)

    def optimize_gas(self, gas_used: int) -> int:
        if gas_used < self.tx_gas:
            return self.tx_gas
        if gas_used > 300000:
            return 300000
        return gas_used

    def get_gas_prices(self) -> dict:
        return {
            "base_fee": self.base_fee,
            "priority_fee": self.priority_fee,
            "transfer_gas": self.tx_gas,
            "min_fee": self.calculate_total_fee(self.tx_gas)
        }

if __name__ == "__main__":
    gas = GasCalculator()
    print("转账费用:", gas.calculate_total_fee(gas.calculate_transfer_gas()))
