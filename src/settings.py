import os

from dotenv import load_dotenv

load_dotenv()


COMMUNITY_TOKEN = os.getenv("COMMUNITY_TOKEN", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")
DATABASE_URL = os.getenv("DATABASE_URL", "")
