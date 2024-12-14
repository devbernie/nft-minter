# test_sell.py
import pytest
from src.nft.sell import NFTSeller

@pytest.fixture
def seller():
    return NFTSeller()

def test_list_for_sale(seller):
    listing = seller.list_for_sale("TestNFT", 1000000, "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u")

    assert listing["asset_name"] == "TestNFT"
    assert listing["price"] == 1000000
    assert listing["seller"] == "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u"

def test_get_listings(seller):
    seller.list_for_sale("TestNFT", 1000000, "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u")
    listings = seller.get_listings()

    assert len(listings) == 1
    assert listings[0]["asset_name"] == "TestNFT"