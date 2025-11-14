# app/utils.py

import os
import json
from dataclasses import fields
from typing import Any, Dict, List, Optional

from app.config import Config
from app.logger import setup_logger

logger = setup_logger("Utils")

def _dict_to_dataclass(dc_class, data: Dict[str, Any]):
    field_names = {f.name for f in fields(dc_class)}
    filtered = {k: v for k, v in data.items() if k in field_names}
    # Normalizar listas a tuplas
    if "valid_extensions" in filtered and isinstance(filtered["valid_extensions"], list):
        filtered["valid_extensions"] = tuple(filtered["valid_extensions"])
    return dc_class(**filtered)

def load_config_from_json(path: str) -> Config:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return _dict_to_dataclass(Config, data)

def listar_carpetas_y_archivos(path: str, cfg: Config) -> None:
    if not os.path.exists(path):
        logger.warning(f"⚠️ La ruta {path} no existe.")
        return
    
    logger.info("📂 Carpetas existentes dentro de la madre:")
    carpetas = sorted(os.listdir(path))
    if not carpetas:
        logger.info("(Vacío)")
        return
    
    for carpeta in carpetas:
        carpeta_path = os.path.join(path, carpeta)
        if os.path.isdir(carpeta_path):
            imagenes = obtener_imagenes(carpeta_path, cfg)
            estado = f"{len(imagenes)} imágenes" if imagenes else "vacía"
            logger.info(f"N° {carpeta} ({estado})")
            
def obtener_imagenes(path: str, cfg: Config) -> List[str]:
    try:
        return [
            img for img in sorted(os.listdir(path))
            if img.lower().endswith(cfg.valid_extensions)
        ]
    except FileNotFoundError:
        logger.warning(f"⚠️ Carpeta no encontrada: {path}")
        return []

def contar_imagenes_en(path: str, cfg: Config) -> int:
    return len(obtener_imagenes(path, cfg))

def join_if_dir(path: str, carpeta: str) -> Optional[str]:
    ruta = os.path.join(path, carpeta)
    return ruta if os.path.isdir(ruta) else None
