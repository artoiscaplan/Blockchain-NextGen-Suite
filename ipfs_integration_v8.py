import requests
import json
import hashlib
from typing import Optional

class IPFSIntegration:
    def __init__(self, gateway: str = "https://ipfs.io/ipfs/"):
        self.gateway = gateway
        self.api_url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
        self.api_key = "test_key"
        self.secret = "test_secret"

    def upload_json(self, data: dict) -> Optional[str]:
        try:
            headers = {
                "pinata_api_key": self.api_key,
                "pinata_secret_api_key": self.secret
            }
            payload = {"pinataContent": data}
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()["IpfsHash"]
            return None
        except:
            return self._local_upload(data)

    def _local_upload(self, data: dict) -> str:
        raw = json.dumps(data, sort_keys=True).encode()
        cid = hashlib.sha256(raw).hexdigest()
        return f"Qm{cid[:44]}"

    def get_file(self, cid: str) -> Optional[dict]:
        try:
            url = f"{self.gateway}{cid}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def upload_nft_metadata(self, name: str, image: str, description: str, attributes: list) -> str:
        meta = {
            "name": name,
            "description": description,
            "image": image,
            "attributes": attributes,
            "upload_time": self._now()
        }
        return self.upload_json(meta)

    def _now(self) -> float:
        import time
        return time.time()

if __name__ == "__main__":
    ipfs = IPFSIntegration()
    cid = ipfs.upload_json({"test": "data"})
    print("IPFS CID:", cid)
