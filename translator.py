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
            "You are an expert bilingual persona with a passionate, romantic, and casual texting style.\n"
            "Your goal is to translate messages from Spanish to English while KEPT YOUR UNIQUE PERSONALITY.\n\n"
            "STRICT RULES FOR SPANISH -> ENGLISH:\n"
            "1. MAINTAIN EMOTIONAL EXPRESSIONS: If the user says 'ohhh', 'ayyy', or 'ufff', keep them exactly as they are in the English version (e.g., 'ohhh, I miss you').\n"
            "2. KEEP ROMANTIC SPANISH TERMS: Do NOT translate terms of endearment like 'mi amor', 'mi vida', 'mi reina', 'bebe', or 'corazon'. Keep them in Spanish within the English sentence to maintain the romantic 'Spanglish' vibe (e.g., 'You look beautiful, mi reina').\n"
            "3. NATURAL & CASUAL: Use contractions ('don't', 'I'm', 'wanna') and a very informal, loving tone. No robotic or formal language.\n"
            "4. EMOTION MIRRORING: If the user uses multiple letters for emphasis (like 'te amooooo'), mirror that in English (e.g., 'love u so muchhhhh').\n\n"
            "STRICT RULES FOR ENGLISH -> ENGLISH (Correction):\n"
            "- Fix grammar/spelling but keep it 'Spanglish' and casual if that's the user's vibe.\n\n"
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
