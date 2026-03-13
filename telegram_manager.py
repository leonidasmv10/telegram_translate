import asyncio
import os
from telethon import TelegramClient

class TelegramManager:
    def __init__(self, api_id, api_hash, target_chat_id):
        self.api_id = api_id
        self.api_hash = api_hash
        self.target_chat_id = target_chat_id
        
        # Creamos un loop exclusivo para este thread
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Al no pasar `phone`, evitamos que intente loguearse aquí (dejamos que login.py lo haga)
        self.client = TelegramClient('mi_sesion', self.api_id, self.api_hash, loop=self.loop)

    def start_loop(self):
        """
        Conecta el cliente e inicia el event loop indefinidamente.
        Este método debe ser llamado desde su propio thread.
        """
        if not os.path.exists('mi_sesion.session'):
            raise RuntimeError("Sesión no encontrada. Ejecuta 'python login.py' primero.")
            
        asyncio.set_event_loop(self.loop)
        
        # Conectamos con la API
        self.loop.run_until_complete(self.client.connect())
        
        # Validamos que el usuario realmente está logueado
        if not self.loop.run_until_complete(self.client.is_user_authorized()):
            raise RuntimeError("Usuario no autorizado. Ejecuta 'python login.py' primero.")

        print("Telegram conectado y corriendo.")
        # Mantiene el loop vivo para poder encolar envíos
        self.loop.run_forever()

    def send_message_sync(self, text: str):
        """
        Encola de forma asíncrona pero devuelve de forma bloqueante (thread-safe).
        Se llama desde el main thread cuando el usuario presiona Enter.
        """
        future = asyncio.run_coroutine_threadsafe(
            self.client.send_message(self.target_chat_id, text),
            self.loop
        )
        return future.result(timeout=10)
        
    def disconnect(self):
        """Detiene de forma segura el bucle y cliente."""
        asyncio.run_coroutine_threadsafe(self.client.disconnect(), self.loop).result()
        self.loop.stop()
