import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_BASE_URL = os.getenv("API_BASE_URL", "https://preview.koios.rest/api/v1")
    NETWORK = os.getenv("NETWORK", "preview")
    WALLET_ADDRESS = os.getenv("WALLET_ADDRESS", "")