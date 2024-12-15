# mint.py
from src.api.blockchain import BlockchainManager
from src.nft.utils import validate_image_url

class NFTMinter:
    """
    Handles the minting of NFTs.
    """
    def __init__(self, blockchain_manager: BlockchainManager):
        self.blockchain_manager = blockchain_manager

    def mint_nft(self, wallet_address, asset_name, metadata, image_url, amount):
        # Generate a unique policy ID for this minting operation
        policy_id = self.blockchain_manager.generate_policy_id()

        # Update the metadata with the generated policy ID
        if "721" in metadata and "placeholder_policy_id" in metadata["721"]:
            metadata["721"][policy_id] = metadata["721"].pop("placeholder_policy_id")

        # Create the minting transaction
        tx_hash = self.blockchain_manager.create_minting_transaction(
            wallet_address,
            asset_name,
            metadata,
            policy_id,
            amount
        )

        return {"tx_hash": tx_hash}