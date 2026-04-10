import json
import sqlite3
from typing import List, Dict, Optional
from datetime import datetime

class BlockIndexer:
    def __init__(self, db_path: str = "block_index.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self) -> None:
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS blocks
                     (idx INTEGER PRIMARY KEY, hash TEXT, prev_hash TEXT, timestamp REAL, merkle_root TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (tx_hash TEXT PRIMARY KEY, block_idx INTEGER, sender TEXT, recipient TEXT, amount REAL, data TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS address_txs
                     (address TEXT, tx_hash TEXT, type TEXT)''')
        self.conn.commit()

    def index_block(self, block: Dict) -> None:
        c = self.conn.cursor()
        c.execute('INSERT OR REPLACE INTO blocks VALUES (?,?,?,?,?)',
                  (block["index"], block["hash"], block["previous_hash"], block["timestamp"], block["merkle_root"]))
        for tx in block["transactions"]:
            tx_hash = tx.get("hash", self._hash_tx(tx))
            c.execute('INSERT OR REPLACE INTO transactions VALUES (?,?,?,?,?,?)',
                      (tx_hash, block["index"], tx["sender"], tx["recipient"], tx["amount"], tx.get("data", "")))
            c.execute('INSERT OR REPLACE INTO address_txs VALUES (?,?,?)',
                      (tx["sender"], tx_hash, "send"))
            c.execute('INSERT OR REPLACE INTO address_txs VALUES (?,?,?)',
                      (tx["recipient"], tx_hash, "receive"))
        self.conn.commit()

    def get_block_by_index(self, idx: int) -> Optional[Dict]:
        c = self.conn.cursor()
        c.execute('SELECT * FROM blocks WHERE idx=?', (idx,))
        return c.fetchone()

    def get_tx_by_hash(self, tx_hash: str) -> Optional[Dict]:
        c = self.conn.cursor()
        c.execute('SELECT * FROM transactions WHERE tx_hash=?', (tx_hash,))
        return c.fetchone()

    def get_txs_by_address(self, addr: str) -> List[Dict]:
        c = self.conn.cursor()
        c.execute('SELECT tx_hash FROM address_txs WHERE address=?', (addr,))
        return [{"tx_hash": x[0]} for x in c.fetchall()]

    def _hash_tx(self, tx: Dict) -> str:
        return hashlib.sha256(json.dumps(tx, sort_keys=True).encode()).hexdigest()

if __name__ == "__main__":
    indexer = BlockIndexer()
    print("索引器已启动")
