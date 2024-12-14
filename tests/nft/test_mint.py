# test_mint.py
import pytest
from src.nft.mint import NFTMinter
from unittest.mock import MagicMock

@pytest.fixture
def minter():
    blockchain_manager = MagicMock()
    return NFTMinter(blockchain_manager)

def test_mint_nft(minter):
    minter.blockchain_manager.mint_nft.return_value = {"tx_hash": "mock_hash"}

    result = minter.mint_nft(
        "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u", MagicMock(), "policy_id", "TestNFT",
        {"name": "Test NFT"}, "https://i.imgur.com/CZwugry.jpeg", 1
    )
    assert result["tx_hash"] == "mock_hash"