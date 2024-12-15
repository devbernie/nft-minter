# test_list.py
import pytest
from src.nft.list import NFTLister
from unittest.mock import MagicMock

@pytest.fixture
def lister():
    koios_api = MagicMock()
    return NFTLister(koios_api)

def test_list_nfts(lister):
    lister.koios_api.get_address_assets.return_value = [
        {"asset_name": "TestNFT", "quantity": 1}
    ]

    result = lister.list_nfts("addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u")
    assert len(result) == 1
    assert result[0]["asset_name"] == "TestNFT"