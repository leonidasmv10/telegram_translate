import csv
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, filename="learning_history.csv"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Crea el CSV con la estructura correcta la primera vez."""
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Creamos las cabeceras ideales para Anki / Flashcards
                writer.writerow(["Fecha", "Español", "Inglés"])

    def record_phrase(self, spanish: str, english: str):
        """Guarda una frase en el diccionario para estudiar más tarde."""
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([date_str, spanish, english])
