class Lenda:
    def __init__(self, nome, nacionalidade, titulos, vitorias, poles, podios, anos_ativo, equipes_principais, bio=None):
        self.nome = nome
        self.nacionalidade = nacionalidade
        self.titulos = titulos
        self.vitorias = vitorias
        self.poles = poles
        self.podios = podios
        self.anos_ativo = anos_ativo
        self.equipes_principais = equipes_principais
        self.bio = bio

    def to_dict(self):
        return {
            "nome": self.nome,
            "nacionalidade": self.nacionalidade,
            "titulos": self.titulos,
            "vitorias": self.vitorias,
            "poles": self.poles,
            "podios": self.podios,
            "anos_ativo": self.anos_ativo,
            "equipes_principais": self.equipes_principais,
            "bio": self.bio
        }

    @staticmethod
    def from_dict(data):
        return Lenda(
            nome=data.get("nome"),
            nacionalidade=data.get("nacionalidade"),
            titulos=data.get("titulos"),
            vitorias=data.get("vitorias"),
            poles=data.get("poles"),
            podios=data.get("podios"),
            anos_ativo=data.get("anos_ativo"),
            equipes_principais=data.get("equipes_principais"),
            bio=data.get("bio")
        ) 