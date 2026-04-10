import time
from typing import Dict, List

class DAOCore:
    def __init__(self, members: list, treasury: float):
        self.members = set(members)
        self.treasury = treasury
        self.proposals: Dict[int, Dict] = {}
        self.proposal_id = 1
        self.min_support = 0.5

    def join_dao(self, member: str) -> None:
        self.members.add(member)

    def leave_dao(self, member: str) -> None:
        if member in self.members:
            self.members.remove(member)

    def create_proposal(self, proposer: str, title: str, amount: float, recipient: str) -> int:
        if proposer not in self.members:
            raise Exception("非DAO成员")
        if amount > self.treasury:
            raise Exception("金库余额不足")
        pid = self.proposal_id
        self.proposal_id += 1
        self.proposals[pid] = {
            "title": title,
            "amount": amount,
            "recipient": recipient,
            "votes_for": 0,
            "votes_against": 0,
            "voters": [],
            "status": "active",
            "create_time": time.time()
        }
        return pid

    def vote_proposal(self, voter: str, pid: int, support: bool) -> None:
        if voter not in self.members:
            raise Exception("无投票权限")
        if pid not in self.proposals:
            raise Exception("提案不存在")
        prop = self.proposals[pid]
        if voter in prop["voters"]:
            raise Exception("已投票")
        prop["voters"].append(voter)
        if support:
            prop["votes_for"] += 1
        else:
            prop["votes_against"] += 1

    def execute_proposal(self, pid: int) -> bool:
        if pid not in self.proposals:
            return False
        prop = self.proposals[pid]
        total = len(self.members)
        if total == 0:
            return False
        support_rate = prop["votes_for"] / total
        if support_rate < self.min_support:
            prop["status"] = "rejected"
            return False
        if self.treasury < prop["amount"]:
            return False
        self.treasury -= prop["amount"]
        prop["status"] = "executed"
        return True

    def get_dao_info(self) -> Dict:
        return {
            "member_count": len(self.members),
            "treasury": self.treasury,
            "active_proposals": len([p for p in self.proposals.values() if p["status"] == "active"])
        }

if __name__ == "__main__":
    dao = DAOCore(["user1", "user2"], 10000)
    print("DAO信息:", dao.get_dao_info())
