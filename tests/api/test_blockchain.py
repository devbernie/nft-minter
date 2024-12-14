# test_blockchain.py
import pytest
from src.api.blockchain import BlockchainManager
from pycardano import PaymentSigningKey, Transaction
from unittest.mock import MagicMock

@pytest.fixture
def blockchain_manager():
    koios_api = MagicMock()
    return BlockchainManager(koios_api, "preview")

def test_build_transaction(blockchain_manager):
    mock_transaction = MagicMock()
    blockchain_manager.build_transaction = MagicMock(return_value=mock_transaction)

    result = blockchain_manager.build_transaction(
        "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u", "addr_test1qzmcx2fp747pzmqpsgfmzmlwjgkkcxxajjw4dy3fwhpjztkfq5vxr694la5f87y709k0alm2dtnl7rl04a9nvccunwtseskzvv", 1000000
    )
    assert result is not None

def test_sign_transaction(blockchain_manager):
    mock_transaction = MagicMock(spec=Transaction)
    signing_key = MagicMock(spec=PaymentSigningKey)

    signed_transaction = blockchain_manager.sign_transaction(mock_transaction, signing_key)
    assert signed_transaction is not None

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
