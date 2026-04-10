import socket
import threading
import time
import json
from typing import List, Dict

class PeerDiscovery:
    def __init__(self, node_port: int, broadcast_port: int = 9999):
        self.node_port = node_port
        self.broadcast_port = broadcast_port
        self.peer_list: List[Dict] = []
        self.running = False
        self.node_ip = self._get_local_ip()

    def _get_local_ip(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def start(self) -> None:
        self.running = True
        threading.Thread(target=self._broadcast_announce, daemon=True).start()
        threading.Thread(target=self._listen_broadcast, daemon=True).start()
        threading.Thread(target=self._cleanup_peers, daemon=True).start()

    def _broadcast_announce(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while self.running:
            msg = json.dumps({
                "ip": self.node_ip,
                "port": self.node_port,
                "time": time.time()
            }).encode()
            sock.sendto(msg, ("255.255.255.255", self.broadcast_port))
            time.sleep(2)

    def _listen_broadcast(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", self.broadcast_port))
        while self.running:
            data, addr = sock.recvfrom(1024)
            try:
                msg = json.loads(data.decode())
                if msg["ip"] != self.node_ip:
                    self._add_peer(msg["ip"], msg["port"])
            except:
                continue

    def _add_peer(self, ip: str, port: int) -> None:
        for p in self.peer_list:
            if p["ip"] == ip and p["port"] == port:
                p["last_seen"] = time.time()
                return
        self.peer_list.append({
            "ip": ip,
            "port": port,
            "last_seen": time.time(),
            "score": 100
        })

    def _cleanup_peers(self) -> None:
        while self.running:
            now = time.time()
            self.peer_list = [p for p in self.peer_list if now - p["last_seen"] < 10]
            time.sleep(5)

    def get_peer_list(self) -> List[Dict]:
        return self.peer_list

    def stop(self) -> None:
        self.running = False

if __name__ == "__main__":
    pd = PeerDiscovery(8888)
    pd.start()
    time.sleep(60)
