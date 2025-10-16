import os
from downloader import connect_to_chrome, download_images

BASE_PATH = r"C:\\Users\\Hector\\Documents\\The Fearless Storyteller\\images"

def listar_carpetas_y_archivos(path):
    print("\n📂 Carpetas existentes dentro de la madre:")
    carpetas = sorted(os.listdir(path))
    if not carpetas:
        print("\n   (Vacío)")
        return
    for carpeta in carpetas:
        carpeta_path = os.path.join(path, carpeta)
        if os.path.isdir(carpeta_path):
            imagenes = [img for img in sorted(os.listdir(carpeta_path))
                        if img.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))]
            if imagenes:
                nombres = " - ".join(imagenes)
                print(f"\n N° {carpeta} ({len(imagenes)} imágenes):")
                print(f" [ {nombres} ]")
            else:
                print(f"\n N° {carpeta} (vacía)")

def obtener_siguiente_numero(path):
    existentes = [int(c) for c in os.listdir(path) if c.isdigit()]
    if not existentes:
        return "01"
    siguiente = max(existentes) + 1
    return f"{siguiente:02d}"

def buscar_carpeta_vacia(path):
    for carpeta in sorted(os.listdir(path)):
        carpeta_path = os.path.join(path, carpeta)
        if os.path.isdir(carpeta_path):
            if not any(fname.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))
                       for fname in os.listdir(carpeta_path)):
                return carpeta
    return None

def main():
    while True:
        try:
            numero = int(input("Ingrese el número de carpeta madre (1-9999): "))
            if 1 <= numero <= 9999:
                break
            else:
                print("❌ Debe ser un número entre 1 y 9999.")
        except ValueError:
            print("❌ Entrada inválida. Intente nuevamente.")
    carpeta_madre = f"{numero:04d}"
    ruta_madre = os.path.join(BASE_PATH, carpeta_madre)
    if not os.path.exists(ruta_madre):
        os.makedirs(ruta_madre)
        print(f"\n✅ Carpeta madre creada: {ruta_madre}")
    else:
        print(f"\n⚠️  La carpeta madre '{carpeta_madre}' ya existe en:")
        print(ruta_madre)
        listar_carpetas_y_archivos(ruta_madre)
    carpeta_vacia = buscar_carpeta_vacia(ruta_madre)
    if carpeta_vacia:
        nueva_carpeta_hija = os.path.join(ruta_madre, carpeta_vacia)
        print(f"\n📁 Se usará la carpeta vacía existente: {carpeta_vacia}")
    else:
        siguiente = obtener_siguiente_numero(ruta_madre)
        nueva_carpeta_hija = os.path.join(ruta_madre, siguiente)
        os.makedirs(nueva_carpeta_hija, exist_ok=True)
        print(f"\n🆕 Se creó automáticamente la carpeta hija: {siguiente}")
    print(f"\n📍 Ruta final donde se guardarán las imágenes:")
    print(nueva_carpeta_hija)
    print("\nConectando a Chrome abierto...")
    driver = connect_to_chrome()
    if driver:
        print("\n🖼️ Iniciando la generación y descarga de imágenes...")
        download_images(driver, nueva_carpeta_hija, max_images=32)

if __name__ == "__main__":
    main()
