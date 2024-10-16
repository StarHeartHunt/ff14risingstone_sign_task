import logging

from .models import Settings

logging.basicConfig(level=logging.INFO)
settings = Settings()
logging.debug(f"Settings: {settings.model_dump_json()}")
