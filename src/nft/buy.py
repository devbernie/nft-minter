# buy.py
from src.api.blockchain import BlockchainManager

class NFTBuyer:
    """
    Handles the purchasing of NFTs.
    """
    def __init__(self, blockchain_manager: BlockchainManager):
        self.blockchain_manager = blockchain_manager

    def buy_nft(self, sender_address, receiver_address, signing_key, amount_lovelace):
        # Build transaction
        transaction = self.blockchain_manager.build_transaction(sender_address, receiver_address, amount_lovelace)

        # Sign transaction
        signed_transaction = self.blockchain_manager.sign_transaction(transaction, signing_key)

        # Serialize (ensure object has to_cbor_hex or use a library for CBOR serialization)
        if hasattr(signed_transaction, "to_cbor_hex"):
            serialized_transaction = signed_transaction.to_cbor_hex()
        else:
            import cbor2
            serialized_transaction = cbor2.dumps(signed_transaction).hex()

        # Submit transaction
        return self.blockchain_manager.submit_transaction(serialized_transaction)
