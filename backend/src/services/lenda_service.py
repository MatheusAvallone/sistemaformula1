import json
from src.models.lenda import Lenda

class LendaService:
    def __init__(self):
        self.lendas = []
        self._load_lendas()

    def _load_lendas(self):
        try:
            with open('data/lendas.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.lendas = [Lenda.from_dict(lenda) for lenda in data]
        except FileNotFoundError:
            self.lendas = []

    def _save_lendas(self):
        data = [lenda.to_dict() for lenda in self.lendas]
        with open('data/lendas.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_all_lendas(self):
        return self.lendas

    def get_lenda_by_nome(self, nome):
        return next((l for l in self.lendas if l.nome.lower() == nome.lower()), None)

    def add_lenda(self, lenda_data):
        lenda = Lenda.from_dict(lenda_data)
        if not self.get_lenda_by_nome(lenda.nome):
            self.lendas.append(lenda)
            self._save_lendas()
            return lenda
        return None

    def update_lenda(self, nome, lenda_data):
        lenda = self.get_lenda_by_nome(nome)
        if lenda:
            lenda.__dict__.update(lenda_data)
            self._save_lendas()
            return lenda
        return None

    def delete_lenda(self, nome):
        lenda = self.get_lenda_by_nome(nome)
        if lenda:
            self.lendas.remove(lenda)
            self._save_lendas()
            return True
        return False 