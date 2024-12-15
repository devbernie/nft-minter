# test_mint.py
import pytest
from src.nft.mint import NFTMinter
from unittest.mock import patch, MagicMock

@pytest.fixture
def minter():
    blockchain_manager = MagicMock()
    return NFTMinter(blockchain_manager)

def test_mint_nft():
    mock_blockchain_manager = MagicMock()
    mock_blockchain_manager.generate_policy_id.return_value = "test_policy_id"
    mock_blockchain_manager.create_minting_transaction.return_value = "test_tx_hash"

    minter = NFTMinter(mock_blockchain_manager)

    wallet_address = "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u"
    asset_name = "TestNFT"
    metadata = {
        "721": {
            "placeholder_policy_id": {
                "TestNFT": {
                    "name": "Test NFT",
                    "image": "https://i.imgur.com/CZwugry.jpeg",
                    "mediaType": "image/jpeg",
                    "files": [
                        {
                            "name": "Test NFT",
                            "src": "https://i.imgur.com/CZwugry.jpeg",
                            "mediaType": "image/jpeg"
                        }
                    ]
                }
            }
        }
    }
    image_url = "https://i.imgur.com/CZwugry.jpeg"
    amount = 1

    result = minter.mint_nft(wallet_address, asset_name, metadata, image_url, amount)

    assert result == {"tx_hash": "test_tx_hash"}
    mock_blockchain_manager.generate_policy_id.assert_called_once()
    mock_blockchain_manager.create_minting_transaction.assert_called_once_with(
        wallet_address, asset_name, metadata, "test_policy_id", amount
    )