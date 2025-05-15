import json
from src.models.circuito import Circuito

class CircuitoService:
    def __init__(self):
        self.circuitos = []
        self._load_circuitos()

    def _load_circuitos(self):
        try:
            with open('data/circuitos.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.circuitos = [Circuito.from_dict(circuito) for circuito in data['circuitos']]
        except FileNotFoundError:
            self.circuitos = []

    def _save_circuitos(self):
        data = {'circuitos': [circuito.to_dict() for circuito in self.circuitos]}
        with open('data/circuitos.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_all_circuitos(self):
        return self.circuitos

    def get_circuito_by_nome(self, nome):
        return next((c for c in self.circuitos if c.nome.lower() == nome.lower()), None)

    def add_circuito(self, circuito_data):
        circuito = Circuito.from_dict(circuito_data)
        if not self.get_circuito_by_nome(circuito.nome):
            self.circuitos.append(circuito)
            self._save_circuitos()
            return circuito
        return None

    def update_circuito(self, nome, circuito_data):
        circuito = self.get_circuito_by_nome(nome)
        if circuito:
            circuito.__dict__.update(circuito_data)
            self._save_circuitos()
            return circuito
        return None

    def delete_circuito(self, nome):
        circuito = self.get_circuito_by_nome(nome)
        if circuito:
            self.circuitos.remove(circuito)
            self._save_circuitos()
            return True
        return False 