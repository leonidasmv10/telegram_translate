# Telegram Magic Send - Traductor & Tutor de Inglés

Este proyecto convierte tu cuenta de Telegram en una herramienta de aprendizaje de idiomas en tiempo real.

## 🌟 Funcionalidades Principales
1. **Magic Send (Interceptor):** Escribe en español en el chat de tu novia desde tu App de Telegram normal; el bot borrará tu mensaje y enviará la traducción al inglés al instante.
2. **Auto-Corrección:** Si escribes en inglés, el bot corregirá tu ortografía y gramática antes de que ella lo lea.
3. **Registro de Aprendizaje:** 
   - `learning_history.csv`: Historial de frases para tus Flashcards.
   - `grammar_lessons.txt`: Explicaciones detalladas de por qué te equivocaste al escribir en inglés.
4. **Multi-Modelo Gratis (OpenRouter):** Conectado a Llama 3.3, Gemma 3, Mistral y Qwen. ¡Cero costo de tokens!

## 🛠️ Configuración Rápida
1. **Instalar dependencias:**
   ```cmd
   pip install -r requirements.txt
   ```
2. **Configura tu `config.ini`:**
   - Pon tu `api_id` y `api_hash` de Telegram.
   - Pon tu número de móvil con código de país.
   - Pon el `@username` de tu pareja en `target_chat_id`.
   - Pega tu API Key de [OpenRouter.ai](https://openrouter.ai/).

3. **Iniciar (Primera vez):**
   - Ejecuta `start.bat`. 
   - La primera vez te pedirá el código de Telegram en la consola para crear el archivo `mi_sesion.session`.

4. **Uso Diario:**
   - Solo abre `start.bat` y déjalo minimizado. ¡Chatea normal en Telegram y disfruta!

---
*Desarrollado para aprendizaje de idiomas en pareja.*
