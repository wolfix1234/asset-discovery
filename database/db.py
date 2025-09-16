from mongoengine import connect
from config import config

def initialize_db():
    """
    Initialize the connection to the MongoDB database.
    """
    # Assuming your config function returns a dictionary or object containing database configurations
    db_config = config()

    connect(
        db=db_config.get('DB_NAME', 'watch'),  # Database name, default to 'watch'
        host=db_config.get('DB_HOST', '127.0.0.1'),  # Database host, default to localhost
        port=db_config.get('DB_PORT', 27017),  # Database port, default to 27017
    )
