import tkinter as tk
from tkinter import ttk
from f1_pilotos import *
from PIL import Image, ImageTk, ImageOps
import os
import ttkbootstrap as ttkb
import unicodedata

# ========== Cores F1 ==========
COR_FUNDO = "#111111"
COR_TEXTO = "#ffffff"
COR_BOTAO = "#e60000"
COR_BOTAO_HOVER = "#c20000"
COR_CAIXA = "#333333"
COR_BORDA = "#666666"

# ========== Tooltip ==========
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 30
        y += self.widget.winfo_rooty() + cy
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.configure(bg="black")
        label = tk.Label(tw, text=self.text, bg="black", fg="white",
                         relief="solid", borderwidth=1, font=("Arial", 10))
        label.pack(ipadx=6, ipady=2)
        tw.wm_geometry(f"+{x}+{y}")

    def hide(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

# ========== Funções ==========
def limpar_conteudo():
    for widget in conteudo_frame.winfo_children():
        widget.destroy()

def mostrar_mensagem_boas_vindas():
    limpar_conteudo()
    label = tk.Label(conteudo_frame, text=" 🏎 Seja Bem-Vindo ao Sistema de Fórmula 1 2025 🏎 ",
                     font=("Arial", 20, "bold"), bg=COR_FUNDO, fg=COR_TEXTO)
    label.pack(expand=True)

def listar_pilotos():
    limpar_conteudo()
    pilotos = carregar_pilotos()

    canvas = tk.Canvas(conteudo_frame, bg=COR_FUNDO, highlightthickness=0)
    scrollbar = ttk.Scrollbar(conteudo_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=COR_FUNDO)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for numero, piloto in sorted(pilotos.items(), key=lambda x: int(x[0])):
        frame_piloto = tk.Frame(scroll_frame, bg=COR_CAIXA, bd=2, relief="solid", borderwidth=2)
        frame_piloto.pack(fill="x", pady=6, padx=10)

        info_label = tk.Label(frame_piloto, text=f"{piloto['numero']} - {piloto['nome']}",
                              font=("Arial", 14, "bold"), bg=COR_CAIXA, fg=COR_TEXTO, anchor="w", width=35)
        info_label.grid(row=0, column=0, sticky="w")

        equipe_label = tk.Label(frame_piloto, text=f"Equipe: {piloto['equipe']}", font=("Arial", 14),
                                bg=COR_CAIXA, fg=COR_TEXTO, anchor="w", width=25)
        equipe_label.grid(row=0, column=1, padx=10, sticky="w")

        botao_det = tk.Button(frame_piloto, text="Detalhes", command=lambda numero=numero: mostrar_detalhes(numero),
                              bg=COR_BOTAO, fg=COR_TEXTO, activebackground=COR_BOTAO_HOVER, cursor="hand2")
        botao_det.grid(row=0, column=2, padx=10)
        ToolTip(botao_det, "Ver detalhes do piloto")

        botao_edit = tk.Button(frame_piloto, text="Editar", command=lambda numero=numero: editar_piloto(numero),
                               bg=COR_BOTAO, fg=COR_TEXTO, activebackground=COR_BOTAO_HOVER, cursor="hand2")
        botao_edit.grid(row=0, column=3, padx=10)
        ToolTip(botao_edit, "Editar dados do piloto")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def mostrar_detalhes(numero, frame_destino=None, mostrar_voltar=True):
    pilotos = carregar_pilotos()
    piloto = pilotos.get(numero)
    if piloto:
        if not frame_destino:
            limpar_conteudo()
            frame_destino = conteudo_frame
        else:
            for widget in frame_destino.winfo_children():
                widget.destroy()

        box_frame = tk.Frame(frame_destino, bg=COR_CAIXA, padx=20, pady=20, bd=2, relief="groove", borderwidth=3)
        box_frame.pack(pady=20, padx=20)

        imagem_frame = tk.Frame(box_frame, bg=COR_CAIXA)
        imagem_frame.grid(row=0, column=0, padx=10, sticky="n")

        caminho_imagem = f"C:/Users/Matheus/Documents/PROJETOS/fotos_pilotos/{numero}.jpg"
        if os.path.exists(caminho_imagem):
            try:
                img = Image.open(caminho_imagem)
                img = ImageOps.fit(img, (250, 250), method=Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                imagem_label = tk.Label(imagem_frame, image=img_tk, bg=COR_CAIXA)
                imagem_label.image = img_tk
                imagem_label.pack()
            except Exception as e:
                print(f"Erro ao carregar imagem: {e}")
        else:
            print("Imagem não encontrada.")

        texto_frame = tk.Frame(box_frame, bg=COR_CAIXA)
        texto_frame.grid(row=0, column=1, sticky="nw", padx=15)

        labels_info = [
            ("Nome", piloto['nome']),
            ("Número", piloto['numero']),
            ("Nacionalidade", piloto['nacionalidade']),
            ("Equipe Atual", piloto['equipe']),
            ("Títulos", piloto['titulos']),
            ("Corridas", piloto['estatisticas']['corridas']),
            ("Vitórias", piloto['estatisticas']['vitorias']),
            ("Pódios", piloto['estatisticas']['podios']),
            ("Poles", piloto['estatisticas']['poles']),
            ("Voltas Mais Rápidas", piloto['estatisticas']['voltas_mais_rapidas']),
            ("Histórico de Equipes", ', '.join(piloto['historico_equipes'])),
        ]

        for idx, (titulo, valor) in enumerate(labels_info):
            label_titulo = tk.Label(texto_frame, text=f"{titulo}:", font=("Arial", 12, "bold"),
                                    bg=COR_CAIXA, fg=COR_TEXTO, anchor="w")
            label_titulo.grid(row=idx, column=0, sticky="w", pady=5)

            label_valor = tk.Label(texto_frame, text=valor, font=("Arial", 12),
                                   bg=COR_CAIXA, fg=COR_TEXTO, anchor="w")
            label_valor.grid(row=idx, column=1, sticky="w", pady=5)

        if mostrar_voltar:
            botao_voltar = tk.Button(frame_destino, text="Voltar", command=listar_pilotos,
                                     bg=COR_BOTAO, fg=COR_TEXTO, activebackground=COR_BOTAO,
                                     activeforeground=COR_TEXTO)
            botao_voltar.pack(pady=10)

def editar_piloto(numero):
    limpar_conteudo()
    pilotos = carregar_pilotos()
    piloto = pilotos.get(numero)

    if not piloto:
        return

    frame = tk.Frame(conteudo_frame, bg=COR_CAIXA, padx=20, pady=20)
    frame.pack(pady=20)

    entradas = {}

    def criar_entrada(label_texto, chave, valor_inicial):
        label = tk.Label(frame, text=label_texto, bg=COR_CAIXA, fg=COR_TEXTO, font=("Arial", 12))
        label.pack(anchor="w", pady=2)
        entrada = tk.Entry(frame, font=("Arial", 12))
        entrada.insert(0, str(valor_inicial))
        entrada.pack(fill="x", pady=2)
        entradas[chave] = entrada

    criar_entrada("Nome", "nome", piloto["nome"])
    criar_entrada("Nacionalidade", "nacionalidade", piloto["nacionalidade"])
    criar_entrada("Equipe Atual", "equipe", piloto["equipe"])
    criar_entrada("Títulos", "titulos", piloto["titulos"])

    est = piloto["estatisticas"]
    for stat in ["corridas", "vitorias", "podios", "poles", "voltas_mais_rapidas"]:
        criar_entrada(stat.capitalize(), f"estatisticas.{stat}", est[stat])

    criar_entrada("Histórico de Equipes (separado por vírgulas)", "historico_equipes", ', '.join(piloto["historico_equipes"]))

    def salvar_edicao():
        novos_dados = {
            "nome": entradas["nome"].get(),
            "nacionalidade": entradas["nacionalidade"].get(),
            "equipe": entradas["equipe"].get(),
            "titulos": int(entradas["titulos"].get()),
            "estatisticas": {
                "corridas": int(entradas["estatisticas.corridas"].get()),
                "vitorias": int(entradas["estatisticas.vitorias"].get()),
                "podios": int(entradas["estatisticas.podios"].get()),
                "poles": int(entradas["estatisticas.poles"].get()),
                "voltas_mais_rapidas": int(entradas["estatisticas.voltas_mais_rapidas"].get()),
            },
            "historico_equipes": [e.strip() for e in entradas["historico_equipes"].get().split(",")]
        }
        atualizar_piloto(pilotos, numero, novos_dados)
        listar_pilotos()

    botao_salvar = tk.Button(frame, text="Salvar", command=salvar_edicao,
                             bg=COR_BOTAO, fg=COR_TEXTO, activebackground=COR_BOTAO_HOVER)
    botao_salvar.pack(pady=10)

    botao_cancelar = tk.Button(frame, text="Cancelar", command=listar_pilotos,
                               bg=COR_BOTAO, fg=COR_TEXTO)
    botao_cancelar.pack()

def buscar_por_numero():
    limpar_conteudo()
    entrada_frame = tk.Frame(conteudo_frame, bg=COR_FUNDO)
    entrada_frame.pack(pady=10)

    entrada_numero = tk.Entry(entrada_frame, font=("Arial", 12), width=10)
    entrada_numero.pack(side="left", padx=5)

    resultado_frame = tk.Frame(conteudo_frame, bg=COR_FUNDO)
    resultado_frame.pack(pady=10)

    def buscar():
        numero = entrada_numero.get()
        pilotos = carregar_pilotos()
        piloto = buscar_piloto(pilotos, numero)
        if piloto:
            mostrar_detalhes(numero, frame_destino=resultado_frame)
        else:
            for widget in resultado_frame.winfo_children():
                widget.destroy()
            msg = tk.Label(resultado_frame, text="Piloto não encontrado.", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 12))
            msg.pack()

    botao_buscar = tk.Button(entrada_frame, text="Buscar", command=buscar,
                             bg=COR_BOTAO, fg=COR_TEXTO, activebackground=COR_BOTAO_HOVER, cursor="hand2")
    botao_buscar.pack(side="left", padx=5)

def mostrar_pistas():
    # Criando a janela principal para exibir a lista de pistas
    pistas_window = tk.Toplevel(root)
    pistas_window.title("Pistas de F1 2025")
    pistas_window.geometry('400x600')
    
    # Criando a lista de pistas com botões de "Detalhes"
    for pista in pistas_2025:
        frame = ttk.Frame(pistas_window)
        frame.pack(pady=10)
        
        # Exibindo o nome da pista
        pista_label = tk.Label(frame, text=pista['nome'], font=("Arial", 12))
        pista_label.pack(side=tk.LEFT, padx=10)
        
        # Botão para mostrar os detalhes da pista
        detalhes_button = ttk.Button(frame, text="Detalhes", command=lambda p=pista: mostrar_detalhes_pista(p))
        detalhes_button.pack(side=tk.LEFT)
    pistas = [
        {"nome": "Bahrein", "circuito": "Sakhir"},
        {"nome": "Arábia Saudita", "circuito": "Jeddah"},
        {"nome": "Austrália", "circuito": "Melbourne"},
        {"nome": "Japão", "circuito": "Suzuka"},
        {"nome": "China", "circuito": "Xangai"},
        {"nome": "Miami", "circuito": "EUA"},
        {"nome": "Espanha", "circuito": "Barcelona"},
        {"nome": "Mônaco", "circuito": "Monte Carlo"},
        {"nome": "Canadá", "circuito": "Montreal"},
        {"nome": "Áustria", "circuito": "Red Bull Ring"},
        {"nome": "Reino Unido", "circuito": "Silverstone"},
        {"nome": "Hungria", "circuito": "Hungaroring"},
        {"nome": "Bélgica", "circuito": "Spa-Francorchamps"},
        {"nome": "Países Baixos", "circuito": "Zandvoort"},
        {"nome": "Itália", "circuito": "Monza"},
        {"nome": "Singapura", "circuito": "Marina Bay"},
        {"nome": "EUA", "circuito": "Austin"},
        {"nome": "México", "circuito": "Hermanos Rodríguez"},
        {"nome": "Brasil", "circuito": "Interlagos"},
        {"nome": "Las Vegas", "circuito": "Strip Circuit"},
        {"nome": "Abu Dhabi", "circuito": "Yas Marina"},
    ]

    for idx, pista in enumerate(pistas):
        frame_pista = tk.Frame(scroll_frame, bg=COR_CAIXA, bd=2, relief="solid", borderwidth=2)
        frame_pista.pack(fill="x", pady=6, padx=10)

        info_label = tk.Label(frame_pista, text=f"{pista['nome']}", font=("Arial", 14, "bold"),
                              bg=COR_CAIXA, fg=COR_TEXTO, anchor="w", width=30)
        info_label.grid(row=0, column=0, sticky="w", padx=5)

        circuito_label = tk.Label(frame_pista, text=f"Circuito: {pista['circuito']}", font=("Arial", 14),
                                  bg=COR_CAIXA, fg=COR_TEXTO, anchor="w", width=30)
        circuito_label.grid(row=0, column=1, padx=5)

        botao_det = tk.Button(frame_pista, text="Detalhes", 
                              command=lambda p=pista: mostrar_detalhes_pista(p),
                              bg=COR_BOTAO, fg=COR_TEXTO, activebackground=COR_BOTAO_HOVER, cursor="hand2")
        botao_det.grid(row=0, column=2, padx=10)

        ToolTip(botao_det, "Ver detalhes da pista")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# Dicionário com as pistas e seus respectivos arquivos de imagem

imagens_pistas = {
    "Bahrein": "bahrein.png",
    "Arábia Saudita": "jeddah.png",
    "Austrália": "australia.png",
    "Japão": "japao.png",
    "China": "china.png",
    "Miami": "miami.png",
    "Espanha": "espanha.png",
    "Mônaco": "monaco.png",
    "Canadá": "canada.png",
    "Áustria": "austria.png",
    "Reino Unido": "silverstone.png",
    "Hungria": "hungria.png",
    "Bélgica": "belgica.png",
    "Países Baixos": "holanda.png",
    "Itália": "italia.png",
    "Singapura": "singapura.png",
    "EUA": "austin.png",
    "México": "mexico.png",
    "Brasil": "brasil.png",
    "Las Vegas": "vegas.png",
    "Abu Dhabi": "dhabi.png",
}

pistas_2025 = [
    {
        "nome": "Circuito de Mônaco",
        "pais": "Mônaco",
        "cidade": "Monte Carlo",
        "tipo": "Urbano",
        "extensao_km": 3.337,
        "voltas": 78,
        "distancia_total_km": 260.286,
        "capacidade": "37.000",
        "recorde": "1:14.260 (Max Verstappen - 2023)",
        "ano_inauguracao": 1929,
        "imagem": "imagens/monaco.png"
    },
    {
        "nome": "Circuito de Silverstone",
        "pais": "Reino Unido",
        "cidade": "Silverstone",
        "tipo": "Mistura (velocidade e técnica)",
        "extensao_km": 5.891,
        "voltas": 52,
        "distancia_total_km": 306.198,
        "capacidade": "150.000",
        "recorde": "1:27.097 (Max Verstappen - 2021)",
        "ano_inauguracao": 1948,
        "imagem": "imagens/silverstone.png"
    },
    {
        "nome": "Circuito de Suzuka",
        "pais": "Japão",
        "cidade": "Suzuka",
        "tipo": "Mistura",
        "extensao_km": 5.807,
        "voltas": 53,
        "distancia_total_km": 306.541,
        "capacidade": "155.000",
        "recorde": "1:31.540 (Michael Schumacher - 2003)",
        "ano_inauguracao": 1962,
        "imagem": "imagens/suzuka.png"
    },
    {
        "nome": "Circuito de Monza",
        "pais": "Itália",
        "cidade": "Monza",
        "tipo": "Velocidade pura",
        "extensao_km": 5.793,
        "voltas": 53,
        "distancia_total_km": 306.72,
        "capacidade": "120.000",
        "recorde": "1:19.119 (Lewis Hamilton - 2020)",
        "ano_inauguracao": 1922,
        "imagem": "imagens/monza.png"
    },
    {
        "nome": "Circuito de Interlagos",
        "pais": "Brasil",
        "cidade": "São Paulo",
        "tipo": "Mistura de velocidade e técnica",
        "extensao_km": 4.309,
        "voltas": 71,
        "distancia_total_km": 305.909,
        "capacidade": "150.000",
        "recorde": "1:10.540 (Lewis Hamilton - 2019)",
        "ano_inauguracao": 1990,
        "imagem": "imagens/interlagos.png"
    },
    {
        "nome": "Circuito de Spa-Francorchamps",
        "pais": "Bélgica",
        "cidade": "Spa",
        "tipo": "Mistura",
        "extensao_km": 7.004,
        "voltas": 44,
        "distancia_total_km": 308.052,
        "capacidade": "70.000",
        "recorde": "1:46.286 (Lewis Hamilton - 2020)",
        "ano_inauguracao": 1921,
        "imagem": "imagens/spa.png"
    },
    {
        "nome": "Circuito de Barcelona-Catalunha",
        "pais": "Espanha",
        "cidade": "Montmelo",
        "tipo": "Mistura",
        "extensao_km": 4.675,
        "voltas": 66,
        "distancia_total_km": 308.424,
        "capacidade": "140.000",
        "recorde": "1:18.149 (Max Verstappen - 2021)",
        "ano_inauguracao": 1991,
        "imagem": "imagens/barcelona.png"
    },
    {
        "nome": "Circuito de Zandvoort",
        "pais": "Países Baixos",
        "cidade": "Zandvoort",
        "tipo": "Mistura",
        "extensao_km": 4.259,
        "voltas": 72,
        "distancia_total_km": 306.587,
        "capacidade": "105.000",
        "recorde": "1:08.215 (Max Verstappen - 2021)",
        "ano_inauguracao": 1952,
        "imagem": "imagens/zandvoort.png"
    },
    {
        "nome": "Circuito de Baku",
        "pais": "Azerbaijão",
        "cidade": "Baku",
        "tipo": "Urbano",
        "extensao_km": 6.003,
        "voltas": 51,
        "distancia_total_km": 306.049,
        "capacidade": "50.000",
        "recorde": "1:43.009 (Valtteri Bottas - 2019)",
        "ano_inauguracao": 2016,
        "imagem": "imagens/baku.png"
    },
    {
        "nome": "Circuito de Las Vegas",
        "pais": "Estados Unidos",
        "cidade": "Las Vegas",
        "tipo": "Urbano",
        "extensao_km": 6.120,
        "voltas": 50,
        "distancia_total_km": 306.0,
        "capacidade": "170.000",
        "recorde": "Ainda não disponível",
        "ano_inauguracao": 2023,
        "imagem": "imagens/lasvegas.png"
    },
    {
        "nome": "Circuito de Jeddah",
        "pais": "Arábia Saudita",
        "cidade": "Jeddah",
        "tipo": "Urbano",
        "extensao_km": 6.174,
        "voltas": 50,
        "distancia_total_km": 308.7,
        "capacidade": "50.000",
        "recorde": "1:27.511 (Max Verstappen - 2021)",
        "ano_inauguracao": 2021,
        "imagem": "imagens/jeddah.png"
    },
    {
        "nome": "Circuito de Melbourne",
        "pais": "Austrália",
        "cidade": "Melbourne",
        "tipo": "Mistura",
        "extensao_km": 5.278,
        "voltas": 58,
        "distancia_total_km": 318.569,
        "capacidade": "120.000",
        "recorde": "1:20.260 (Charles Leclerc - 2019)",
        "ano_inauguracao": 1996,
        "imagem": "imagens/melbourne.png"
    },
    {
        "nome": "Circuito de Miami",
        "pais": "Estados Unidos",
        "cidade": "Miami",
        "tipo": "Urbano",
        "extensao_km": 5.412,
        "voltas": 57,
        "distancia_total_km": 308.326,
        "capacidade": "90.000",
        "recorde": "1:31.097 (Max Verstappen - 2022)",
        "ano_inauguracao": 2022,
        "imagem": "imagens/miami.png"
    },
    {
        "nome": "Circuito de Cingapura",
        "pais": "Cingapura",
        "cidade": "Cingapura",
        "tipo": "Urbano",
        "extensao_km": 5.063,
        "voltas": 61,
        "distancia_total_km": 308.706,
        "capacidade": "85.000",
        "recorde": "1:41.905 (Sebastian Vettel - 2019)",
        "ano_inauguracao": 2008,
        "imagem": "imagens/cingapura.png"
    },
    {
        "nome": "Circuito de Austin",
        "pais": "Estados Unidos",
        "cidade": "Austin",
        "tipo": "Mistura",
        "extensao_km": 5.513,
        "voltas": 56,
        "distancia_total_km": 308.405,
        "capacidade": "120.000",
        "recorde": "1:36.169 (Max Verstappen - 2021)",
        "ano_inauguracao": 2012,
        "imagem": "imagens/austin.png"
    },
    {
        "nome": "Circuito de Losail",
        "pais": "Catar",
        "cidade": "Losail",
        "tipo": "Mistura",
        "extensao_km": 5.380,
        "voltas": 57,
        "distancia_total_km": 306.684,
        "capacidade": "40.000",
        "recorde": "1:23.776 (Valtteri Bottas - 2020)",
        "ano_inauguracao": 2004,
        "imagem": "imagens/losail.png"
    }
]


def mostrar_detalhes_pista(pista):
    # Criação de uma nova janela para mostrar os detalhes da pista
    detalhes_window = tk.Toplevel(root)
    detalhes_window.title(pista['nome'])
    detalhes_window.geometry('500x600')
    
    # Exibindo a imagem da pista
    try:
        imagem_pista = Image.open(pista['imagem'])
        imagem_pista = imagem_pista.resize((300, 200))
        imagem_pista = ImageTk.PhotoImage(imagem_pista)
        imagem_label = tk.Label(detalhes_window, image=imagem_pista)
        imagem_label.image = imagem_pista
        imagem_label.pack(pady=10)
    except:
        pass
    
    # Exibindo as informações adicionais
    tk.Label(detalhes_window, text=f"Nome: {pista['nome']}", font=("Arial", 12)).pack(pady=5)
    tk.Label(detalhes_window, text=f"País: {pista['pais']}", font=("Arial", 12)).pack(pady=5)
    tk.Label(detalhes_window, text=f"Cidade: {pista['cidade']}", font=("Arial", 12)).pack(pady=5)
    tk.Label(detalhes_window, text=f"Tipo: {pista['tipo']}", font=("Arial", 12)).pack(pady=5)
    tk.Label(detalhes_window, text=f"Extensão: {pista['extensao_km']} km", font=("Arial", 12)).pack(pady=5)
    tk.Label(detalhes_window, text=f"Voltas: {pista['voltas']}", font=("Arial", 12)).pack(pady=5)
    tk.Label(detalhes_window, text=f"Distância total: {pista['distancia_total_km']} km", font=("Arial", 12)).pack(pady=5)
    tk.Label(detalhes_window, text=f"Capacidade: {pista['capacidade']}", font=("Arial", 12)).pack(pady=5)
    tk.Label(detalhes_window, text=f"Recorde: {pista['recorde']}", font=("Arial", 12)).pack(pady=5)
    tk.Label(detalhes_window, text=f"Ano de Inauguração: {pista['ano_inauguracao']}", font=("Arial", 12)).pack(pady=5)

    # ========== Função para Lendas da Fórmula 1 ==========

import os
from PIL import Image, ImageTk

def mostrar_lendas():
    limpar_conteudo()

    # Criação de uma área com rolagem mais eficaz
    canvas = tk.Canvas(conteudo_frame)
    scrollbar = tk.Scrollbar(conteudo_frame, orient="vertical", command=canvas.yview)
    frame_scroll = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Posicionar a barra de rolagem à direita
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Atualiza a área de rolagem
    frame_scroll.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    # Título
    label_titulo = tk.Label(frame_scroll, text="🏆 Lendas da Fórmula 1 🏆",
                            font=("Arial", 20, "bold"), bg=COR_FUNDO, fg=COR_TEXTO)
    label_titulo.pack(pady=10)
    
    # Lista de lendas com seus respectivos arquivos de imagem, informações e nacionalidade
    lendas = [
        {"nome": "Ayrton Senna", "imagem": "senna.png", "titulos": 3, "vitorias": 41, "anos_ativo": "1984–1994", "nacionalidade": "Brasileiro"},
        {"nome": "Michael Schumacher", "imagem": "schumacher.png", "titulos": 7, "vitorias": 91, "anos_ativo": "1991–2012", "nacionalidade": "Alemão"},
        {"nome": "Juan Manuel Fangio", "imagem": "fangio.png", "titulos": 5, "vitorias": 24, "anos_ativo": "1949–1951", "nacionalidade": "Argentino"},
        {"nome": "Alain Prost", "imagem": "prost.png", "titulos": 4, "vitorias": 51, "anos_ativo": "1980–1991", "nacionalidade": "Francês"},
        {"nome": "Nelson Piquet", "imagem": "piquet.png", "titulos": 3, "vitorias": 23, "anos_ativo": "1978–1991", "nacionalidade": "Brasileiro"}
    ]
    
    pasta_imagens = r"C:/Users/Matheus/Documents/PROJETOS/fotos_lendas"  # Caminho da pasta de imagens

    for lenda in lendas:
        # Criando o "cartão" com borda e fundo
        frame_lenda = tk.Frame(frame_scroll, bg=COR_FUNDO, bd=10, relief="solid", padx=20, pady=20)
        frame_lenda.pack(pady=20, fill="x", padx=50)  # Aumentando os espaços dos cartões

        # Tentativa de carregar a imagem
        try:
            caminho_img = os.path.join(pasta_imagens, lenda["imagem"])  # Caminho absoluto da imagem
            if os.path.exists(caminho_img):
                img = Image.open(caminho_img)
                img = img.resize((300, 300), Image.Resampling.LANCZOS)  # Imagem maior
                foto = ImageTk.PhotoImage(img)
                label_img = tk.Label(frame_lenda, image=foto, bg=COR_FUNDO)
                label_img.image = foto  # Mantendo a referência da imagem
                label_img.grid(row=0, column=0, rowspan=2, padx=10, pady=10)  # Posicionando a imagem
            else:
                print(f"Arquivo {caminho_img} não encontrado.")
        except Exception as e:
            print(f"Erro ao carregar imagem de {lenda['nome']}: {e}")

        # Nome do piloto
        label_nome = tk.Label(frame_lenda, text=lenda["nome"],
                              font=("Arial", 20, "bold"), bg=COR_FUNDO, fg=COR_TEXTO)
        label_nome.grid(row=0, column=1, sticky="w", padx=10, pady=10)  # Nome maior e mais destacado

        # Informações sobre o piloto
        info_text = f"Títulos: {lenda['titulos']}\nVitórias: {lenda['vitorias']}\nAnos Ativo: {lenda['anos_ativo']}\nNacionalidade: {lenda['nacionalidade']}"
        label_info = tk.Label(frame_lenda, text=info_text, 
                              font=("Arial", 14), bg=COR_FUNDO, fg="gray")
        label_info.grid(row=1, column=1, sticky="w", padx=10, pady=5)

    # Exemplo de atualização para aumentar o layout e melhorar a rolagem
    canvas.update_idletasks()  # Atualizar a interface do canvas para evitar distorções

def mostrar_titulos():
    for widget in conteudo_frame.winfo_children():
        widget.destroy()

    titulos_label = ttkb.Label(
        conteudo_frame,
        text="Campeões de Fórmula 1 (1950-2024)",
        font=("Arial", 20, "bold")  # Aumentei o tamanho da fonte
    )
    titulos_label.pack(pady=15)

    # Frame que segura a tabela
    tabela_frame = tk.Frame(conteudo_frame, bg=COR_FUNDO)
    tabela_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Scrollbar vertical
    scrollbar = ttk.Scrollbar(tabela_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Estilo com linhas visíveis e alternância de cor
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#1e1e1e",
                    foreground="white",
                    rowheight=58,  # Aumentei a altura da linha para acomodar o texto maior
                    fieldbackground="#1e1e1e",
                    borderwidth=0,
                    font=("Arial", 14))  # Aumentei o tamanho da fonte para os dados
    style.configure("Treeview.Heading",
                    background="#c0392b",
                    foreground="white",
                    font=("Arial", 16, "bold"))  # Aumentei o tamanho da fonte para os títulos das colunas
    style.map('Treeview', background=[('selected', '#c44536')])

    # Criando a tabela
    tabela = ttk.Treeview(
        tabela_frame,
        columns=("Nome", "Títulos"),
        show="headings",
        yscrollcommand=scrollbar.set,
        selectmode="none"
    )
    tabela.heading("Nome", text="Nome")
    tabela.heading("Títulos", text="Títulos")

    tabela.column("Nome", anchor="w", width=500)
    tabela.column("Títulos", anchor="center", width=300)

    tabela.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=tabela.yview)

    # Dados
    campeoes = [
        ("Giuseppe Farina", 1), ("Juan Manuel Fangio", 5), ("Alberto Ascari", 2), ("Mike Hawthorn", 1),
        ("Jack Brabham", 3), ("Phil Hill", 1), ("Graham Hill", 2), ("Jim Clark", 2), ("John Surtees", 1),
        ("Jackie Stewart", 3), ("Jochen Rindt", 1), ("Emerson Fittipaldi", 2), ("James Hunt", 1),
        ("Niki Lauda", 3), ("Nelson Piquet", 3), ("Alain Prost", 4), ("Ayrton Senna", 3), ("Michael Schumacher", 7),
        ("Mika Häkkinen", 2), ("Fernando Alonso", 2), ("Kimi Räikkönen", 1), ("Lewis Hamilton", 7),
        ("Sebastian Vettel", 4), ("Max Verstappen", 3)
    ]

    campeoes_ordenados = sorted(campeoes, key=lambda x: x[1], reverse=True)
    for i, (nome, titulos) in enumerate(campeoes_ordenados):
        tag = "linha_par" if i % 2 == 0 else "linha_impar"
        tabela.insert("", "end", values=(nome, titulos), tags=(tag,))

    tabela.tag_configure("linha_par", background="#2e2e2e")
    tabela.tag_configure("linha_impar", background="#333333")

    # Botão voltar
    voltar_button = ttkb.Button(
        conteudo_frame,
        text="Voltar",
        command=mostrar_mensagem_boas_vindas
    )
    voltar_button.pack(pady=20)

    import tkinter as tk
