import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tkinter as tk
from tkinter import messagebox

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

json_path = os.path.join(base_path, "credentials.json")

creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
client = gspread.authorize(creds)
sheet = client.open("PlanilhaLar").sheet1

def carregar_dados():
    lista_itens.delete(0, tk.END)
    dados = sheet.get_all_records()
    estoque = {}
    for linha in dados:
        item = linha["Item"].capitalize()
        qtd = int(linha["Quantidade"])
        estoque[item] = estoque.get(item, 0) + qtd
    for item, qtd in estoque.items():
        lista_itens.insert(tk.END, f"{item}: {qtd}")

def adicionar_item():
    qtd = entrada_qtd.get().strip()
    if not qtd.isdigit():
        messagebox.showerror("Erro", "Preencha a quantidade corretamente!")
        return
    if modo_var.get() == "novo":
        nome = entrada_item.get().strip().capitalize()
        if not nome:
            messagebox.showerror("Erro", "Digite o nome do item")
            return
        sheet.append_row([nome, int(qtd)])
    else:
        selecionado = lista_itens.curselection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um item da lista")
            return
        linha_texto = lista_itens.get(selecionado[0])
        item_nome = linha_texto.split(":")[0].strip()
        dados = sheet.get_all_records()
        for i, linha in enumerate(dados, start=2):
            if linha["Item"].capitalize() == item_nome:
                nova_qtd = int(linha["Quantidade"]) + int(qtd)
                sheet.update_cell(i, 2, nova_qtd)
                break
    entrada_item.delete(0, tk.END)
    entrada_qtd.delete(0, tk.END)
    carregar_dados()

def remover_quantidade():
    selecionado = lista_itens.curselection()
    if not selecionado:
        messagebox.showerror("Erro", "Selecione um item para remover quantidade")
        return
    qtd_remover = entrada_qtd.get().strip()
    if not qtd_remover.isdigit():
        messagebox.showerror("Erro", "Digite uma quantidade válida")
        return
    qtd_remover = int(qtd_remover)
    linha_texto = lista_itens.get(selecionado[0])
    item_nome = linha_texto.split(":")[0].strip()
    dados = sheet.get_all_records()
    for i, linha in enumerate(dados, start=2):
        if linha["Item"].capitalize() == item_nome:
            qtd_atual = int(linha["Quantidade"])
            nova_qtd = max(qtd_atual - qtd_remover, 0)
            sheet.update_cell(i, 2, nova_qtd)
            break
    entrada_qtd.delete(0, tk.END)
    carregar_dados()
    messagebox.showinfo("Sucesso", f"{qtd_remover} unidades removidas de {item_nome}")

janela = tk.Tk()
janela.title("Controle de Estoque")
janela.geometry("350x500")

tk.Label(janela, text="Estoque Atual", font=("Arial", 14, "bold")).pack(pady=5)

frame_lista = tk.Frame(janela)
frame_lista.pack(pady=10)
lista_itens = tk.Listbox(frame_lista, width=30)
lista_itens.pack()

modo_var = tk.StringVar(value="existente")
tk.Radiobutton(janela, text="Adicionar a item existente", variable=modo_var, value="existente").pack()
tk.Radiobutton(janela, text="Criar item novo", variable=modo_var, value="novo").pack()

tk.Label(janela, text="Nome do Item (apenas para novo):").pack()
entrada_item = tk.Entry(janela)
entrada_item.pack()

tk.Label(janela, text="Quantidade:").pack()
entrada_qtd = tk.Entry(janela)
entrada_qtd.pack()

btn_add = tk.Button(janela, text="Adicionar/Atualizar", command=adicionar_item)
btn_add.pack(pady=5)

btn_remover = tk.Button(janela, text="Remover Quantidade", command=remover_quantidade)
btn_remover.pack(pady=5)

carregar_dados()
janela.mainloop()
