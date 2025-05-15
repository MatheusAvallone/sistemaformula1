class Circuito:
    def __init__(self, nome, pais, cidade, comprimento, num_voltas, data_corrida, distancia_total=None, recorde_volta=None, primeiro_gp=None):
        self.nome = nome
        self.pais = pais
        self.cidade = cidade
        self.comprimento = comprimento  # em km
        self.num_voltas = num_voltas
        self.data_corrida = data_corrida
        self.distancia_total = distancia_total or (comprimento * num_voltas)
        self.recorde_volta = recorde_volta
        self.primeiro_gp = primeiro_gp

    def to_dict(self):
        return {
            "nome": self.nome,
            "pais": self.pais,
            "cidade": self.cidade,
            "comprimento": self.comprimento,
            "num_voltas": self.num_voltas,
            "data_corrida": self.data_corrida,
            "distancia_total": self.distancia_total,
            "recorde_volta": self.recorde_volta,
            "primeiro_gp": self.primeiro_gp
        }

    @staticmethod
    def from_dict(data):
        return Circuito(
            nome=data.get("nome"),
            pais=data.get("pais"),
            cidade=data.get("cidade"),
            comprimento=data.get("comprimento"),
            num_voltas=data.get("num_voltas"),
            data_corrida=data.get("data_corrida"),
            recorde_volta=data.get("recorde_volta"),
            primeiro_gp=data.get("primeiro_gp"),
            distancia_total=data.get("distancia_total")
        ) 