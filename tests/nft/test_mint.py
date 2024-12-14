# test_mint.py
import pytest
from src.nft.mint import NFTMinter
from unittest.mock import patch, MagicMock

@pytest.fixture
def minter():
    blockchain_manager = MagicMock()
    return NFTMinter(blockchain_manager)

@patch("src.nft.utils.requests.head")
def test_mint_nft(mock_head, minter):
    mock_head.return_value.headers = {"Content-Type": "image/jpeg"}
    minter.blockchain_manager.mint_nft.return_value = {"tx_hash": "mock_hash"}
    metadata = {"name": "Test NFT"}
    result = minter.mint_nft(
        "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u", "TestNFT", metadata, "https://i.imgur.com/CZwugry.jpeg", 1
    )
    assert result["tx_hash"] == "mock_hash"