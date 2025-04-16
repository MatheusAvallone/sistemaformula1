import tkinter as tk
from tkinter import ttk
from f1_pilotos import *
from PIL import Image, ImageTk, ImageOps
import os
import ttkbootstrap as ttkb

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
    ("Voltar ao Menu", mostrar_mensagem_boas_vindas)
]

for texto, comando in botoes:
    btn = tk.Button(menu_frame, text=texto, command=comando,
                    bg=COR_BOTAO, fg=COR_TEXTO, activebackground=COR_BOTAO_HOVER,
                    font=("Arial", 12, "bold"), width=20, cursor="hand2", relief="flat")
    btn.pack(pady=10, padx=10)
    ToolTip(btn, f"{texto}")

mostrar_mensagem_boas_vindas()
root.mainloop()
