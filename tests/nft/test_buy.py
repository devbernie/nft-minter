# test_buy.py
import pytest
from src.nft.buy import NFTBuyer
from unittest.mock import MagicMock

@pytest.fixture
def buyer():
    blockchain_manager = MagicMock()
    return NFTBuyer(blockchain_manager)

def test_buy_nft(buyer):
    buyer.blockchain_manager.build_transaction.return_value = MagicMock()
    buyer.blockchain_manager.sign_transaction.return_value = MagicMock()
    buyer.blockchain_manager.submit_transaction.return_value = {"tx_hash": "mock_hash"}

    result = buyer.buy_nft("addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u", "addr_test1qzmcx2fp747pzmqpsgfmzmlwjgkkcxxajjw4dy3fwhpjztkfq5vxr694la5f87y709k0alm2dtnl7rl04a9nvccunwtseskzvv", MagicMock(), 1000000)
    assert result["tx_hash"] == "mock_hash"