from tkinter import ttk
import random

def iniciar_quiz():
    for widget in conteudo_frame.winfo_children():
        widget.destroy()
    
    titulos_label = ttk.Label(
        conteudo_frame,
        text="Quiz de Fórmula 1",
        font=("Arial", 20, "bold")
    )
    titulos_label.pack(pady=15)

    # Lista de perguntas e respostas
    perguntas = [
        {
            "pergunta": "Quem foi o campeão de Fórmula 1 de 2020?",
            "respostas": ["Lewis Hamilton", "Max Verstappen", "Sebastian Vettel", "Valtteri Bottas"],
            "correta": "Lewis Hamilton"
        },
        {
            "pergunta": "Qual piloto tem mais títulos na história da F1?",
            "respostas": ["Juan Manuel Fangio", "Lewis Hamilton", "Michael Schumacher", "Ayrton Senna"],
            "correta": "Michael Schumacher"
        },
        {
            "pergunta": "Em que ano a Fórmula 1 foi criada?",
            "respostas": ["1945", "1950", "1965", "1970"],
            "correta": "1950"
        },
        {
            "pergunta": "Qual é o circuito mais longo da F1?",
            "respostas": ["Circuito de Mônaco", "Circuito de Spa-Francorchamps", "Circuito de Suzuka", "Circuito de Silverstone"],
            "correta": "Circuito de Spa-Francorchamps"
        },
        {
            "pergunta": "Quem é conhecido como o 'Rei de Mônaco'?",
            "respostas": ["Ayrton Senna", "Alain Prost", "Lewis Hamilton", "Niki Lauda"],
            "correta": "Ayrton Senna"
        }
    ]
    
    # Embaralha as perguntas para que sejam apresentadas de maneira aleatória
    random.shuffle(perguntas)
    
    # Variáveis globais para controle do quiz
    pontuacao = 0
    pergunta_atual = 0
    
    def verificar_resposta(resposta_selecionada):
        nonlocal pontuacao, pergunta_atual
        
        # Verifica se a resposta está correta
        if resposta_selecionada == perguntas[pergunta_atual]["correta"]:
            pontuacao += 1

        pergunta_atual += 1
        
        # Se ainda houver perguntas
        if pergunta_atual < len(perguntas):
            mostrar_pergunta(pergunta_atual)
        else:
            mostrar_resultado()
    
    def mostrar_pergunta(pergunta_index):
        # Limpa a tela de conteúdo
        for widget in conteudo_frame.winfo_children():
            widget.destroy()
        
        # Exibe a pergunta atual
        pergunta = perguntas[pergunta_index]["pergunta"]
        titulos_label = ttk.Label(conteudo_frame, text=pergunta, font=("Arial", 16, "bold"))
        titulos_label.pack(pady=15)

        # Exibe as alternativas
        respostas = perguntas[pergunta_index]["respostas"]
        for resposta in respostas:
            resposta_button = ttk.Button(conteudo_frame, text=resposta, width=30, command=lambda r=resposta: verificar_resposta(r))
            resposta_button.pack(pady=5)
    
    def mostrar_resultado():
        # Exibe a pontuação final
        for widget in conteudo_frame.winfo_children():
            widget.destroy()
        
        resultado_label = ttk.Label(
            conteudo_frame,
            text=f"Você acertou {pontuacao} de {len(perguntas)} perguntas!",
            font=("Arial", 18, "bold")
        )
        resultado_label.pack(pady=15)
        
        # Botão para voltar ao menu
        voltar_button = ttk.Button(
            conteudo_frame,
            text="Voltar",
            command=mostrar_mensagem_boas_vindas
        )
        voltar_button.pack(pady=20)
    
    # Começa o quiz mostrando a primeira pergunta
    mostrar_pergunta(pergunta_atual)

