# blockchain.py
import os
from src.api.koios import KoiosAPI
from pycardano import TransactionBuilder, PaymentSigningKey, Transaction, TransactionOutput, Network
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

class BlockchainManager:
    """
    Handles higher-level blockchain operations such as creating, signing, and submitting transactions.
    """

    def __init__(self, koios_api: KoiosAPI, network: Network):
        self.koios_api = koios_api
        self.network = network

    def build_transaction(self, sender_address, receiver_address, amount_lovelace):
        """
        Build a transaction to send ADA or other assets.

        :param sender_address: Address of the sender
        :param receiver_address: Address of the receiver
        :param amount_lovelace: Amount of ADA to send (in lovelace)
        :return: Unsigned Transaction object
        """
        try:
            builder = TransactionBuilder(self.network)
            builder.add_output(TransactionOutput(receiver_address, amount_lovelace))
            transaction = builder.build(sender_address)
            return transaction
        except Exception as e:
            return {"error": str(e)}

    def sign_transaction(self, transaction: Transaction, signing_key: PaymentSigningKey):
        """
        Sign a transaction using the sender's signing key.

        :param transaction: Unsigned Transaction object
        :param signing_key: PaymentSigningKey of the sender
        :return: Signed Transaction object
        """
        try:
            signed_transaction = transaction.sign([signing_key])
            return signed_transaction
        except Exception as e:
            return {"error": str(e)}

    def submit_transaction(self, signed_transaction: Transaction):
        """
        Submit a signed transaction to the blockchain.

        :param signed_transaction: Signed Transaction object
        :return: Transaction ID or error message
        """
        try:
            cbor_hex = signed_transaction.to_cbor_hex()
            result = self.koios_api.submit_transaction(cbor_hex)
            return result
        except Exception as e:
            return {"error": str(e)}

    def mint_nft(self, sender_address, asset_name, metadata, amount=1):
        """
        Mint an NFT using a specific policy ID and metadata.

        :param sender_address: Address of the sender
        :param asset_name: Name of the NFT asset
        :param metadata: Metadata for the NFT (dict)
        :param amount: Amount of NFTs to mint (default 1)
        :return: Transaction ID or error message
        """
        try:
            builder = TransactionBuilder(self.network)
            builder.mint = {asset_name: amount}  # Định nghĩa lượng mint
            builder.metadata = metadata  # Gắn metadata

            transaction = builder.build(sender_address)
            signed_transaction = transaction.sign([])  # Không cần signing key
            result = self.submit_transaction(signed_transaction)
            return result
        except Exception as e:
            return {"error": str(e)}

    def list_nfts(self, assets):
        """
        List NFTs based on the assets provided by KoiosAPI
        """
        nfts = []
        for asset in assets:
            # Fetch additional details for each asset if needed
            # For now, we'll just use the information from the assets list
            nft = {
                "name": asset.get("asset_name", "Unknown"),
                "policy_id": asset.get("policy_id", "Unknown"),
                "asset_name": asset.get("asset_name", "Unknown"),
                "quantity": asset.get("quantity", 0)
            }
            nfts.append(nft)
        return nfts

    def generate_policy_id(self):
        # This is a placeholder. In a real implementation, you would generate a proper Cardano policy ID
        return str(uuid.uuid4())

    def create_minting_transaction(self, wallet_address, asset_name, metadata, policy_id, amount):
        # This is where you would implement the actual minting logic
        # For now, we'll just return a mock transaction hash
        return f"mock_tx_hash_{uuid.uuid4()}"