import os
from typing import Optional, Tuple

from app.config import Config
from app.logger import setup_logger
from app.utils import listar_carpetas_y_archivos, contar_imagenes_en, join_if_dir

logger = setup_logger("Logic")

def preparar_carpeta_madre(cfg: Config) -> str:
    if not os.path.exists(cfg.base_path):
        logger.warning(f"⚠️ Ruta base {cfg.base_path} no existe. Creándola...")
        os.makedirs(cfg.base_path, exist_ok=True)
        
    ultima_madre = obtener_ultima_carpeta_madre(cfg)
    if ultima_madre:
        ruta_madre = os.path.join(cfg.base_path, ultima_madre)
        if obtener_subcarpetas_completas(ruta_madre, cfg) >= cfg.total_subfolders:
            carpeta_madre = obtener_siguiente_madre(ultima_madre)
            ruta_madre = os.path.join(cfg.base_path, carpeta_madre)
            os.makedirs(ruta_madre, exist_ok=True)
            logger.info(f"🆕 Nueva carpeta madre creada automáticamente: {carpeta_madre}")
        else:
            carpeta_madre = ultima_madre
            logger.info(f"📁 Continuando con la carpeta madre existente: {carpeta_madre}")
    else:
        carpeta_madre = "0001"
        ruta_madre = os.path.join(cfg.base_path, carpeta_madre)
        os.makedirs(ruta_madre, exist_ok=True)
        logger.info(f"🆕 Creada carpeta madre inicial: {carpeta_madre}")
        
    listar_carpetas_y_archivos(ruta_madre, cfg)
    return ruta_madre

# --- Carpetas Madre ---
def obtener_ultima_carpeta_madre(cfg: Config) -> Optional[str]:
    carpetas = [c for c in os.listdir(cfg.base_path) if c.isdigit()]
    if not carpetas:
        return None
    return f"{max(int(c) for c in carpetas):04d}"

def obtener_siguiente_madre(actual: str) -> str:
    return f"{int(actual) + 1:04d}"

def obtener_subcarpetas_completas(path: str, cfg: Config) -> int:
    completas = 0
    for carpeta in sorted(os.listdir(path)):
        carpeta_path = join_if_dir(path, carpeta)
        if carpeta_path and contar_imagenes_en(carpeta_path, cfg) >= cfg.images_per_subfolder:
            completas += 1
    return completas

# --- Carpetas Hijas ---
def obtener_siguiente_hija(path: str, cfg: Config) -> Tuple[str, int]:
    carpetas = sorted([c for c in os.listdir(path) if c.isdigit()])
    for carpeta in carpetas:
        carpeta_path = join_if_dir(path, carpeta)
        if carpeta_path:
            cantidad = contar_imagenes_en(carpeta_path, cfg)
            if cantidad < cfg.images_per_subfolder:
                logger.info(f"🔁 Subcarpeta {carpeta} incompleta ({cantidad}/{cfg.images_per_subfolder}). Se completará ahora.")
                return carpeta, cantidad
            
    siguiente = len(carpetas) + 1
    return f"{siguiente:02d}", 0
