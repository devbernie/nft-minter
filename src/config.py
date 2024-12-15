class Config:
    API_BASE_URL = "https://preview.koios.rest/api/v1"
    NETWORK = "preview"
    WALLET_ADDRESS = ""  # Set a default value or leave empty
    SIGNING_KEY = None  # Add this to define SIGNING_KEY

    @staticmethod
    def get(attr, default=None):
        return getattr(Config, attr, default)