import hashlib
import ecdsa
from typing import Tuple

class ECDSACrypto:
    def __init__(self):
        self.curve = ecdsa.SECP256k1

    def generate_key_pair(self) -> Tuple[str, str]:
        sk = ecdsa.SigningKey.generate(curve=self.curve)
        vk = sk.get_verifying_key()
        private_key = sk.to_string().hex()
        public_key = vk.to_string().hex()
        return private_key, public_key

    def private_to_public(self, private_key: str) -> str:
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=self.curve)
        return sk.get_verifying_key().to_string().hex()

    def get_address(self, public_key: str) -> str:
        pub_bytes = bytes.fromhex(public_key)
        sha256 = hashlib.sha256(pub_bytes).digest()
        ripemd = hashlib.new('ripemd160', sha256).digest()
        return "0x" + ripemd.hex()

    def sign_message(self, private_key: str, message: str) -> str:
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=self.curve)
        msg_hash = hashlib.sha256(message.encode()).digest()
        signature = sk.sign(msg_hash)
        return signature.hex()

    def verify_signature(self, public_key: str, message: str, signature: str) -> bool:
        try:
            vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=self.curve)
            msg_hash = hashlib.sha256(message.encode()).digest()
            return vk.verify(bytes.fromhex(signature), msg_hash)
        except:
            return False

if __name__ == "__main__":
    crypto = ECDSACrypto()
    sk, pk = crypto.generate_key_pair()
    addr = crypto.get_address(pk)
    print("地址:", addr)
