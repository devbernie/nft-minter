# list.py
from src.api.koios import KoiosAPI

class NFTLister:
    """
    Lists NFTs from a wallet.
    """
    def __init__(self, koios_api: KoiosAPI):
        self.koios_api = koios_api

    def list_nfts(self, wallet_address):
        """
        List all NFTs held by the given wallet address.

        :param wallet_address: Wallet address to query
        :return: List of NFTs or an error message
        """
        return self.koios_api.get_account_assets(wallet_address)