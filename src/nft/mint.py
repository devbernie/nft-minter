# mint.py
from src.api.blockchain import BlockchainManager
from src.nft.utils import validate_image_url

class NFTMinter:
    """
    Handles the minting of NFTs.
    """
    def __init__(self, blockchain_manager: BlockchainManager):
        self.blockchain_manager = blockchain_manager

    def mint_nft(self, sender_address, signing_key, policy_id, asset_name, metadata, image_url=None, amount=1):
        """
        Mint an NFT.

        :param sender_address: Address of the sender
        :param signing_key: PaymentSigningKey of the sender
        :param policy_id: Policy ID
        :param asset_name: Name of the NFT asset
        :param metadata: Metadata for the NFT
        :param image_url: URL of the image for the NFT (optional)
        :param amount: Quantity to mint
        :return: Result from the blockchain
        """
        if image_url:
            validate_image_url(image_url)
            metadata["image"] = image_url

        return self.blockchain_manager.mint_nft(
            sender_address, signing_key, policy_id, asset_name, metadata, amount
        )