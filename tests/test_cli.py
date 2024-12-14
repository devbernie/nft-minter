import pytest
from click.testing import CliRunner
from src.cli import cli
from src.config import Config
from unittest.mock import patch, MagicMock

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

@patch("src.api.koios.KoiosAPI")
def test_list_nfts_command(mock_koios_class, monkeypatch):
    mock_instance = MagicMock()
    mock_instance.get_account_assets.return_value = [
        {"asset_name": "TestNFT", "quantity": 2}
    ]
    mock_koios_class.return_value = mock_instance
    
    monkeypatch.setattr(Config, "WALLET_ADDRESS", "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u")
    monkeypatch.setattr(Config, "API_BASE_URL", "https://preview.koios.rest/api/v1")
    
    runner = CliRunner()
    result = runner.invoke(cli, ["list_nfts"])
    
    # Debugging output
    print("Output:", result.output)
    print("Exit Code:", result.exit_code)
    
    assert result.exit_code == 0
    assert "TestNFT" in result.output
    assert "quantity: 2" in result.output
    
    mock_instance.get_account_assets.assert_called_once_with(Config.WALLET_ADDRESS)

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