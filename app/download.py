# app/download.py

import os
import base64
from typing import Set

from selenium.webdriver.remote.webdriver import WebDriver

from app.config import Config
from app.logger import setup_logger
from app.helpers import human_delay, click_generate_button, detect_new_images

logger = setup_logger("Download")


def save_base64_image(img_src: str, filename: str) -> bool:
    try:
        if "," not in img_src:
            logger.error(f"❌ Formato inválido de imagen base64 para {filename}")
            return False
        
        img_data = base64.b64decode(img_src.split(",", 1)[1])
        with open(filename, "wb") as f:
            f.write(img_data)
        
        human_delay(0.2, 0.6)
        logger.debug(f"🖼️ Imagen guardada en {filename}")
        return True
    except Exception as e:
        logger.error(f"❌ Error al guardar imagen {filename}: {e}")
        return False

def download_images(driver: WebDriver, save_path: str, max_images: int = 32, cfg: Config = Config()) -> None:
    os.makedirs(save_path, exist_ok=True)
    
    existing_files = [
        f for f in os.listdir(save_path)
        if f.lower().endswith(cfg.valid_extensions)
    ]
    existing_files.sort()
    existing_count = len(existing_files)
    
    downloaded: Set[str] = set()
    idle_cycles = 0
    last_count = 0
    
    logger.info("🖼️ Iniciando generación y descarga de imágenes...")
    human_delay(1.5, 3.0)
    
    if not click_generate_button(driver, cfg):
        logger.error("❌ No se pudo iniciar la generación. Abortando.")
        return
    
    objetivo_total = existing_count + max_images
    logger.info(f"⌛ Esperando generación de imágenes... Objetivo: {objetivo_total} imágenes")
    
    while existing_count + len(downloaded) < objetivo_total:
        human_delay(1.0, 1.8)
        new_imgs = detect_new_images(driver, downloaded, cfg)
        
        if new_imgs:
            idle_cycles = 0
            for img_src in new_imgs:
                downloaded.add(img_src)
                index = existing_count + len(downloaded)
                filename = os.path.join(save_path, f"{index:02}.jpeg")
                
                if img_src.startswith("data:image/jpeg;base64,"):
                    if save_base64_image(img_src, filename):
                        logger.info(f"✅ Imagen {index:02} descargada correctamente.")
                        human_delay(1.2, 3.5)
                else:
                    logger.warning(f"⚠️ Fuente no reconocida para imagen {index:02}.")
                
                logger.info(f"📊 Progreso: {existing_count + len(downloaded)}/{objetivo_total} imágenes descargadas en {os.path.basename(save_path)}")
                human_delay(0.8, 1.5)
                
                if existing_count + len(downloaded) >= objetivo_total:
                    break
                
        else:
            idle_cycles += 1
            idle_time = idle_cycles * cfg.poll_interval
            human_delay(0.6, 1.4)
            
            if idle_cycles % 5 == 0:
                logger.info(f"⌛ Esperando nuevas imágenes... ({idle_time}s sin cambios)")
                
            if idle_time >= 60:
                logger.warning("⚠️ 60s sin nuevas imágenes. Reintentando pulsar 'Generate'...")
                if click_generate_button(driver, cfg):
                    logger.info("🔄️ Reintento exitoso: botón 'Generate' pulsado de nuevo.")
                    human_delay(2.0, 4.0)
                    idle_cycles = 0
                else:
                    logger.error("❌ Reintento fallido al pulsar 'Generate'.")
                    
            if idle_cycles >= cfg.patience_limit:
                logger.warning("⚠️ No se detectan nuevas imágenes desde hace demasiado tiempo. Finalizando.")
                break
            
        if len(downloaded) != last_count:
            last_count = len(downloaded)
        
        human_delay(cfg.poll_interval * 0.8, cfg.poll_interval * 1.2)
    
    total_final = existing_count + len(downloaded)
    logger.info(f"🎉 Descarga completada: {total_final} imágenes guardadas en '{save_path}'.")
