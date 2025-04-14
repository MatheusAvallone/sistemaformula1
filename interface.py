import tkinter as tk
from tkinter import messagebox
from f1_pilotos import (
    carregar_pilotos,
    salvar_pilotos,
    buscar_piloto,
    cadastrar_piloto,
    atualizar_piloto,
    excluir_piloto,
    piloto_com_mais_titulos,
    piloto_com_mais_vitorias,
    media_vitorias,
    equipes_por_piloto
)

def abrir_cadastro(): 
    def salvar():
        dados = {
            "numero": entradas["Número"].get(),
            "nome": entradas["Nome"].get(),
            "nacionalidade": entradas["Nacionalidade"].get(),
            "equipe": entradas["Equipe"].get(),
            "titulos": int(entradas["Títulos"].get()),
            "estatisticas": {
                "corridas": int(entradas["Corridas"].get()),
                "vitorias": int(entradas["Vitórias"].get()),
                "podios": int(entradas["Pódios"].get()),
                "poles": int(entradas["Poles"].get()),
                "voltas_mais_rapidas": int(entradas["Voltas Rápidas"].get())
            },
            "historico_equipes": entradas["Histórico"].get().split(",")
        }
        pilotos = carregar_pilotos()
        sucesso = cadastrar_piloto(pilotos, dados)
        if sucesso:
            messagebox.showinfo("Sucesso", "Piloto cadastrado com sucesso!")
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Número de piloto já existe.")

    janela = tk.Toplevel()
    janela.title("Cadastrar Piloto")

    campos = ["Número", "Nome", "Nacionalidade", "Equipe", "Títulos", "Corridas", "Vitórias", "Pódios", "Poles", "Voltas Rápidas", "Histórico"]
    entradas = {}

    for campo in campos:
        tk.Label(janela, text=campo).pack()
        entrada = tk.Entry(janela)
        entrada.pack()
        entradas[campo] = entrada

    tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

def listar_interface():
    def aplicar_filtro():
        equipe = entrada_filtro.get().lower()
        criterio = var_ordenar.get()
        pilotos = carregar_pilotos().values()

        if equipe:
            pilotos = [p for p in pilotos if equipe in p['equipe'].lower()]

        if criterio == "Número":
            pilotos = sorted(pilotos, key=lambda p: int(p['numero']))
        elif criterio == "Nome":
            pilotos = sorted(pilotos, key=lambda p: p['nome'])
        elif criterio == "Vitórias":
            pilotos = sorted(pilotos, key=lambda p: p['estatisticas']['vitorias'], reverse=True)

        for widget in frame_lista.winfo_children():
            widget.destroy()

        for piloto in pilotos:
            texto = f"{piloto['numero']} - {piloto['nome']} ({piloto['equipe']})"
            tk.Label(frame_lista, text=texto, anchor="w").pack(fill="x")

    janela_lista = tk.Toplevel()
    janela_lista.title("Lista de Pilotos")

    tk.Label(janela_lista, text="Filtrar por equipe:").pack()
    entrada_filtro = tk.Entry(janela_lista)
    entrada_filtro.pack()

    tk.Label(janela_lista, text="Ordenar por:").pack()
    var_ordenar = tk.StringVar(value="Número")
    tk.OptionMenu(janela_lista, var_ordenar, "Número", "Nome", "Vitórias").pack()

    tk.Button(janela_lista, text="Aplicar Filtro", command=aplicar_filtro).pack(pady=5)

    frame_lista = tk.Frame(janela_lista)
    frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

    aplicar_filtro()

def buscar_interface():
    def buscar():
        num = entrada.get()
        piloto = buscar_piloto(pilotos, num)
        if piloto:
            texto = f"""
Número: {piloto['numero']}
Nome: {piloto['nome']}
Nacionalidade: {piloto['nacionalidade']}
Equipe Atual: {piloto['equipe']}
Títulos: {piloto['titulos']}
Corridas: {piloto['estatisticas']['corridas']}
Vitórias: {piloto['estatisticas']['vitorias']}
Pódios: {piloto['estatisticas']['podios']}
Poles: {piloto['estatisticas']['poles']}
Voltas Rápidas: {piloto['estatisticas']['voltas_mais_rapidas']}
Histórico de Equipes: {', '.join(piloto['historico_equipes'])}
"""
            messagebox.showinfo("Piloto Encontrado", texto)
        else:
            messagebox.showerror("Erro", "Piloto não encontrado.")

    pilotos = carregar_pilotos()
    janela_busca = tk.Toplevel()
    janela_busca.title("Buscar Piloto")

    tk.Label(janela_busca, text="Número do piloto:").pack()
    entrada = tk.Entry(janela_busca)
    entrada.pack()
    tk.Button(janela_busca, text="Buscar", command=buscar).pack(pady=10)

