import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
LOCATION = "us-central1"
