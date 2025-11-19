# app/utils.py

import os
import json
import tkinter as tk
from tkinter import filedialog
from dataclasses import fields
from typing import Any, Dict, List, Optional

from app.config import Config
from app.logger import setup_logger

logger = setup_logger("Utils")


# ------------------------------
# Conversión dataclass
# ------------------------------
def _dict_to_dataclass(dc_class, data: Dict[str, Any]):
    field_names = {f.name for f in fields(dc_class)}
    filtered = {k: v for k, v in data.items() if k in field_names}
    
    # Normalizar listas a tuplas
    if "valid_extensions" in filtered and isinstance(filtered["valid_extensions"], list):
        filtered["valid_extensions"] = tuple(filtered["valid_extensions"])
        
    return dc_class(**filtered)


# ------------------------------
# Guardar JSON actualizado
# ------------------------------
def _guardar_config(path: str, data: Dict[str, Any]):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f"💾 Configuración actualizada en: {path}")
    except Exception as e:
        logger.error(f"❌ Error guardando configuración: {e}")


# ------------------------------
# Mostrar diálogo de selección
# ------------------------------
def seleccionar_carpeta_inicial(mensaje: str = "Selecciona la carpeta base") -> str:
    logger.info(f"📁 Abriendo explorador de archivos: {mensaje}")
    
    root = tk.Tk()
    root.withdraw()
    
    ruta = filedialog.askdirectory(title=mensaje)
    root.destroy()
    
    if ruta:
        logger.info(f"📁 Carpeta seleccionada: {ruta}")
    else:
        logger.warning("⚠️ No se seleccionó ninguna carpeta.")
        
    return ruta


# ------------------------------
# Cargar configuración + UI base_path
# ------------------------------
def load_config_from_json(path: str) -> Config:
    logger.info(f"🔧 Cargando configuración desde: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    base_path = data.get("base_path", "").strip()
    
    # 1. Base path vacío o inválido -> forzar selección
    if not base_path or not os.path.isdir(base_path):
        logger.warning("⚠️ No se detectó un 'base_path' válido.")
        nueva = seleccionar_carpeta_inicial("Selecciona la carpeta base para guardar las imágenes")
        
        if nueva:
            data["base_path"] = nueva.replace("\\", "/")
            _guardar_config(path, data)
        else:
            logger.error("❌ No se seleccionó carpeta. Abortando.")
            raise Exception("No se seleccionó ninguna carpeta.")
        
    # 2. Base path válido -> preguntar si desea cambiarlo
    else:
        logger.info(f"📂 Carpeta actual configurada: {base_path}")
        
        try:
            resp = input("¿Deseas cambiarla? (s/n): ").strip().lower()
        except Exception:
            resp = "n"
            
        logger.info(f"📝 Respuesta del usuario: {resp}")
        
        if resp == "s":
            nueva = seleccionar_carpeta_inicial("Selecciona la nueva carpeta base")
            
            if nueva:
                data["base_path"] = nueva.replace("\\", "/")
                _guardar_config(path, data)
            else:
                logger.info("➡️ Manteniendo la carpeta anterior sin cambios.")
                
    # Convertir a dataclass final
    cfg = _dict_to_dataclass(Config, data)
    logger.info(f"✅ Configuración final cargada correctamente.")
    return cfg


# ------------------------------
# Listado de carpetas
# ------------------------------
def listar_carpetas_y_archivos(path: str, cfg: Config) -> None:
    if not os.path.exists(path):
        logger.warning(f"⚠️ La ruta {path} no existe.")
        return
    
    logger.info("📂 Explorando subcarpetas dentro de la carpeta madre...")
    
    carpetas = sorted(os.listdir(path))
    if not carpetas:
        logger.info("📂 (Vacío)")
        return
    
    for carpeta in carpetas:
        carpeta_path = os.path.join(path, carpeta)
        if os.path.isdir(carpeta_path):
            imagenes = obtener_imagenes(carpeta_path, cfg)
            estado = f"{len(imagenes)} imágenes" if imagenes else "vacía"
            logger.info(f"📁 Subcarpeta {carpeta} → {estado}")


# ------------------------------
# Obtener imágenes filtradas
# ------------------------------
def obtener_imagenes(path: str, cfg: Config) -> List[str]:
    try:
        return [
            img for img in sorted(os.listdir(path))
            if img.lower().endswith(cfg.valid_extensions)
        ]
    except FileNotFoundError:
        logger.warning(f"⚠️ Carpeta no encontrada: {path}")
        return []


# ------------------------------
# Contar imágenes
# ------------------------------
def contar_imagenes_en(path: str, cfg: Config) -> int:
    return len(obtener_imagenes(path, cfg))


# ------------------------------
# Validar si carpeta existe
# ------------------------------
def join_if_dir(path: str, carpeta: str) -> Optional[str]:
    ruta = os.path.join(path, carpeta)
    return ruta if os.path.isdir(ruta) else None