def atualizar_interface():
    def atualizar():
        num = entrada_num.get()
        pilotos = carregar_pilotos()
        if num not in pilotos:
            messagebox.showerror("Erro", "Piloto não encontrado.")
            return

        piloto = pilotos[num]

        campos = ["Nome", "Nacionalidade", "Equipe", "Títulos", "Corridas", "Vitórias", "Pódios", "Poles", "Voltas Rápidas", "Histórico"]
        valores = [
            piloto["nome"], piloto["nacionalidade"], piloto["equipe"], str(piloto["titulos"]),
            str(piloto["estatisticas"]["corridas"]), str(piloto["estatisticas"]["vitorias"]),
            str(piloto["estatisticas"]["podios"]), str(piloto["estatisticas"]["poles"]),
            str(piloto["estatisticas"]["voltas_mais_rapidas"]), ",".join(piloto["historico_equipes"])
        ]
        entradas = {}

        janela_detalhes = tk.Toplevel()
        janela_detalhes.title("Atualizar Dados")

        for campo, valor in zip(campos, valores):
            tk.Label(janela_detalhes, text=campo).pack()
            entrada = tk.Entry(janela_detalhes)
            entrada.insert(0, valor)
            entrada.pack()
            entradas[campo] = entrada

        def salvar_atualizacao():
            novos_dados = {
                "nome": entradas["Nome"].get(),
                "nacionalidade": entradas["Nacionalidade"].get(),
                "equipe": entradas["Equipe"].get(),
                "titulos": int(entradas["Títulos"].get()),
                "estatisticas": {
                    "corridas": int(entradas["Corridas"].get()),
                    "vitorias": int(entradas["Vitórias"].get()),
                    "podios": int(entradas["Pódios"].get()),
                    "poles": int(entradas["Poles"].get()),
                    "voltas_mais_rapidas": int(entradas["Voltas Rápidas"].get())
                },
                "historico_equipes": entradas["Histórico"].get().split(",")
            }
            sucesso = atualizar_piloto(pilotos, num, novos_dados)
            if sucesso:
                messagebox.showinfo("Sucesso", "Piloto atualizado com sucesso!")
                janela_detalhes.destroy()
                janela_atualizar.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar piloto.")

        tk.Button(janela_detalhes, text="Salvar", command=salvar_atualizacao).pack(pady=10)

    janela_atualizar = tk.Toplevel()
    janela_atualizar.title("Atualizar Piloto")

    tk.Label(janela_atualizar, text="Número do piloto para atualizar:").pack()
    entrada_num = tk.Entry(janela_atualizar)
    entrada_num.pack()
    tk.Button(janela_atualizar, text="Buscar", command=atualizar).pack(pady=10)

def excluir_interface():
    def excluir():
        num = entrada_num.get()
        pilotos = carregar_pilotos()

        if num not in pilotos:
            messagebox.showerror("Erro", "Piloto não encontrado.")
            return

        confirmacao = messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o piloto {pilotos[num]['nome']}?")
        if confirmacao:
            sucesso = excluir_piloto(pilotos, num)
            if sucesso:
                messagebox.showinfo("Sucesso", "Piloto excluído com sucesso!")
                janela_excluir.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao excluir piloto.")

    janela_excluir = tk.Toplevel()
    janela_excluir.title("Excluir Piloto")

    tk.Label(janela_excluir, text="Número do piloto para excluir:").pack()
    entrada_num = tk.Entry(janela_excluir)
    entrada_num.pack()
    tk.Button(janela_excluir, text="Excluir", command=excluir).pack(pady=10)

def relatorios_interface():
    pilotos = carregar_pilotos()
    if not pilotos:
        messagebox.showinfo("Informação", "Nenhum piloto cadastrado.")
        return

    mais_titulos = piloto_com_mais_titulos(pilotos)
    mais_vitorias = piloto_com_mais_vitorias(pilotos)
    media = media_vitorias(pilotos)
    equipes = equipes_por_piloto(pilotos)

    janela_relat = tk.Toplevel()
    janela_relat.title("Relatórios e Estatísticas")

    texto = f"""🏆 Piloto com mais títulos:
{mais_titulos['nome']} ({mais_titulos['titulos']} títulos)

🥇 Piloto com mais vitórias:
{mais_vitorias['nome']} ({mais_vitorias['estatisticas']['vitorias']} vitórias)

📊 Média de vitórias por piloto:
{media:.2f}

🛠️ Quantidade de equipes por piloto:
"""
    for nome, qtd in equipes.items():
        texto += f"- {nome}: {qtd} equipes\n"

    tk.Label(janela_relat, text=texto, justify="left", anchor="w").pack(padx=10, pady=10)

def interface():
    global janela
    janela = tk.Tk()
    janela.title("Sistema de Pilotos F1")

    tk.Label(janela, text="Menu Principal", font=("Helvetica", 14)).pack(pady=10)

    tk.Button(janela, text="Cadastrar Piloto", width=25, command=abrir_cadastro).pack(pady=5)
    tk.Button(janela, text="Listar Pilotos", width=25, command=listar_interface).pack(pady=5)
    tk.Button(janela, text="Buscar Piloto", width=25, command=buscar_interface).pack(pady=5)
    tk.Button(janela, text="Atualizar Piloto", width=25, command=atualizar_interface).pack(pady=5)
    tk.Button(janela, text="Excluir Piloto", width=25, command=excluir_interface).pack(pady=5)
    tk.Button(janela, text="Relatórios e Estatísticas", width=25, command=relatorios_interface).pack(pady=5)

    janela.mainloop()


# Adicione esta parte abaixo
if __name__ == "__main__":
    interface()