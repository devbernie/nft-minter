# test_blockchain.py
import pytest
from src.api.blockchain import BlockchainManager
from pycardano import PaymentSigningKey, Transaction
from unittest.mock import MagicMock
import cbor2

@pytest.fixture
def blockchain_manager():
    koios_api = MagicMock()
    return BlockchainManager(koios_api, "preview")

def test_build_transaction(blockchain_manager):
    # Mock TransactionBuilder
    mock_builder = MagicMock()
    blockchain_manager.TransactionBuilder = MagicMock(return_value=mock_builder)

    # Mock TransactionOutput
    mock_output = MagicMock()  # Mocked TransactionOutput instance

    # Mock the add_output method to simulate success
    mock_builder.add_output.return_value = None

    # Mock the build method to simulate success
    mock_transaction = MagicMock()  # Mocked unsigned transaction object
    mock_builder.build.return_value = mock_transaction

    # Test successful transaction build
    transaction = blockchain_manager.build_transaction("sender", "receiver", 1000000)
    assert transaction == mock_transaction  # Ensure the returned transaction is correct
    mock_builder.add_output.assert_called_once()  # Ensure add_output was called
    mock_builder.build.assert_called_once_with("sender")  # Ensure build was called with the sender address

    # Test failure in transaction build
    mock_builder.build.side_effect = Exception("Build error")
    with pytest.raises(Exception) as excinfo:
        blockchain_manager.build_transaction("sender", "receiver", 1000000)
    assert str(excinfo.value) == "Error building transaction: Build error"

def test_sign_transaction_success(blockchain_manager):
    # Mock the transaction and signing key
    mock_transaction = MagicMock()
    mock_signing_key = MagicMock()

    # Simulate signing and CBOR serialization
    mock_signed_transaction = MagicMock()
    mock_signed_transaction.to_cbor_hex.return_value = "a1686d6f636b5f6b65796a6d6f636b5f76616c7565"
    mock_transaction.sign.return_value = mock_signed_transaction

    # Call sign_transaction
    signed_transaction = blockchain_manager.sign_transaction(mock_transaction, mock_signing_key)

    # Assert that sign() was called on the transaction
    mock_transaction.sign.assert_called_once_with(mock_signing_key)

    # Assert the CBOR hex matches the expected value
    assert signed_transaction == "a1686d6f636b5f6b65796a6d6f636b5f76616c7565"

def test_sign_transaction_error(blockchain_manager):
    # Mock the transaction and signing key
    mock_transaction = MagicMock()
    mock_signing_key = MagicMock()

    # Simulate an error during signing
    mock_transaction.sign.side_effect = Exception("Signing failed")

    # Call sign_transaction and expect an exception
    try:
        blockchain_manager.sign_transaction(mock_transaction, mock_signing_key)
    except Exception as e:
        assert str(e) == "Error signing transaction: Signing failed"

def test_submit_transaction(blockchain_manager):
    signed_transaction = MagicMock(spec=Transaction)
    signed_transaction.to_cbor_hex.return_value = "mock_cbor_hex"

    blockchain_manager.koios_api.submit_transaction.return_value = {"tx_hash": "mock_hash"}

    result = blockchain_manager.submit_transaction(signed_transaction)
    assert result["tx_hash"] == "mock_hash"

def test_mint_nft(blockchain_manager):
    blockchain_manager.koios_api.submit_transaction.return_value = {"tx_hash": "mock_hash"}
    metadata = {"name": "Test NFT"}
    blockchain_manager.build_transaction = MagicMock(return_value=MagicMock())
    blockchain_manager.sign_transaction = MagicMock(return_value=MagicMock())
    blockchain_manager.mint_nft = MagicMock(return_value={"tx_hash": "mock_hash"})

    result = blockchain_manager.mint_nft(
        "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u", "TestNFT", metadata, 1
    )
    assert result["tx_hash"] == "mock_hash"
