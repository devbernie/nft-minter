# buy.py
from src.api.blockchain import BlockchainManager

class NFTBuyer:
    """
    Handles the purchasing of NFTs.
    """
    def __init__(self, blockchain_manager: BlockchainManager):
        self.blockchain_manager = blockchain_manager

    def buy_nft(self, sender_address, receiver_address, signing_key, amount_lovelace):
        """
        Buy an NFT by sending ADA.

        :param sender_address: Address of the buyer
        :param receiver_address: Address of the seller
        :param signing_key: Signing key of the buyer
        :param amount_lovelace: Amount of ADA to send
        :return: Transaction result
        """
        # Build transaction
        transaction = self.blockchain_manager.build_transaction(
            sender_address, receiver_address, amount_lovelace
        )

        # Sign and submit transaction
        signed_transaction = self.blockchain_manager.sign_transaction(transaction, signing_key)
        return self.blockchain_manager.submit_transaction(signed_transaction)