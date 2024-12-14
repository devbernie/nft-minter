# koios.py
import requests
import os

class KoiosAPI:
    """
    Wrapper class for interacting with the Koios API on Cardano Preview Testnet.
    """

    BASE_URL = os.getenv("API_BASE_URL")

    def __init__(self, api_base_url="https://preview.koios.rest/api/v1"):
        self.api_base_url = api_base_url

    def get_account_assets(self, address):
        url = f"{self.api_base_url}/account_assets"
        payload = {"_addresses": [address]}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def submit_transaction(self, cbor_hex):
        url = f"{self.BASE_URL}/submittx"
        payload = {"_tx": cbor_hex}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}