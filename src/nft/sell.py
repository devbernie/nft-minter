# sell.py
class NFTSeller:
    """
    Handles the listing of NFTs for sale.
    """
    def __init__(self):
        self.listings = []  # Example: [{'asset_name': 'MyNFT', 'price': 1000000, 'seller': 'addr...'}]

    def list_for_sale(self, asset_name, price, seller_address):
        """
        List an NFT for sale.

        :param asset_name: Name of the NFT asset
        :param price: Price in lovelace
        :param seller_address: Address of the seller
        """
        listing = {
            "asset_name": asset_name,
            "price": price,
            "seller": seller_address
        }
        self.listings.append(listing)
        return listing

    def get_listings(self):
        """
        Retrieve all current NFT listings.

        :return: List of NFT listings
        """
        return self.listings