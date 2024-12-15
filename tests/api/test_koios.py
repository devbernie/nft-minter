# test_koios.py
import pytest
from src.api.koios import KoiosAPI
from unittest.mock import patch

@pytest.fixture
def koios_api():
    return KoiosAPI()

def test_get_address_assets(koios_api):
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = [{"asset": "asset_1"}]

        result = koios_api.get_address_assets("addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u")
        assert len(result) == 1
        assert result[0]["asset"] == "asset_1"

def test_submit_transaction(koios_api):
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"tx_hash": "mock_hash"}

        result = koios_api.submit_transaction("mock_cbor_hex")
        assert result["tx_hash"] == "mock_hash"