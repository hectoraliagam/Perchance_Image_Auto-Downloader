# app/helpers.py

import random
import time
from typing import Optional, Set, List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException, 
    ElementClickInterceptedException, 
    TimeoutException
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.config import Config
from app.logger import setup_logger

logger = setup_logger("Helpers")


def human_delay(base: float = 1.0, var: float = 1.0):
    delay = base + random.uniform(0, var)
    logger.debug(f"⏳ Esperando {delay:.2f}s (human delay)")
    time.sleep(delay)

def get_outer_iframe(driver: WebDriver, cfg: Config) -> Optional[WebElement]:
    human_delay(0.5, 0.8)
    try:
        iframe = driver.find_element(By.XPATH, cfg.outer_iframe_xpath)
        logger.debug("✅ Iframe principal encontrado.")
        return iframe
    except NoSuchElementException:
        logger.debug("No se encontró el iframe principal.")
        return None
    
def click_generate_button(driver: WebDriver, cfg: Config, timeout: int = 10) -> bool:
    human_delay(1.0, 1.5)
    outer_iframe = get_outer_iframe(driver, cfg)
    if not outer_iframe:
        logger.warning("⚠️ No se encontró el iframe principal. No se pulsará el botón.")
        return False
    
    try:
        driver.switch_to.frame(outer_iframe)
        human_delay(0.5, 1.0)
        
        btn = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, cfg.generate_button_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        human_delay(0.8, 1.2)
        
        driver.execute_script(
            "var ev = new MouseEvent('mouseover', {bubbles: true}); arguments[0].dispatchEvent(ev);",
            btn,
        )
        human_delay(0.4, 0.7)
        
        btn.click()
        logger.info("🚀 Botón 'Generate' pulsado correctamente.")
        human_delay(2.5, 1.5)
        return True
    
    except (NoSuchElementException, ElementClickInterceptedException, TimeoutException) as e:
        logger.error(f"❌ No se pudo pulsar el botón 'Generate': {e}")
        return False
    finally:
        driver.switch_to.default_content()
        
def detect_new_images(driver: WebDriver, known_urls: Set[str], cfg: Config) -> List[str]:
    human_delay(1.2, 1.5)
    new_imgs: List[str] = []
    outer_iframe = get_outer_iframe(driver, cfg)
    if not outer_iframe:
        return []
    
    try:
        driver.switch_to.frame(outer_iframe)
        human_delay(0.8, 1.0)
        containers = driver.find_elements(By.XPATH, cfg.output_area_xpath)
        logger.debug(f"Detectados {len(containers)} contenedores de imágenes.")
        
        for div in containers:
            human_delay(0.5, 0.8)
            inner_iframes = div.find_elements(By.TAG_NAME, "iframe")
            if not inner_iframes:
                continue
            
            inner_iframe = inner_iframes[0]
            if not inner_iframe.is_displayed():
                continue
            
            try:                
                driver.switch_to.frame(inner_iframe)
                human_delay(0.4, 0.6)
                img = driver.find_element(By.ID, cfg.result_img_id)
                img_src = img.get_attribute("src")
                
                if img_src and img_src not in known_urls:
                    new_imgs.append(img_src)
                    logger.debug(f"🖼️ Nueva imagen detectada: {img_src[:70]}...")
                    
            except NoSuchElementException:
                logger.debug("No se encontró imagen en un contenedor.")
            finally:
                driver.switch_to.parent_frame()
                
    except Exception as e:
        logger.warning(f"⚠️ Error al detectar imágenes: {e}")
    finally:
        driver.switch_to.default_content()
        
    return new_imgs
