import argparse
import sys
from typing import Optional
from blockchain_core_v17 import BlockchainCore
from wallet_core_v14 import WalletCore

class BlockchainCLI:
    def __init__(self):
        self.bc = BlockchainCore()
        self.wallet = WalletCore()
        self.parser = self._build_parser()

    def _build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="区块链命令行工具")
        subparsers = parser.add_subparsers(dest="command")

        subparsers.add_parser("info", help="显示链信息")
        subparsers.add_parser("create-wallet", help="创建钱包")
        p_tx = subparsers.add_parser("send-tx", help="发送交易")
        p_tx.add_argument("--from", required=True, help="发送地址")
        p_tx.add_argument("--to", required=True, help="接收地址")
        p_tx.add_argument("--amount", required=True, type=float, help="金额")
        p_mine = subparsers.add_parser("mine", help="挖矿")
        p_mine.add_argument("--miner", required=True, help="矿工地址")
        return parser

    def run(self):
        args = self.parser.parse_args()
        if args.command == "info":
            self._cmd_info()
        elif args.command == "create-wallet":
            self._cmd_create_wallet()
        elif args.command == "send-tx":
            self._cmd_send_tx(getattr(args, "from"), args.to, args.amount)
        elif args.command == "mine":
            self._cmd_mine(args.miner)
        else:
            self.parser.print_help()

    def _cmd_info(self):
        print("=== 区块链信息 ===")
        print(f"区块高度: {len(self.bc.chain) - 1}")
        print(f"待处理交易: {len(self.bc.pending_transactions)}")
        print(f"链有效: {self.bc.validate_chain()}")

    def _cmd_create_wallet(self):
        wallet = self.wallet.create_wallet("123456")
        print("=== 钱包创建成功 ===")
        print(f"地址: {wallet['address']}")
        print(f"助记词: {wallet['mnemonic']}")

    def _cmd_send_tx(self, sender: str, to: str, amount: float):
        idx = self.bc.add_transaction(sender, to, amount)
        print(f"交易已加入交易池，将在区块 {idx} 打包")

    def _cmd_mine(self, miner: str):
        block = self.bc.mine_block(miner)
        print(f"挖矿成功！区块高度: {block['index']}, 哈希: {block['hash'][:16]}...")

if __name__ == "__main__":
    cli = BlockchainCLI()
    cli.run()
