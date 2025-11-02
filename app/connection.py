from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

from app.config import Config
from app.logger import setup_logger

logger = setup_logger("Connection")

def connect_to_chrome(cfg: Config) -> webdriver.Chrome | None:
    try:
        options = Options()
        options.debugger_address = cfg.debugger_address
        driver = webdriver.Chrome(options=options)
        logger.info("✅ Conectado correctamente a Chrome.")
        return driver
    except WebDriverException as e:
        logger.error(f"❌ No se pudo conectar a Chrome en {cfg.debugger_address}: {e}")
        return None
