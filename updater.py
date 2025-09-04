import os
import sys
import requests
import tempfile
import subprocess

# Versión actual de tu app
CURRENT_VERSION = "1.0.0"

# Enlace al version.json en GitHub (en la rama principal)
VERSION_URL = "https://raw.githubusercontent.com/BJMAG/veterinaria/main/version.json"

def check_for_updates():
    try:
        response = requests.get(VERSION_URL)
        if response.status_code != 200:
            print("No se pudo verificar actualizaciones.")
            return

        data = response.json()
        latest_version = data.get("version")
        download_url = data.get("url")

        if latest_version != CURRENT_VERSION:
            print(f"Hay una nueva versión disponible: {latest_version}")
            download_and_install(download_url)
        else:
            print("La app está actualizada.")
    except Exception as e:
        print(f"Error al verificar actualizaciones: {e}")

def download_and_install(download_url):
    try:
        temp_dir = tempfile.gettempdir()
        new_exe_path = os.path.join(temp_dir, "mi_app_update.exe")

        print("Descargando la nueva versión...")
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(new_exe_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        print("Actualización descargada. Reemplazando ejecutable...")

        current_exe = sys.executable
        subprocess.Popen(
            f'ping 127.0.0.1 -n 3 > nul & move /Y "{new_exe_path}" "{current_exe}" & start "" "{current_exe}"',
            shell=True
        )
        sys.exit(0)
    except Exception as e:
        print(f"Error durante la actualización: {e}")

if __name__ == "__main__":
    check_for_updates()
