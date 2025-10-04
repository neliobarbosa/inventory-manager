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

def load_data():
    item_list.delete(0, tk.END)
    data = sheet.get_all_records()
    inventory = {}
    for row in data:
        item = row["Item"].capitalize()
             
        qty = int(row["Quantidade"]) #quantity
        inventory[item] = inventory.get(item, 0) + qty
    for item, qty in inventory.items():
        item_list.insert(tk.END, f"{item}: {qty}")

def add_item():
    qty = entry_qty.get().strip()
    if not qty.isdigit():
        messagebox.showerror("Erro", "Preencha a quantidade corretamente!")
        return
    if mode_var.get() == "new":
        name = entry_item.get().strip().capitalize()
        if not name:
            messagebox.showerror("Erro", "Digite o nome do item")
            return
        sheet.append_row([name, int(qty)])
    else:
        selected = item_list.curselection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um item da lista")
            return
        line_text = item_list.get(selected[0])
        item_name = line_text.split(":")[0].strip()
        data = sheet.get_all_records()
        for i, row in enumerate(data, start=2):
            if row["Item"].capitalize() == item_name:
                new_qty = int(row["Quantidade"]) + int(qty)
                sheet.update_cell(i, 2, new_qty)
                break
    entry_item.delete(0, tk.END)
    entry_qty.delete(0, tk.END)
    load_data()

def remove_quantity():
    selected = item_list.curselection()
    if not selected:
        messagebox.showerror("Erro", "Selecione um item para remover quantidade")
        return
    qty_remove = entry_qty.get().strip()
    if not qty_remove.isdigit():
        messagebox.showerror("Erro", "Digite uma quantidade válida")
        return
    qty_remove = int(qty_remove)
    line_text = item_list.get(selected[0])
    item_name = line_text.split(":")[0].strip()
    data = sheet.get_all_records()
    for i, row in enumerate(data, start=2):
        if row["Item"].capitalize() == item_name:
            current_qty = int(row["Quantidade"])
            new_qty = max(current_qty - qty_remove, 0)
            sheet.update_cell(i, 2, new_qty)
            break
    entry_qty.delete(0, tk.END)
    load_data()
    messagebox.showinfo("Sucesso", f"{qty_remove} unidades removidas de {item_name}")

window = tk.Tk()
window.title("Controle de Estoque")
window.geometry("350x500")

tk.Label(window, text="Estoque Atual", font=("Arial", 14, "bold")).pack(pady=5)

frame_list = tk.Frame(window)
frame_list.pack(pady=10)
item_list = tk.Listbox(frame_list, width=30)
item_list.pack()

mode_var = tk.StringVar(value="existing")
tk.Radiobutton(window, text="Adicionar a item existente", variable=mode_var, value="existing").pack()
tk.Radiobutton(window, text="Criar item novo", variable=mode_var, value="new").pack()

tk.Label(window, text="Nome do Item (apenas para novo):").pack()
entry_item = tk.Entry(window)
entry_item.pack()

tk.Label(window, text="Quantidade:").pack()
entry_qty = tk.Entry(window)
entry_qty.pack()

btn_add = tk.Button(window, text="Adicionar/Atualizar", command=add_item)
btn_add.pack(pady=5)

btn_remove = tk.Button(window, text="Remover Quantidade", command=remove_quantity)
btn_remove.pack(pady=5)

load_data()
window.mainloop()
