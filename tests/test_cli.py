import pytest
from click.testing import CliRunner
from src.cli.cli import cli
from src import config
from unittest.mock import patch, MagicMock

@patch("src.cli.cli.BlockchainManager.mint_nft", return_value={"tx_hash": "mock_hash"})
def test_mint_command(mock_mint, monkeypatch):
    monkeypatch.setattr(config.Config, "WALLET_ADDRESS", "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u")
    runner = CliRunner()
    result = runner.invoke(cli, [
        "mint", "--asset-name", "TestNFT",
        "--metadata", '{"name": "Test NFT"}',
        "--image-url", "https://i.imgur.com/CZwugry.jpeg", "--amount", "1"
    ])
    assert result.exit_code == 0
    assert "NFT minted successfully" in result.output

@patch("src.cli.cli.KoiosAPI.get_account_assets", return_value=[{"asset_name": "TestNFT", "quantity": 1}])
def test_list_nfts_command(mock_get_assets, monkeypatch):
    monkeypatch.setattr(Config, "WALLET_ADDRESS", "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u")
    runner = CliRunner()
    result = runner.invoke(cli, ["list_nfts"])
    assert result.exit_code == 0
    assert "TestNFT" in result.output

@patch("src.cli.cli.BlockchainManager.build_transaction", return_value=MagicMock())
@patch("src.cli.cli.BlockchainManager.sign_transaction", return_value=MagicMock())
@patch("src.cli.cli.BlockchainManager.submit_transaction", return_value={"tx_hash": "mock_hash"})
def test_sell_command(mock_build, mock_sign, mock_submit, monkeypatch):
    monkeypatch.setattr("src.cli.cli.Config.WALLET_ADDRESS", "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u")
    runner = CliRunner()
    result = runner.invoke(cli, [
        'sell',
        '--asset-name', 'TestNFT',
        '--price', '1000000'
    ])
    assert result.exit_code == 0
    assert "NFT listed for sale" in result.output

@patch("src.cli.cli.BlockchainManager.build_transaction", return_value=MagicMock())
@patch("src.cli.cli.BlockchainManager.sign_transaction", return_value=MagicMock())
@patch("src.cli.cli.BlockchainManager.submit_transaction", return_value={"tx_hash": "mock_hash"})
def test_buy_command(mock_build, mock_sign, mock_submit, monkeypatch):
    monkeypatch.setattr(config.Config, "WALLET_ADDRESS", "addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u")
    runner = CliRunner()
    result = runner.invoke(cli, [
        "buy", "--seller-address", "addr_test1qzmcx2fp747pzmqpsgfmzmlwjgkkcxxajjw4dy3fwhpjztkfq5vxr694la5f87y709k0alm2dtnl7rl04a9nvccunwtseskzvv", "--price", "1000000"
    ])
    assert result.exit_code == 0
    assert "NFT purchased successfully" in result.output