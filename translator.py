from deep_translator import GoogleTranslator
from langdetect import detect
import re

class Translator:
    def __init__(self, api_key: str = None):
        """
        Iniciamos el traductor 100% rápido (Google Translate).
        Ya no usamos OpenRouter para ganar velocidad y estabilidad.
        """
        # Lista de palabras que NO queremos traducir para mantener el estilo personal/romántico
        self.protected_words = [
            "amor", "amorcito", "mi amor", "mi vida", "vida", "reina", "bebe", 
            "bebé", "corazon", "corazón", "cariño", "rey"
        ]

    def process_message(self, text: str):
        """
        Traduce el mensaje de forma instantánea usando Google Translate.
        Mantiene las palabras protegidas intactas.
        """
        try:
            # 1. Detectar idioma (muy rápido)
            try:
                lang_detected = detect(text)
            except:
                lang_detected = "es" # Por defecto español si falla la detección

            # Si el texto es muy corto o ya está en inglés, manejamos la detección
            if lang_detected != "en":
                lang_original = "es"
                target_lang = "en"
            else:
                lang_original = "en"
                target_lang = "en" # En modo traductor puro, el inglés se queda igual

            # 2. Protección de palabras (para que no traduzca "mi amor" -> "my love")
            placeholders = {}
            temp_text = text
            for i, word in enumerate(self.protected_words):
                # Buscamos la palabra con regex para que sea palabra completa e ignore mayúsculas
                pattern = re.compile(re.escape(word), re.IGNORECASE)
                matches = pattern.findall(temp_text)
                for match in matches:
                    placeholder = f"[[PROTECTED_{i}_{hash(match)}]]"
                    placeholders[placeholder] = match
                    temp_text = temp_text.replace(match, placeholder)

            # 3. Traducción Real (Instantánea)
            # Solo traducimos si detectamos que es español
            if lang_original == "es":
                resultado = GoogleTranslator(source='auto', target='en').translate(temp_text)
            else:
                # Si ya es inglés, solo devolvemos el texto (limpiando posibles placeholders)
                resultado = temp_text

            # 4. Restaurar palabras protegidas
            for placeholder, original_word in placeholders.items():
                resultado = resultado.replace(placeholder, original_word)

            # 5. Limpieza final de espacios o caracteres raros
            resultado = resultado.strip()

            print(f"    [OK] Traducción rápida completada ({lang_original} -> {target_lang})")
            return lang_original, resultado, "NONE"

        except Exception as e:
            print(f"    [!] Error en traducción rápida: {e}")
            return "es", text, "NONE"
