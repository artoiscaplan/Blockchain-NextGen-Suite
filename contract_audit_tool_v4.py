import re
from typing import List, Dict

class ContractAuditTool:
    def __init__(self):
        self.vulnerabilities = []

    def scan_reentrancy(self, code: str) -> bool:
        if re.search(r'call\.value.*external', code) and not re.search(r'reentrancy|mutex|lock', code):
            self.vulnerabilities.append({"type": "重入风险", "level": "高危"})
            return True
        return False

    def scan_overflow(self, code: str) -> bool:
        if re.search(r'uint.*[+-/*].*uint', code) and not re.search(r'SafeMath|overflow', code):
            self.vulnerabilities.append({"type": "整数溢出", "level": "高危"})
            return True
        return False

    def scan_unprotected(self, code: str) -> bool:
        if re.search(r'function.*transfer|withdraw', code) and not re.search(r'onlyOwner|modifier|require', code):
            self.vulnerabilities.append({"type": "未授权访问", "level": "高危"})
            return True
        return False

    def scan_timestamp(self, code: str) -> bool:
        if re.search(r'block\.timestamp.*random|luck', code):
            self.vulnerabilities.append({"type": "时间戳操纵", "level": "中危"})
            return True
        return False

    def full_audit(self, code: str) -> List[Dict]:
        self.vulnerabilities.clear()
        self.scan_reentrancy(code)
        self.scan_overflow(code)
        self.scan_unprotected(code)
        self.scan_timestamp(code)
        return self.vulnerabilities

    def get_security_score(self) -> int:
        score = 100
        for vul in self.vulnerabilities:
            if vul["level"] == "高危":
                score -= 30
            else:
                score -= 15
        return max(score, 0)

if __name__ == "__main__":
    audit = ContractAuditTool()
    code = "function withdraw() external { msg.sender.call.value(100); }"
    print("漏洞报告:", audit.full_audit(code))