# ========== Janela Principal ==========
root = ttkb.Window(themename="cyborg")
root.title("Fórmula 1 - 2025")
root.geometry("960x600")
root.configure(bg=COR_FUNDO)

main_frame = tk.Frame(root, bg=COR_FUNDO)
main_frame.pack(fill="both", expand=True)

menu_frame = tk.Frame(main_frame, width=200, bg=COR_FUNDO)
menu_frame.pack(side="left", fill="y")

conteudo_frame = tk.Frame(main_frame, bg=COR_FUNDO)
conteudo_frame.pack(side="right", fill="both", expand=True)

botoes = [
    ("Listar Pilotos", listar_pilotos),
    ("Buscar por Número", buscar_por_numero),
    ("Pistas", mostrar_pistas),
    ("Lendas", mostrar_lendas),
    ("Títulos", mostrar_titulos),
    ("Iniciar Quiz", iniciar_quiz),
    ("Voltar ao Menu", mostrar_mensagem_boas_vindas),
   
]

for texto, comando in botoes:
    btn = tk.Button(menu_frame, text=texto, command=comando,
                    bg=COR_BOTAO, fg=COR_TEXTO, activebackground=COR_BOTAO_HOVER,
                    font=("Arial", 12, "bold"), width=20, cursor="hand2", relief="flat")
    btn.pack(pady=10, padx=10)
    ToolTip(btn, f"{texto}")

mostrar_mensagem_boas_vindas()
root.mainloop()
