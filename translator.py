# NOTA: Usamos la librería de OpenAI porque OpenRouter es compatible con su formato.
# Esto no significa que estemos usando modelos de pago de OpenAI; 
# solo usamos su SDK para conectarnos a los modelos gratuitos de OpenRouter.
from openai import OpenAI

class Translator:
    def __init__(self, api_key: str):
        # Configuramos el cliente para que apunte a OpenRouter en lugar de a OpenAI
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        # Le decimos a la IA cómo queremos que traduzca de forma ultra-estricta
        self.system_instruction = (
            "You are a robotic, literal language converter. YOU HAVE NO CONDUCT OR FEELINGS.\n\n"
            "STRICT PROTOCOL:\n"
            "1. NO ADDITIONS: Never add words like 'babe', 'honey', 'hey', 'just', 'out' if they are not in the raw text.\n"
            "2. NO EMOJIS: If the user didn't put a 🥰, YOU MUST NOT PUT ONE. Forbidden: 🥰, ❤️, 😂, etc.\n"
            "3. PROTECTED TERMS: NEVER TRANSLATE 'amor', 'amorcito', 'mi amor', 'mi vida', 'vida', 'reina', 'bebe'. You MUST keep them in Spanish. Never use 'babe', 'honey', 'sweetheart' or 'love'.\n"
            "4. RAW CHARACTER MATCH: If the user says 'ohhh', your output must contain 'ohhh'. Never change it to 'Oh' or 'Ohhh'. Match the exact letters.\n\n"
            "EXAMPLES (STRICT COMPLIANCE):\n"
            "- INPUT: 'ohh amorcito, ¿cómo estás?'\n"
            "- CORRECT: 'ohh amorcito, how are you?'\n"
            "- INPUT: 'hola mi vida, valee'\n"
            "- CORRECT: 'hello mi vida, okay'\n\n"
            "IMPORTANT: Your response MUST be exactly in this format on three lines:\n"
            "LANG:es (if Spanish) or LANG:en (if English)\n"
            "TEXT:<result>\n"
            "EXPLANATION:<grammar explanation in Spanish for English mistakes, otherwise NONE>"
        )

    def process_message(self, text: str):
        """
        Procesa el texto. Devuelve (idioma_original, texto_procesado, explicacion_gramatical).
        """
        modelos_gratuitos = [
            "google/gemma-3-27b-it:free",               # Gemma es ultra inteligente pero rebotaba el "System" role
            "qwen/qwen3-next-80b-a3b-instruct:free",    # Qwen Next (Modelo gigantesco y muy capaz)
            "meta-llama/llama-3.2-3b-instruct:free",    # Llama 3 ligero, muy rápido
            "nvidia/nemotron-3-nano-30b-a3b:free"       # Nvidia Nemotron, gran respaldo
        ]

        for modelo in modelos_gratuitos:
            try:
                # Combinamos la instrucción con el texto en el rol "user" para evitar que modelos
                # restrictivos o plataformas como Google reboten el rol "system" (Causa del error 400).
                mensaje_combinado = f"{self.system_instruction}\n\nTEXTO A ANALIZAR:\n{text}"

                completion = self.client.chat.completions.create(
                    model=modelo, 
                    messages=[
                        {
                            "role": "user",
                            "content": mensaje_combinado
                        }
                    ],
                    temperature=0.3
                )
                output = completion.choices[0].message.content.strip()
                
                # --- FILTRO DE SEGURIDAD EXTRA (Mano de Hierro) ---
                # Si la IA intenta hacerse la graciosa y pone emojis o textos extra, lo limpiamos aquí.
                import re
                
                # Parsear el formato "LANG:xx \n TEXT:yy \n EXPLANATION:zz"
                lang = "es"
                result_text = ""
                explanation = "NONE"
                
                lines = [line.strip() for line in output.split('\n') if line.strip()]
                for line in lines:
                    if line.upper().startswith("LANG:"):
                        lang = line.split(":", 1)[1].strip().lower()
                    elif line.upper().startswith("TEXT:"):
                        result_text = line.split(":", 1)[1].strip()
                    elif line.upper().startswith("EXPLANATION:"):
                        explanation = line.split(":", 1)[1].strip()
                
                # Si por algún motivo TEXT está vacío o no se parseó bien
                if not result_text:
                    result_text = output.split('\n')[0] # Al menos tomamos la primera línea

                # LIMPIEZA FORZOSA: Eliminamos emojis y cualquier texto después de una barra "/" o paréntesis
                # que la IA use para dar "opciones". Queremos literalidad absoluta.
                if lang == "es":
                    # Elimina emojis comunes (rango unicode) para que no ensucie
                    result_text = re.sub(r'[^\x00-\x7F]+', '', result_text).strip()
                    # Si la IA puso opciones tipo "honey/babe", nos quedamos solo con la primera o limpiamos
                    if "/" in result_text:
                        result_text = result_text.split("/")[0].strip()
                        
                return lang, result_text, explanation

            except Exception as e:
                print(f"    [AVISO] El modelo {modelo} falló. (Causa: {e})")
                continue
                
        return "es", f"[Error: Todos los modelos fallaron.] {text}", "NONE"
