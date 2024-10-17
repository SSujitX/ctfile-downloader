import os
import yaml
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config(config_path="config.yml"):
    """Loads configuration from the YAML file. If it doesn't exist, it prompts the user for basic details and creates one."""
    if not os.path.exists(config_path):
        logging.warning("Configuration file not found. Creating a new one.")
        config = create_default_config(config_path)
    else:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
    return config


def create_default_config(config_path):
    """Creates a default configuration file based on user input."""
    logging.info("To use this downloader, you must be a premium member of CTFile.\n")

    username = input("Enter your CTFile username: ").strip()
    password = input("Enter your CTFile password: ").strip()

    # Default configuration
    default_config = {
        "directories": ["CTFile Downloaded", "CTFile Batch Text", "CTFile Text Files"],
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        },
        "passcodes": ["4431", "6688"],
        "batch_folder": "CTFile Batch Text",
        "download_folder": "CTFile Downloaded",
        "credentials": {"username": username, "password": password},
    }

    # Save to config.yml
    with open(config_path, "w") as file:
        yaml.safe_dump(default_config, file)

    logging.info(f"Configuration file created at {config_path}.\n")
    return default_config


def create_directories(config):
    """Ensures necessary directories exist."""
    directories = config.get("directories", [])
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


def get_credentials(config):
    """Retrieves credentials from the config."""
    credentials = config.get("credentials", {})
    return credentials.get("username"), credentials.get("password")
