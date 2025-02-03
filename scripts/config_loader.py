import json
import os

# Define the absolute path to config.json
CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Moves up one directory
CONFIG_PATH = os.path.join(CONFIG_DIR, "config", "config.json")

def load_config(config_path=CONFIG_PATH):
    """Load and return the configuration file as a dictionary."""
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON in: {config_path}")
