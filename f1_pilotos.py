import json
import os

CAMINHO_JSON = "pilotos.json"

def carregar_pilotos():
    if not os.path.exists(CAMINHO_JSON):
        return {}
    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_pilotos(pilotos):
    with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
        json.dump(pilotos, f, indent=4, ensure_ascii=False)

def cadastrar_piloto(pilotos, dados):
    numero = dados["numero"]
    if numero in pilotos:
        return False
    pilotos[numero] = dados
    salvar_pilotos(pilotos)
    return True

def buscar_piloto(pilotos, numero):
    return pilotos.get(numero)

def atualizar_piloto(pilotos, numero, novos_dados):
    if numero not in pilotos:
        return False
    pilotos[numero].update(novos_dados)
    salvar_pilotos(pilotos)
    return True

def excluir_piloto(pilotos, numero):
    if numero in pilotos:
        del pilotos[numero]
        salvar_pilotos(pilotos)
        return True
    return False

# ========== Estatísticas e Relatórios ==========

def piloto_com_mais_titulos(pilotos):
    return max(pilotos.values(), key=lambda p: p["titulos"])

def piloto_com_mais_vitorias(pilotos):
    return max(pilotos.values(), key=lambda p: p["estatisticas"]["vitorias"])

def media_vitorias(pilotos):
    total = sum(p["estatisticas"]["vitorias"] for p in pilotos.values())
    return total / len(pilotos) if pilotos else 0

def equipes_por_piloto(pilotos):
    return {p["nome"]: len(p["historico_equipes"]) for p in pilotos.values()}
