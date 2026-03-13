import sys
import os
import asyncio
from configparser import ConfigParser
from telethon import TelegramClient, events

from translator import Translator
from history_manager import HistoryManager

# Actualizamos la función de hilo al nuevo formato
async def process_msg_async(translator, text):
    """Ejecuta la API de IA en un hilo para no congelar Telegram."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, translator.process_message, text)

async def main():
    print("==============================================")
    print("   Iniciando Interceptor 'Magic Send' ")
    print("==============================================")
    
    # 1. Leemos Configuración
    config = ConfigParser()
    if not config.read('config.ini'):
        print("[ERROR FATAL] No se encontró el archivo 'config.ini'.")
        sys.exit(1)

    try:
        api_id = config.getint('Telegram', 'api_id')
        api_hash = config.get('Telegram', 'api_hash')
        target_chat = config.get('Telegram', 'target_chat_id')
        openrouter_key = config.get('OpenRouter', 'api_key')
    except Exception as e:
        print(f"[ERROR DE CONFIGURACIÓN] config.ini mal estructurado: {e}")
        sys.exit(1)

    # 2. Inicializamos Administradores (Módulos)
    translator = Translator(openrouter_key)
    history = HistoryManager()

    if not os.path.exists('mi_sesion.session'):
        print("[ALERTA] Sesión no encontrada. Ejecuta 'python login.py' primero.")
        sys.exit(1)

    print("\n[INFO] Conectando a Telegram de forma silenciosa...")
    # Usamos la sesión local para interceptar
    client = TelegramClient('mi_sesion', api_id, api_hash)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("[ERROR] Sesión inválida o expirada.")
        print("Solución: Elimina 'mi_sesion.session' y vuelve a ejecutar 'start.bat' para volver a loguearte.")
        sys.exit(1)

    print(f"\n✅ Conectado exitosamente a tu cuenta.")
    print(f"👂 Escuchando en tiempo real TODO lo que envíes a: {target_chat}")
    print("\n👉 CÓMO USARLO AHORA:")
    print(" - Si escribes en Español: Se traducirá y mandará el doble formato.")
    print(" - Si escribes en Inglés: Se corregirá tu ortografía y se mandará solo el Inglés.")
    print(" 5. (Deja esta pantalla abierta de fondo)\n")

    # Detectamos cualquier mensaje NUEVO, SALIENTE (outgoing), enviado al TARGET CHAT
    @client.on(events.NewMessage(outgoing=True, chats=target_chat))
    async def handler(event):
        try:
            spanish_text = event.raw_text.strip()
            
            # Filtros: Ignorar mensajes vacíos, fotos sin texto o si es un mensaje de sistema
            if not spanish_text:
                return
            
            # Para evitar un bucle infinito (ya que enviamos un mensaje outgoing que volvería a disparar este evento)
            # detectamos un carácter invisible que pondremos al final de nuestros mensajes traducidos.
            if "\u200b" in spanish_text:
                return
                
            print(f"[NUEVO RECEPTADO] Tú: {spanish_text}")
            
            # 1. Eliminamos tu mensaje original para reemplazarlo
            await event.delete()
            
            # 2. Pedimos traducción o corrección a la IA
            print("  ... Análisis en proceso ...")
            lang_original, texto_procesado, explanation = await process_msg_async(translator, spanish_text)
            
            # Guardamos la lección de gramática si la IA detectó errores en tu inglés
            if lang_original == "en" and explanation and explanation.upper() != "NONE":
                with open("grammar_lessons.txt", "a", encoding="utf-8") as f:
                    f.write(f"--- NUEVO ERROR (Tú escribiste: {spanish_text}) ---\n")
                    f.write(f"Corrección: {texto_procesado}\n")
                    f.write(f"Lección: {explanation}\n\n")
                print("  💡 [LECCIÓN DE GRAMÁTICA GUARDADA EN TXT]")

            # 3. Formateamos el mensaje dependiendo del idioma detectado
            if lang_original == "es":
                # Si era español, mandamos SOLO en inglés para no ocupar espacio
                mensaje_final = f"{texto_procesado}\u200b"
                print(f"  ✅ [ENVIADO INGLÉS TRADUCIDO ES -> EN]")
                # Guardamos solo cuando es una traducción en tu archivo de estudio
                history.record_phrase(spanish_text, texto_procesado)
            else:
                # Si era inglés, mandamos solo la corrección
                mensaje_final = f"{texto_procesado}\u200b"
                print(f"  ✅ [ENVIADO INGLÉS CORREGIDO EN -> EN]")
            
            # 4. Enviamos el resultado al chat de ella
            await client.send_message(
                event.chat_id, 
                mensaje_final, 
                reply_to=event.reply_to_msg_id
            )
            print("\n")
            
        except Exception as e:
            print(f"[ERROR] Hubo un fallo con el último envío: {e}")

    # Mantener el script corriendo y escuchando siempre usando asyncio
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        # En Windows, para evitar un "RuntimeError: Event loop is closed" al apagarlo
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[INFO] Apagando el interceptor 'Magic Send'... Hasta pronto.")
