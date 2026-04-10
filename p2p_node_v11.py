import socket
import threading
import json
import time
from typing import List, Dict

class P2PNode:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.peers: List[tuple] = []
        self.running = False
        self.server_socket = None

    def start(self) -> None:
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        threading.Thread(target=self._accept_connections, daemon=True).start()
        print(f"P2P节点启动: {self.host}:{self.port}")

    def _accept_connections(self) -> None:
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                threading.Thread(target=self._handle_peer, args=(conn, addr), daemon=True).start()
            except:
                break

    def _handle_peer(self, conn: socket.socket, addr: tuple) -> None:
        self.peers.append(addr)
        while self.running:
            try:
                data = conn.recv(4096).decode()
                if not data: break
                msg = json.loads(data)
                self._handle_message(msg, addr)
            except:
                break
        self.peers.remove(addr)
        conn.close()

    def _handle_message(self, msg: Dict, peer: tuple) -> None:
        if msg["type"] == "tx":
            print(f"收到交易: {msg['data']}")
        elif msg["type"] == "block":
            print(f"收到区块: {msg['data']}")
        elif msg["type"] == "ping":
            self.send_to_peer(peer, {"type": "pong"})

    def connect_peer(self, host: str, port: int) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            threading.Thread(target=self._handle_peer, args=(sock, (host, port)), daemon=True).start()
            print(f"已连接节点: {host}:{port}")
        except:
            print("连接失败")

    def broadcast(self, msg: Dict) -> None:
        for peer in self.peers:
            self.send_to_peer(peer, msg)

    def send_to_peer(self, peer: tuple, msg: Dict) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(peer)
            sock.send(json.dumps(msg).encode())
            sock.close()
        except:
            pass

    def stop(self) -> None:
        self.running = False
        self.server_socket.close()

if __name__ == "__main__":
    node = P2PNode("127.0.0.1", 8888)
    node.start()
    time.sleep(100)
