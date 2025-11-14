# app/connection.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

from app.config import Config
from app.logger import setup_logger

logger = setup_logger("Connection")

def connect_to_chrome(cfg: Config) -> webdriver.Chrome | None:
    try:
        options = Options()
        options.add_experimental_option("debuggerAddress", cfg.debugger_address)
        driver = webdriver.Chrome(options=options)
        
        logger.info("✅ Conectado correctamente a Chrome en modo Debug seguro.")
        return driver
    except WebDriverException as e:
        logger.error(f"❌ No se pudo conectar a Chrome en {cfg.debugger_address}: {e}")
        return None
