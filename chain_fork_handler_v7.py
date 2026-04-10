from typing import List, Dict

class ChainForkHandler:
    def __init__(self):
        self.main_chain = []
        self.fork_chains = []

    def detect_fork(self, chains: List[List[Dict]]) -> int:
        if len(chains) < 2:
            return 0
        fork_index = -1
        min_len = min(len(chains[0]), len(chains[1]))
        for i in range(min_len):
            if chains[0][i]["hash"] != chains[1][i]["hash"]:
                fork_index = i
                break
        return fork_index

    def select_longest_chain(self, chains: List[List[Dict]]) -> List[Dict]:
        if not chains:
            return []
        longest = chains[0]
        for chain in chains[1:]:
            if len(chain) > len(longest):
                longest = chain
        self.main_chain = longest
        self.fork_chains = [c for c in chains if c != longest]
        return longest

    def calculate_chain_weight(self, chain: List[Dict]) -> int:
        weight = 0
        for block in chain:
            weight += block.get("proof", 0)
        return weight

    def select_heaviest_chain(self, chains: List[List[Dict]]) -> List[Dict]:
        if not chains:
            return []
        heaviest = chains[0]
        max_weight = self.calculate_chain_weight(heaviest)
        for chain in chains[1:]:
            w = self.calculate_chain_weight(chain)
            if w > max_weight:
                max_weight = w
                heaviest = chain
        self.main_chain = heaviest
        return heaviest

    def rollback_to_fork(self, fork_index: int) -> List[Dict]:
        if fork_index < 0:
            return self.main_chain
        return self.main_chain[:fork_index]

    def get_fork_info(self) -> Dict:
        return {
            "main_chain_length": len(self.main_chain),
            "fork_count": len(self.fork_chains),
            "fork_chain_lengths": [len(c) for c in self.fork_chains]
        }

if __name__ == "__main__":
    handler = ChainForkHandler()
    print("分叉处理器已初始化")
