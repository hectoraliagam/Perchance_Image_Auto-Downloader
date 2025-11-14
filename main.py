# main.py

import os
import argparse
from app.config import Config
from app.logic import preparar_carpeta_madre, obtener_subcarpetas_completas, obtener_siguiente_hija
from app.logger import setup_logger
from app.connection import connect_to_chrome
from app.download import download_images
from app.helpers import click_generate_button
from app.utils import load_config_from_json, contar_imagenes_en

logger = setup_logger("ImageDownloader")

def main(cfg: Config) -> None:
    logger.info("🔄️ Buscando carpeta madre activa...")
    ruta_madre = preparar_carpeta_madre(cfg)
    
    logger.info("Conectando a Chrome abierto...")
    driver = connect_to_chrome(cfg)
    if not driver:
        logger.error("❌ No se pudo conectar a Chrome. Abortando.")
        return
    if not click_generate_button(driver, cfg):
        logger.error("❌ No se pudo iniciar la generación. Abortando descarga de esta subcarpeta.")
        return
    
    while obtener_subcarpetas_completas(ruta_madre, cfg) < cfg.total_subfolders:        
        siguiente_hija, cantidad_actual = obtener_siguiente_hija(ruta_madre, cfg)
        ruta_hija = os.path.join(ruta_madre, siguiente_hija)
        os.makedirs(ruta_hija, exist_ok=True)
        
        faltantes = cfg.images_per_subfolder - cantidad_actual
        if faltantes <= 0:
            logger.info(f"✅ Subcarpeta {siguiente_hija} ya está completa.")
            continue
        
        logger.info(f"🆕 Preparando subcarpeta hija {siguiente_hija}...")
        logger.info(f"📍 Ruta final: {ruta_hija}")
        logger.info(f"🎯 Faltan {faltantes} imágenes para completar esta subcarpeta.")
        
        download_images(driver, ruta_hija, max_images=faltantes)
        if contar_imagenes_en(ruta_hija, cfg) == 0:
            logger.error(f"❌ La subcarpeta {siguiente_hija} sigue vacía. Revisa el botón 'Generate' o los selectores.")
            break
        logger.info(f"✅ Subcarpeta {siguiente_hija} completada correctamente.")
        
    logger.info("🏁 Proceso de generación terminado por completo.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.json", help="Ruta al archivo de configuración")
    args = parser.parse_args()
    
    try:
        cfg = load_config_from_json(args.config)
        main(cfg)
    except Exception as e:
        logger.exception(f"❌ Error inesperado en la ejecución: {e}")
