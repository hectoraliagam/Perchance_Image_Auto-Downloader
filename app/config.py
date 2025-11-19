# app/config.py

from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Config:
    # --- Paths and folders ---
    base_path: str = ""
    total_subfolders: int = 16
    images_per_subfolder: int = 32
    valid_extensions: Tuple[str, ...] = (".jpg", ".jpeg", ".png", ".webp")
    # --- Chrome ---
    debugger_address: str = "127.0.0.1:9222"
    generate_button_xpath: str = "//*[@id='generateButtonEl']"
    outer_iframe_xpath: str = "//*[@id='outputIframeEl']"
    output_area_xpath: str = "//*[@id='outputAreaEl']/div"
    result_img_id: str = "resultImgEl"
    # --- Download loop ---
    poll_interval: int = 2
    patience_limit: int = 30
