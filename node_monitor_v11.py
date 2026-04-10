import time
import psutil
import socket
from typing import Dict, List
import threading

class NodeMonitor:
    def __init__(self, node_host: str, node_port: int):
        self.node_host = node_host
        self.node_port = node_port
        self.metrics = []
        self.alerts = []
        self.running = False

    def start_monitor(self, interval: int = 5) -> None:
        self.running = True
        threading.Thread(target=self._monitor_loop, args=(interval,), daemon=True).start()
        print("节点监控已启动")

    def _monitor_loop(self, interval: int) -> None:
        while self.running:
            metric = self._collect_metrics()
            self.metrics.append(metric)
            self._check_alerts(metric)
            time.sleep(interval)

    def _collect_metrics(self) -> Dict:
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        net = psutil.net_io_counters()
        node_status = self._check_node_status()
        return {
            "timestamp": time.time(),
            "cpu_usage": cpu,
            "memory_usage": mem,
            "disk_usage": disk,
            "bytes_sent": net.bytes_sent,
            "bytes_recv": net.bytes_recv,
            "node_online": node_status
        }

    def _check_node_status(self) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.node_host, self.node_port))
            sock.close()
            return result == 0
        except:
            return False

    def _check_alerts(self, metric: Dict) -> None:
        if metric["cpu_usage"] > 90:
            self.alerts.append({"type": "high_cpu", "value": metric["cpu_usage"], "time": metric["timestamp"]})
        if not metric["node_online"]:
            self.alerts.append({"type": "node_offline", "time": metric["timestamp"]})

    def get_latest_metrics(self) -> Dict:
        return self.metrics[-1] if self.metrics else {}

    def get_alerts(self) -> List[Dict]:
        return self.alerts

    def stop_monitor(self) -> None:
        self.running = False

if __name__ == "__main__":
    monitor = NodeMonitor("127.0.0.1", 8888)
    monitor.start_monitor()
    time.sleep(30)
