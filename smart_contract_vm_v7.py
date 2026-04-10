from typing import Dict, Any, Optional
import hashlib
import json

class SmartContractVM:
    def __init__(self):
        self.contracts: Dict[str, Dict] = {}
        self.storage: Dict[str, Dict] = {}
        self.gas_limit = 1000000

    def deploy_contract(self, owner: str, code: str, name: str) -> str:
        contract_addr = "0x" + hashlib.sha256((owner + code + str(len(self.contracts))).encode()).hexdigest()[:40]
        self.contracts[contract_addr] = {
            "owner": owner,
            "name": name,
            "code": code,
            "deploy_time": self._now()
        }
        self.storage[contract_addr] = {}
        return contract_addr

    def execute_contract(self, caller: str, contract_addr: str, method: str, params: Dict, gas: int) -> Dict:
        if gas > self.gas_limit:
            raise Exception("Gas超出限制")
        if contract_addr not in self.contracts:
            raise Exception("合约不存在")
        contract = self.contracts[contract_addr]
        store = self.storage[contract_addr]
        result = self._run_method(contract["code"], method, params, caller, store)
        return {
            "success": True,
            "gas_used": gas // 2,
            "result": result,
            "contract": contract_addr
        }

    def _run_method(self, code: str, method: str, params: Dict, caller: str, store: Dict) -> Any:
        if method == "set":
            key = params.get("key")
            value = params.get("value")
            store[key] = value
            return "OK"
        elif method == "get":
            return store.get(params.get("key"))
        elif method == "owner":
            return self.contracts[self._current_contract()]["owner"]
        return "unknown method"

    def get_contract(self, addr: str) -> Optional[Dict]:
        return self.contracts.get(addr)

    def get_storage(self, addr: str) -> Dict:
        return self.storage.get(addr, {})

    def _now(self) -> float:
        import time
        return time.time()

    def _current_contract(self) -> str:
        import inspect
        return inspect.stack()[2][0].f_locals["contract_addr"]

if __name__ == "__main__":
    vm = SmartContractVM()
    addr = vm.deploy_contract("user1", "simple storage", "Storage")
    print("合约地址:", addr)
