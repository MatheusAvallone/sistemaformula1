class Piloto:
    def __init__(self, nome, equipe, numero, pontos=0, vitorias=0, poles=0):
        self.nome = nome
        self.equipe = equipe
        self.numero = numero
        self.pontos = pontos
        self.vitorias = vitorias
        self.poles = poles

    def to_dict(self):
        return {
            "nome": self.nome,
            "equipe": self.equipe,
            "numero": self.numero,
            "pontos": self.pontos,
            "vitorias": self.vitorias,
            "poles": self.poles
        }

    @staticmethod
    def from_dict(data):
        return Piloto(
            nome=data.get("nome"),
            equipe=data.get("equipe"),
            numero=data.get("numero"),
            pontos=data.get("pontos", 0),
            vitorias=data.get("vitorias", 0),
            poles=data.get("poles", 0)
        ) 