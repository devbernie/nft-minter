# mint.py
from src.api.blockchain import BlockchainManager
from src.nft.utils import validate_image_url

class NFTMinter:
    """
    Handles the minting of NFTs.
    """
    def __init__(self, blockchain_manager: BlockchainManager):
        self.blockchain_manager = blockchain_manager

    def mint_nft(self, wallet_address, asset_name, metadata, image_url, amount=1):
        """
        Mint an NFT and assign it to the specified wallet address.
        """
        try:
            # Generate a unique policy ID for this minting operation
            policy_id = self.blockchain_manager.generate_policy_id()

            # Update metadata with the generated policy ID
            metadata["721"][policy_id] = metadata["721"].pop("placeholder_policy_id")

            # Create the minting transaction
            tx_hash = self.blockchain_manager.create_minting_transaction(
                wallet_address,
                asset_name,
                metadata,
                policy_id,
                amount
            )

            return {
                "tx_hash": tx_hash
            }
        except Exception as e:
            raise Exception(f"Failed to mint NFT: {str(e)}")