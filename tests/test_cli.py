import pytest
from click.testing import CliRunner
from src.cli.cli import cli
from src.config import Config
from src.api.koios import KoiosAPI
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_blockchain(monkeypatch):
    mock = MagicMock()
    # Mock the blockchain API client
    with patch('src.api.blockchain.BlockchainManager') as mock_api:
        mock_api.return_value = mock
        yield mock

@patch("src.nft.utils.requests.head")
@patch("src.api.blockchain.BlockchainManager.mint_nft", return_value={"tx_hash": "mock_hash"})
@patch("src.api.koios.KoiosAPI", return_value=MagicMock())
def test_mint_command(mock_koios, mock_mint, mock_head, monkeypatch):
    monkeypatch.setattr(Config, "WALLET_ADDRESS", "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u")
    mock_head.return_value.headers = {"Content-Type": "image/jpeg"}
    runner = CliRunner()
    result = runner.invoke(cli, [
        "mint", "--asset-name", "TestNFT",
        "--metadata", '{"name": "Test NFT"}',
        "--image-url", "https://i.imgur.com/CZwugry.jpeg", "--amount", "1"
    ])
    assert result.exit_code == 0
    assert "NFT minted successfully" in result.output

@patch("src.api.koios.KoiosAPI.get_account_assets")
@patch("src.api.blockchain.BlockchainManager.list_nfts")
def test_list_nfts_command(mock_list_nfts, mock_get_account_assets):
    # Mock the KoiosAPI.get_account_assets method
    mock_get_account_assets.return_value = [
        {"asset_name": "TestAsset1", "policy_id": "test_policy_1", "quantity": 1},
        {"asset_name": "TestAsset2", "policy_id": "test_policy_2", "quantity": 1}
    ]

    # Mock the BlockchainManager.list_nfts method
    mock_list_nfts.return_value = [
        {
            "name": "TestAsset1",
            "policy_id": "test_policy_1",
            "asset_name": "TestAsset1",
            "quantity": 1
        },
        {
            "name": "TestAsset2", 
            "policy_id": "test_policy_2",
            "asset_name": "TestAsset2",
            "quantity": 1
        }
    ]
    
    runner = CliRunner()
    result = runner.invoke(cli, ['list-nfts'])
    
    # Verify the command executed successfully
    assert result.exit_code == 0
    # Verify the expected output
    assert "TestAsset1" in result.output
    assert "test_policy_1" in result.output
    assert "TestAsset2" in result.output
    assert "test_policy_2" in result.output
    assert "Quantity: 1" in result.output

@patch("src.nft.sell.NFTSeller.list_for_sale", return_value={"asset_name": "TestNFT", "price": 1000000, "seller": "addr_test1..."})
@patch("src.api.koios.KoiosAPI", return_value=MagicMock())
def test_sell_command(mock_koios, mock_list_for_sale, monkeypatch):
    monkeypatch.setattr(Config, "WALLET_ADDRESS", "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u")
    runner = CliRunner()
    result = runner.invoke(cli, [
        "sell", "--asset-name", "TestNFT",
        "--price", "1000000"
    ])
    assert result.exit_code == 0
    assert "NFT listed for sale" in result.output

@patch("src.api.blockchain.BlockchainManager.build_transaction", return_value=MagicMock())
@patch("src.api.blockchain.BlockchainManager.sign_transaction", return_value=MagicMock())
@patch("src.api.blockchain.BlockchainManager.submit_transaction", return_value={"tx_hash": "mock_hash"})
@patch("src.api.koios.KoiosAPI", return_value=MagicMock())
def test_buy_command(mock_koios, mock_build, mock_sign, mock_submit, monkeypatch):
    monkeypatch.setattr(Config, "WALLET_ADDRESS", "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u")
    runner = CliRunner()
    result = runner.invoke(cli, [
        "buy", 
        "--seller-address", "addr_test1qzmcx2fp747pzmqpsgfmzmlwjgkkcxxajjw4dy3fwhpjztkfq5vxr694la5f87y709k0alm2dtnl7rl04a9nvccunwtseskzvv",
        "--price", "1000000",
        "--asset-name", "TestNFT"
    ])
    assert result.exit_code == 0
    assert "NFT purchased successfully" in result.output