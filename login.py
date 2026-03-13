import os
import sys
from configparser import ConfigParser
from telethon.sync import TelegramClient

def main():
    if not os.path.exists('config.ini'):
        print("ERROR: No se encontró 'config.ini'. Copia 'config.example.ini' a 'config.ini' y añade tus datos.")
        sys.exit(1)

    config = ConfigParser()
    config.read('config.ini')

    try:
        api_id = config.getint('Telegram', 'api_id')
        api_hash = config.get('Telegram', 'api_hash')
        phone = config.get('Telegram', 'phone')
    except Exception as e:
        print(f"ERROR: config.ini mal configurado: {e}")
        sys.exit(1)

    print("Iniciando conexión con Telegram (se creará el archivo mi_sesion.session)...")
    print("Revisa tu aplicación móvil de Telegram o tus SMS, te llegará un código de verificación.")
    
    # Iniciamos el cliente de forma síncrona para que se conecte fácilmente por consola
    client = TelegramClient('mi_sesion', api_id, api_hash)
    client.start(phone=phone)

    print("\n✅ ¡Sesión iniciada con éxito! Ya puedes cerrar este script e iniciar 'python main.py'.")
    client.disconnect()

if __name__ == "__main__":
    main()
