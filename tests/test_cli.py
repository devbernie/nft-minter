import pytest
from click.testing import CliRunner
from src.cli import cli

def test_mint_command():
    runner = CliRunner()
    result = runner.invoke(cli, [
        'mint',
        '--asset-name', 'TestNFT',
        '--metadata', '{"name": "Test NFT", "description": "A test NFT"}',
        '--image-url', 'https://i.imgur.com/CZwugry.jpeg',
        '--amount', '1'
    ])
    assert result.exit_code == 0
    assert "NFT minted successfully" in result.output

def test_list_nfts_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['list_nfts'])
    assert result.exit_code == 0
    assert "[]" in result.output or "{" in result.output

def test_sell_command():
    runner = CliRunner()
    result = runner.invoke(cli, [
        'sell',
        '--asset-name', 'TestNFT',
        '--price', '1000000'
    ])
    assert result.exit_code == 0
    assert "NFT listed for sale" in result.output

def test_buy_command():
    runner = CliRunner()
    result = runner.invoke(cli, [
        'buy',
        '--seller-address', 'addr_test1qp28mg795hwlnptmdyr47zcrc87m8kk0pwvxrwrw24ppdzzquca5pnk4ew6068z6wu4tc9ee2rr2rnn06spkkvj0llqq7fnt8u',
        '--price', '1000000'
    ])
    assert result.exit_code == 0
    assert "NFT purchased successfully" in result.output