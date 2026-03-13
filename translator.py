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
        
        # Le decimos a la IA cómo queremos que traduzca con tu estilo personal
        self.system_instruction = (
            "You are a strictly literal and minimalist translator for a private chat.\n"
            "STRICT RULES:\n"
            "1. NO ADDITIONS: Do not add emojis, extra sentences, or 'cool' expressions that were not in the original text (like 'Seriously crying rn' or 'What the heck').\n"
            "2. WORD-FOR-WORD FEEL: Translate exactly what the user wrote. If they wrote 3 words, you send 3 words.\n"
            "3. MAINTAIN EMOTIONS: If the user writes 'ohhh' or 'valeee', keep those exact words or their literal direct equivalent with the same number of letters.\n"
            "4. KEEP ROMANTIC TERMS: Leave 'mi amor', 'mi vida', 'mi reina', 'bebe' as they are, in Spanish. Do not change them to 'babe' or 'honey'.\n"
            "5. NO FILLER: Your output must be the clean translation. No robotic introductions, just the text.\n\n"
            "IMPORTANT: Your response MUST be exactly in this format on three lines:\n"
            "LANG:es (if original was Spanish) or LANG:en (if original was English)\n"
            "TEXT:<result>\n"
            "EXPLANATION:<grammar explanation in Spanish if the user made mistakes writing in English, otherwise NONE>"
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
                
                # Parsear el formato "LANG:xx \n TEXT:yy \n EXPLANATION:zz"
                lang = "es"
                result_text = output
                explanation = "NONE"
                
                lines = [line.strip() for line in output.split('\n') if line.strip()]
                for line in lines:
                    if line.upper().startswith("LANG:"):
                        lang = line.split(":", 1)[1].strip().lower()
                    elif line.upper().startswith("TEXT:"):
                        result_text = line.split(":", 1)[1].strip()
                    elif line.upper().startswith("EXPLANATION:"):
                        explanation = line.split(":", 1)[1].strip()
                        
                # Caso de borde por si no respetó el formato
                if result_text == output and len(lines) > 0 and not lines[0].upper().startswith("LANG:"):
                    result_text = lines[0]
                        
                return lang, result_text, explanation

            except Exception as e:
                print(f"    [AVISO] El modelo {modelo} falló. (Causa: {e})")
                continue
                
        return "es", f"[Error: Todos los modelos fallaron.] {text}", "NONE"
