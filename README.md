# Perchance Image Auto-Downloader

This tool automates the generation and downloading of unlimited images
from **Perchance AI Text‑to‑Image Generator**\
(https://perchance.org/ai-text-to-image-generator), using **Selenium**
and a manually opened Chrome session in **debug mode**.

⚠️ **Importante:**\
El sitio puede mostrar **CAPTCHA** después de muchas descargas. El programa actual no los resuelve, así que el proceso puede detenerse
temporalmente. Reiniciar Chrome Debug Mode en ese caso.

------------------------------------------------------------------------

## ⭐ Características

-   Automatiza el clic del botón **Generate**.
-   Detecta imágenes generadas dentro de múltiples iframes.
-   Descarga imágenes en formato **JPEG Base64**.
-   Organiza automáticamente las descargas en:
    -   **Carpeta madre**
    -   **Subcarpetas hijas numeradas**
-   Reintenta cuando no detecta nuevas imágenes.
-   Funciona con un Chrome YA ABIERTO en modo debug.

------------------------------------------------------------------------

## 📦 Requisitos

Instalar dependencias:

    pip install -r requirements.txt

Asegúrate de tener **Google Chrome** y **ChromeDriver** compatibles.

------------------------------------------------------------------------

## ⚙️ Configuración (`config.json`)

Ejemplo básico:

``` json
{
  "mother_folder": "output",
  "images_per_subfolder": 32,
  "total_subfolders": 10,
  "debugger_address": "127.0.0.1:9222",
  "outer_iframe_xpath": "//iframe[@id='app-iframe']",
  "generate_button_xpath": "//button[contains(text(),'Generate')]",
  "output_area_xpath": "//div[contains(@class,'images')]",
  "result_img_id": "result-img",
  "valid_extensions": [".jpeg", ".jpg"],
  "poll_interval": 3,
  "patience_limit": 25
}
```

Ajusta los XPaths si Perchance actualiza su diseño.

------------------------------------------------------------------------

## 🚀 Modo de Uso

### 1. Abre Chrome manualmente en modo debug:

Windows:

    chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeDebug"

Linux/macOS:

    google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"

### 2. Abre Perchance AI Text-to-Image Generator en esa ventana.

### 3. Ejecuta el programa:

    python main.py --config config.json

------------------------------------------------------------------------

## 📂 Estructura de carpetas generada

    output/
     ├── 001/
     │    ├── 01.jpeg
     │    ├── 02.jpeg
     │    └── ...
     ├── 002/
     ├── 003/
     └── ...

El programa crea automáticamente cada subcarpeta hija y las llena con la
cantidad exacta de imágenes configuradas.

------------------------------------------------------------------------

## 🧩 Cómo funciona internamente

-   `connect_to_chrome()` se conecta al Chrome abierto en modo debug.
-   `click_generate_button()` inicia nuevas generaciones.
-   `detect_new_images()` examina iframes internos para encontrar
    imágenes nuevas.
-   `download_images()` guarda todo en subcarpetas y maneja ciclos de
    espera si no aparecen nuevas imágenes.
-   `main()` coordina todo el proceso hasta completar todas las
    carpetas.

------------------------------------------------------------------------

## 🛑 Limitaciones

-   El CAPTCHA detiene el proceso. El usuario debe resolverlo
    manualmente.
-   Cambios en el DOM de Perchance pueden requerir actualizar XPaths.
-   No soporta generación sin Chrome abierto.

------------------------------------------------------------------------

## 🧑‍💻 Autor

Desarrollado por **hectoraliagam**

------------------------------------------------------------------------

## 📄 Licencia

MIT License.
