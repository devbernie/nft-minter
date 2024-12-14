import click
import json
from src.config import Config
from src.api.koios import KoiosAPI
from src.api.blockchain import BlockchainManager
from src.nft.mint import NFTMinter
from src.nft.list import NFTLister
from src.nft.buy import NFTBuyer
from src.nft.sell import NFTSeller

@click.group()
def cli():
    """CLI for NFT operations."""
    pass

@cli.command()
@click.option('--asset-name', required=True, help='Name of the NFT asset')
@click.option('--metadata', required=True, help='Metadata for the NFT in JSON format')
@click.option('--image-url', required=True, help='URL of the image for the NFT')
@click.option('--amount', default=1, help='Amount of NFTs to mint')
def mint(asset_name, metadata, image_url, amount):
    """Mint a new NFT."""
    try:
        koios_api = KoiosAPI(Config.API_BASE_URL)
        blockchain_manager = BlockchainManager(koios_api, Config.NETWORK)
        minter = NFTMinter(blockchain_manager)
        
        metadata_dict = json.loads(metadata)
        result = minter.mint_nft(
            Config.WALLET_ADDRESS,
            asset_name,
            metadata_dict,
            image_url,
            amount
        )
        click.echo("NFT minted successfully")
        click.echo(f"Transaction hash: {result['tx_hash']}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
def list_nfts():
    """List all NFTs in the wallet."""
    try:
        koios_api = KoiosAPI(Config.API_BASE_URL)
        assets = koios_api.get_account_assets(Config.WALLET_ADDRESS)
        if not assets:
            click.echo("No NFTs found in wallet")
            return
        
        for asset in assets:
            click.echo(f"Asset Name: {asset['asset_name']}, quantity: {asset['quantity']}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.option('--asset-name', required=True, help='Name of the NFT asset to sell')
@click.option('--price', required=True, type=int, help='Price in lovelace')
def sell(asset_name, price):
    """List an NFT for sale."""
    try:
        seller = NFTSeller()
        
        result = seller.list_for_sale(asset_name, price, Config.WALLET_ADDRESS)
        click.echo("NFT listed for sale")
        click.echo(f"Transaction details: {result}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.option('--seller-address', required=True, help='Address of the NFT seller')
@click.option('--price', required=True, type=int, help='Price in lovelace')
@click.option('--asset-name', required=True, help='Name of the NFT asset to buy')
def buy(seller_address, price, asset_name):
    """Buy an NFT."""
    try:
        koios_api = KoiosAPI(Config.API_BASE_URL)
        blockchain_manager = BlockchainManager(koios_api, Config.NETWORK)
        buyer = NFTBuyer(blockchain_manager)
        
        result = buyer.buy_nft(Config.WALLET_ADDRESS, seller_address, asset_name, price)
        click.echo("NFT purchased successfully")
        click.echo(f"Transaction hash: {result['tx_hash']}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

cli.add_command(mint)
cli.add_command(list_nfts)
cli.add_command(sell)
cli.add_command(buy)

if __name__ == '__main__':
    cli()