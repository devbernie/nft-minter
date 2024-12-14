# cli.py
import click
import os
from dotenv import load_dotenv
from src.nft.mint import NFTMinter
from src.nft.list import NFTLister
from src.nft.buy import NFTBuyer
from src.nft.sell import NFTSeller
from src.api.blockchain import BlockchainManager
from src.nft.utils import validate_image_url
from src.api.koios import KoiosAPI
from pycardano import PaymentSigningKey, Network

# Load environment variables
load_dotenv()

@click.group()
def cli():
    """CLI Tool for managing NFTs on Cardano Preview Testnet."""
    pass

@cli.command()
@click.option('--asset-name', prompt='Asset name', help='The name of the NFT asset.')
@click.option('--metadata', prompt='Metadata (JSON format)', help='Metadata of the NFT asset.')
@click.option('--image-url', prompt='Image URL (optional)', default=None, help='Optional URL of the image for the NFT.')
@click.option('--amount', default=1, help='The amount of NFTs to mint (default: 1).')
def mint(asset_name, metadata, image_url, amount):
    """Mint a new NFT."""
    try:
        blockchain_manager = BlockchainManager(None, Config.NETWORK)
        metadata_dict = eval(metadata)  # Convert string input to dictionary
        result = NFTMinter(blockchain_manager).mint_nft(
            Config.WALLET_ADDRESS, asset_name, metadata_dict, image_url, amount
        )
        click.echo(f"NFT minted successfully: {result}")
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.option('--wallet-address', default=os.getenv("WALLET_ADDRESS"), help='Wallet address to list NFTs.')
def list_nfts(wallet_address):
    """List all NFTs in a wallet."""
    try:
        nft_lister = NFTLister(None)
        nfts = nft_lister.list_nfts(wallet_address)
        click.echo(nfts)
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.option('--asset-name', prompt='Asset name', help='The name of the NFT asset.')
@click.option('--price', prompt='Price in ADA', type=int, help='Price of the NFT in ADA.')
def sell(asset_name, price):
    """List an NFT for sale."""
    try:
        wallet_address = os.getenv("WALLET_ADDRESS")
        seller = NFTSeller()
        listing = seller.list_for_sale(asset_name, price, wallet_address)
        click.echo(f"NFT listed for sale: {listing}")
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.option('--seller-address', prompt='Seller address', help='Address of the NFT seller.')
@click.option('--price', prompt='Price in ADA', type=int, help='Price of the NFT in ADA.')
def buy(seller_address, price):
    """Buy an NFT from a seller."""
    try:
        wallet_address = os.getenv("WALLET_ADDRESS")
        signing_key_path = os.getenv("SIGNING_KEY_PATH")
        network = os.getenv("NETWORK")

        blockchain_manager = BlockchainManager(None, network)
        signing_key = PaymentSigningKey.load(signing_key_path)

        buyer = NFTBuyer(blockchain_manager)
        result = buyer.buy_nft(wallet_address, seller_address, signing_key, price)
        click.echo(f"NFT purchased successfully: {result}")
    except Exception as e:
        click.echo(f"Error: {e}")

if __name__ == '__main__':
    cli()