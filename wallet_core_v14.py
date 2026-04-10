import hashlib
import json
import os
from typing import Optional, Dict
from mnemonic import Mnemonic

class WalletCore:
    def __init__(self):
        self.mnemo = Mnemonic("english")
        self.wallets: Dict[str, Dict] = {}
        self.storage_path = "wallets.json"
        self.load_wallets()

    def create_wallet(self, password: str) -> Dict:
        mnemonic = self.mnemo.generate(strength=128)
        seed = self.mnemo.to_seed(mnemonic, password)
        private_key = hashlib.sha256(seed).hexdigest()
        public_key = self._private_to_public(private_key)
        address = self._public_to_address(public_key)
        wallet = {
            "address": address,
            "mnemonic": mnemonic,
            "public_key": public_key,
            "encrypted_private": self._encrypt(private_key, password)
        }
        self.wallets[address] = wallet
        self.save_wallets()
        return wallet

    def restore_wallet(self, mnemonic: str, password: str) -> Dict:
        if not self.mnemo.check(mnemonic):
            raise Exception("助记词无效")
        seed = self.mnemo.to_seed(mnemonic, password)
        private_key = hashlib.sha256(seed).hexdigest()
        public_key = self._private_to_public(private_key)
        address = self._public_to_address(public_key)
        wallet = {
            "address": address,
            "mnemonic": mnemonic,
            "public_key": public_key,
            "encrypted_private": self._encrypt(private_key, password)
        }
        self.wallets[address] = wallet
        self.save_wallets()
        return wallet

    def sign_transaction(self, address: str, password: str, tx_data: str) -> str:
        wallet = self.wallets.get(address)
        if not wallet:
            raise Exception("钱包不存在")
        private_key = self._decrypt(wallet["encrypted_private"], password)
        return hashlib.sha256((private_key + tx_data).encode()).hexdigest()

    def _private_to_public(self, sk: str) -> str:
        return hashlib.sha512(sk.encode()).hexdigest()

    def _public_to_address(self, pk: str) -> str:
        return "0x" + hashlib.new('ripemd160', pk.encode()).hexdigest()

    def _encrypt(self, data: str, pwd: str) -> str:
        key = hashlib.sha256(pwd.encode()).digest().hex()
        return ''.join(chr(ord(a)^ord(b)) for a,b in zip(data, key))

    def _decrypt(self, enc: str, pwd: str) -> str:
        return self._encrypt(enc, pwd)

    def save_wallets(self) -> None:
        with open(self.storage_path, 'w') as f:
            json.dump(self.wallets, f)

    def load_wallets(self) -> None:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                self.wallets = json.load(f)

if __name__ == "__main__":
    w = WalletCore()
    wallet = w.create_wallet("123456")
    print("钱包地址:", wallet["address"])
