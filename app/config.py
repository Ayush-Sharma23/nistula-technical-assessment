from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
ENVIRONMENT = os.getenv("ENVIRONMENT")
DATABASE_URL = os.getenv("DATABASE_URL")
ANTHROPIC_API_KEY=os.getenv("ANTHROPIC_API_KEY")