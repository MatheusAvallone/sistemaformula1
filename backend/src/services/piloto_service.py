import json
from src.models.piloto import Piloto

class PilotoService:
    def __init__(self):
        self.pilotos = []
        self._load_pilotos()

    def _load_pilotos(self):
        try:
            with open('data/pilotos.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.pilotos = [Piloto.from_dict(piloto) for piloto in data]
        except FileNotFoundError:
            self.pilotos = []

    def _save_pilotos(self):
        data = [piloto.to_dict() for piloto in self.pilotos]
        with open('data/pilotos.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_all_pilotos(self):
        return self.pilotos

    def get_piloto_by_numero(self, numero):
        return next((p for p in self.pilotos if p.numero == numero), None)

    def add_piloto(self, piloto_data):
        piloto = Piloto.from_dict(piloto_data)
        if not self.get_piloto_by_numero(piloto.numero):
            self.pilotos.append(piloto)
            self._save_pilotos()
            return piloto
        return None

    def update_piloto(self, numero, piloto_data):
        piloto = self.get_piloto_by_numero(numero)
        if piloto:
            piloto.__dict__.update(piloto_data)
            self._save_pilotos()
            return piloto
        return None

    def delete_piloto(self, numero):
        piloto = self.get_piloto_by_numero(numero)
        if piloto:
            self.pilotos.remove(piloto)
            self._save_pilotos()
            return True
        return False

    def atualizar_pontos(self, numero, pontos):
        piloto = self.get_piloto_by_numero(numero)
        if piloto:
            piloto.pontos += pontos
            self._save_pilotos()
            return piloto
        return None 