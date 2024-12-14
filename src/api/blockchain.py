# blockchain.py
import os
from src.api.koios import KoiosAPI
from pycardano import TransactionBuilder, PaymentSigningKey, Transaction, TransactionOutput, Network
from dotenv import load_dotenv

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

    def mint_nft(self, sender_address, signing_key, policy_id, asset_name, metadata, amount=1):
        """
        Mint an NFT using a specific policy ID and metadata.

        :param sender_address: Address of the sender
        :param signing_key: PaymentSigningKey of the sender
        :param policy_id: Policy ID for the NFT
        :param asset_name: Name of the NFT asset
        :param metadata: Metadata for the NFT (dict)
        :param amount: Amount of NFTs to mint (default 1)
        :return: Transaction ID or error message
        """
        try:
            builder = TransactionBuilder(self.network)
            builder.mint_asset(policy_id, asset_name, amount, metadata)
            transaction = builder.build(sender_address)
            signed_transaction = transaction.sign([signing_key])
            result = self.submit_transaction(signed_transaction)
            return result
        except Exception as e:
            return {"error": str(e)}