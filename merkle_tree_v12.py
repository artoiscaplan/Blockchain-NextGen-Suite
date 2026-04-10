import hashlib
from typing import List

class MerkleTree:
    def __init__(self, data_list: List[str]):
        self.leaves = [self._hash(data) for data in data_list]
        self.tree = []
        self.build_tree()

    @staticmethod
    def _hash(data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def build_tree(self) -> None:
        if not self.leaves:
            self.root = self._hash("")
            return
        current_level = self.leaves
        self.tree.append(current_level)
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i+1] if (i+1) < len(current_level) else left
                combined = self._hash(left + right)
                next_level.append(combined)
            current_level = next_level
            self.tree.append(current_level)
        self.root = current_level[0]

    def get_root(self) -> str:
        return self.root

    def get_proof(self, index: int) -> List[dict]:
        proof = []
        current_index = index
        for level in self.tree[:-1]:
            sibling_index = current_index ^ 1
            if sibling_index < len(level):
                position = "right" if sibling_index > current_index else "left"
                proof.append({"position": position, "hash": level[sibling_index]})
            current_index = current_index // 2
        return proof

    def verify_proof(self, leaf: str, proof: List[dict], root: str) -> bool:
        current_hash = self._hash(leaf)
        for p in proof:
            if p["position"] == "left":
                current_hash = self._hash(p["hash"] + current_hash)
            else:
                current_hash = self._hash(current_hash + p["hash"])
        return current_hash == root

if __name__ == "__main__":
    data = ["tx1", "tx2", "tx3", "tx4"]
    mt = MerkleTree(data)
    print("默克尔根:", mt.get_root())
