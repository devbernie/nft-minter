# blockchain.py
import os
from src.api.koios import KoiosAPI
from pycardano import TransactionBuilder, PaymentSigningKey, Transaction, TransactionOutput, Network
from dotenv import load_dotenv
import uuid
from src.config import Config
import cbor2

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
        try:
            if not sender_address or not receiver_address or amount_lovelace <= 0:
                raise ValueError("Invalid input for building a transaction")

            builder = self.TransactionBuilder(self.network)
            builder.add_output(TransactionOutput(receiver_address, amount_lovelace))
            transaction = builder.build(sender_address)
            return transaction
        except Exception as e:
            raise Exception(f"Error building transaction: {e}")

    def sign_transaction(self, transaction, signing_key):
        """
        Sign a transaction using the sender's signing key.

        :param transaction: Unsigned Transaction object
        :param signing_key: PaymentSigningKey of the sender
        :return: Serialized signed transaction as CBOR hex
        """
        # Use a library method to sign the transaction
        try:
            signed_transaction = transaction.sign(signing_key)  # Replace with library-specific signing logic
            cbor_serialized = signed_transaction.to_cbor_hex()  # Serialize signed transaction to CBOR hex
            return cbor_serialized
        except Exception as e:
            raise Exception(f"Error signing transaction: {e}")

    def submit_transaction(self, signed_transaction):
        """
        Submit a signed transaction to the blockchain.

        :param signed_transaction: Signed Transaction object
        :return: Transaction ID or error message
        """
        response = self.koios_api.submit_transaction(signed_transaction.to_cbor_hex())
        if response.get("error"):
            raise Exception(f"Transaction submission failed: {response['error']}")
        return {"tx_hash": response["tx_hash"]}

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
        if not isinstance(assets, list):
            print(f"Warning: Expected list of assets, got {type(assets)}")
            return []
        
        nfts = []
        for asset in assets:
            if not isinstance(asset, dict):
                print(f"Warning: Invalid asset format: {asset}")
                continue
            
            nft = {
                "name": str(asset.get("asset_name", "Unknown")),
                "policy_id": str(asset.get("policy_id", "Unknown")),
                "asset_name": str(asset.get("asset_name", "Unknown")),
                "quantity": int(asset.get("quantity", 0))
            }
            nfts.append(nft)
        return nfts

    def generate_policy_id(self):
        # This is a placeholder. In a real implementation, you would generate a proper Cardano policy ID
        return str(uuid.uuid4())

    def create_minting_transaction(self, wallet_address, asset_name, metadata, policy_id, amount):
        # This is where you would implement the actual minting logic
        # For now, we'll just return a mock transaction hash
        tx_hash = f"mock_tx_hash_{uuid.uuid4()}"
        
        # In a real implementation, you would:
        # 1. Create a transaction that mints the NFT
        # 2. Assign the minted NFT to the specified wallet_address
        # 3. Submit the transaction to the blockchain
        
        print(f"Minting {amount} NFT(s) '{asset_name}' to address: {wallet_address}")
        print(f"Policy ID: {policy_id}")
        print(f"Transaction hash: {tx_hash}")
        
        return tx_hash