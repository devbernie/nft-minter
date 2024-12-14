# koios.py
import requests
import os


class KoiosAPI:
    """
    Wrapper class for interacting with the Koios API on Cardano Preview Testnet.
    """

    BASE_URL = os.getenv("API_BASE_URL")

    def __init__(self, api_base_url=None):
        self.api_base_url = api_base_url or self.BASE_URL

    def get_account_assets(self, address):
        """
        Fetch the list of assets (NFTs, tokens) held by a given wallet address.

        :param address: Cardano wallet address (string)
        :return: List of assets (dict) or error message.
        """
        # Simulated mock response for testing
        if self.api_base_url == "mock":
            return [{"asset_name": "MockNFT", "quantity": 1}]

        url = f"{self.api_base_url}/account_assets"
        payload = {"_addresses": [address]}

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def submit_transaction(self, cbor_hex):
        """
        Submit a transaction to the blockchain.

        :param cbor_hex: CBOR-encoded transaction in hex format (string)
        :return: Transaction ID or error message.
        """
        # Simulated mock response for testing
        if self.api_base_url == "mock":
            return {"tx_hash": "mock_hash"}

        url = f"{self.api_base_url}/submittx"
        payload = {"_tx": cbor_hex}

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}