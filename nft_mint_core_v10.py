import hashlib
import time
from typing import Dict, List, Optional

class NFTMintCore:
    def __init__(self):
        self.nfts: Dict[int, Dict] = {}
        self.owners: Dict[int, str] = {}
        self.approvals: Dict[int, str] = {}
        self.token_counter = 1
        self.royalty_fee = 0.05

    def mint_nft(self, to: str, metadata: Dict) -> int:
        token_id = self.token_counter
        self.token_counter += 1
        nft_data = {
            "token_id": token_id,
            "metadata": metadata,
            "mint_time": time.time(),
            "royalty": self.royalty_fee,
            "creator": to
        }
        self.nfts[token_id] = nft_data
        self.owners[token_id] = to
        return token_id

    def transfer_nft(self, from_addr: str, to: str, token_id: int) -> None:
        if self.owners.get(token_id) != from_addr:
            raise Exception("非NFT所有者")
        if to == from_addr:
            raise Exception("不能转移给自己")
        self.owners[token_id] = to
        if token_id in self.approvals:
            del self.approvals[token_id]

    def approve(self, approved: str, token_id: int) -> None:
        if self.owners.get(token_id) != approved:
            self.approvals[token_id] = approved

    def get_owner(self, token_id: int) -> Optional[str]:
        return self.owners.get(token_id)

    def get_nft_info(self, token_id: int) -> Optional[Dict]:
        return self.nfts.get(token_id)

    def burn_nft(self, owner: str, token_id: int) -> None:
        if self.owners.get(token_id) != owner:
            raise Exception("无权限销毁")
        del self.nfts[token_id]
        del self.owners[token_id]
        if token_id in self.approvals:
            del self.approvals[token_id]

    def calculate_royalty(self, price: float) -> float:
        return price * self.royalty_fee

if __name__ == "__main__":
    nft = NFTMintCore()
    meta = {"name": "TestNFT", "image": "ipfs://xxx", "desc": "test"}
    tid = nft.mint_nft("user1", meta)
    print("铸造NFT ID:", tid)
