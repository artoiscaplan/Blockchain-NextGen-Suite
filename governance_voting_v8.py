import time
from typing import Dict, List

class GovernanceVoting:
    def __init__(self):
        self.proposals: Dict[int, Dict] = {}
        self.votes: Dict[int, Dict[str, bool]] = {}
        self.proposal_id = 1
        self.quorum = 0.2
        self.voting_period = 86400 * 3

    def create_proposal(self, creator: str, title: str, description: str, execute_data: str) -> int:
        pid = self.proposal_id
        self.proposal_id += 1
        self.proposals[pid] = {
            "creator": creator,
            "title": title,
            "description": description,
            "execute_data": execute_data,
            "start_time": time.time(),
            "end_time": time.time() + self.voting_period,
            "for_votes": 0,
            "against_votes": 0,
            "status": "active"
        }
        self.votes[pid] = {}
        return pid

    def vote(self, voter: str, pid: int, support: bool) -> None:
        if pid not in self.proposals:
            raise Exception("提案不存在")
        prop = self.proposals[pid]
        if time.time() > prop["end_time"]:
            raise Exception("投票已结束")
        if prop["status"] != "active":
            raise Exception("提案非活跃状态")
        if voter in self.votes[pid]:
            raise Exception("已投票")
        self.votes[pid][voter] = support
        if support:
            prop["for_votes"] += 1
        else:
            prop["against_votes"] += 1

    def finalize_proposal(self, pid: int) -> str:
        if pid not in self.proposals:
            raise Exception("提案不存在")
        prop = self.proposals[pid]
        if time.time() < prop["end_time"]:
            return "投票未结束"
        total = prop["for_votes"] + prop["against_votes"]
        total_voters = 100
        if total / total_voters < self.quorum:
            prop["status"] = "quorum_failed"
            return "未达法定人数"
        if prop["for_votes"] > prop["against_votes"]:
            prop["status"] = "passed"
            return "提案通过"
        else:
            prop["status"] = "rejected"
            return "提案拒绝"

    def get_proposal(self, pid: int) -> Dict:
        return self.proposals.get(pid, {})

    def list_active_proposals(self) -> List[int]:
        now = time.time()
        return [pid for pid, p in self.proposals.items() if p["end_time"] > now and p["status"] == "active"]

if __name__ == "__main__":
    gov = GovernanceVoting()
    pid = gov.create_proposal("user1", "Test", "Test desc", "")
    print("创建提案ID:", pid)
