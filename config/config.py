from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def config():
    """
    Load the configuration settings from environment variables or default values.
    Returns a dictionary containing all the necessary configuration values.
    """
    return {
        "WATCH_DIR": os.getenv("WATCH_DIR", "/opt/watch_narutow/"),
        "DB_NAME": os.getenv("DB_NAME", "watch"),
        "DB_HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "DB_PORT": int(os.getenv("DB_PORT", 27017)),
        "DB_USERNAME": os.getenv("DB_USERNAME", None),
        "DB_PASSWORD": os.getenv("DB_PASSWORD", None),
        "AUTH_SOURCE": os.getenv("AUTH_SOURCE", "admin"),
        "WEBHOOK_URL": os.getenv("WEBHOOK_URL", "https://example.com/webhook"),
        "DEBUG": os.getenv("DEBUG", "False").lower() in ["true", "1", "t"],
        "SECRET_KEY": os.getenv("SECRET_KEY", "supersecretkey"),
    }

