import tkinter as tk
from tkinter import filedialog
import mysql.connector
from mysql.connector import Error

def salvar_dados():
    nome = entry_nome.get()
    idade = entry_idade.get()
    cidade = entry_cidade.get()
    estado = entry_estado.get()
    telefone = entry_telefone.get()
    email = entry_email.get()
    experiencia = text_experiencia.get("1.0", "end")
    curriculo = file_path
    linkedin = entry_linkedin.get()
    status_emprego = entry_status_emprego.get()
    expectativa_salarial = entry_expectativa_salarial.get()

    conn = mysql.connector.connect(host='localhost',
                     user='root',
                     passwd='',
                     database='desenvolvedores_db')
    cursor = conn.cursor()

    insert_query = "INSERT INTO candidatos (nome, idade, cidade, estado, telefone, email, experiencia, linkedin, status_emprego, expectativa_salarial, curriculo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (nome, idade, cidade, estado, telefone, email, experiencia, linkedin, status_emprego, expectativa_salarial, curriculo)
    cursor.execute(insert_query, data)

    conn.commit()
    conn.close()

    entry_nome.delete(0, "end")
    entry_idade.delete(0, "end")
    entry_cidade.delete(0, "end")
    entry_estado.delete(0, "end")
    entry_telefone.delete(0, "end")
    entry_email.delete(0, "end")
    text_experiencia.delete("1.0", "end")
    entry_linkedin.delete(0, "end")
    entry_status_emprego.delete(0, "end")
    entry_expectativa_salarial.delete(0, "end")

    file_path_label.config(text="Currículo anexado: Nenhum arquivo selecionado")

def anexar_curriculo():
    global file_path
    file_path = filedialog.askopenfilename()
    file_path_label.config(text=f"Currículo anexado: {file_path}")

root = tk.Tk()
root.title("Submissão de Candidato")

frame = tk.Frame(root)
frame.pack(padx=30, pady=40)

label_nome = tk.Label(frame, text="Nome:")
label_nome.grid(row=0, column=0)
entry_nome = tk.Entry(frame)
entry_nome.grid(row=0, column=1)

label_idade = tk.Label(frame, text="Idade:")
label_idade.grid(row=2, column=0)
entry_idade = tk.Entry(frame)
entry_idade.grid(row=2, column=1)

label_cidade = tk.Label(frame, text="Cidade:")
label_cidade.grid(row=4, column=0)
entry_cidade = tk.Entry(frame)
entry_cidade.grid(row=4, column=1)

label_estado = tk.Label(frame, text="Estado:")
label_estado.grid(row=6, column=0)
entry_estado = tk.Entry(frame)
entry_estado.grid(row=6, column=1)

label_telefone = tk.Label(frame, text="Telefone:")
label_telefone.grid(row=8, column=0)
entry_telefone = tk.Entry(frame)
entry_telefone.grid(row=8, column=1)

label_email = tk.Label(frame, text="Email:")
label_email.grid(row=10, column=0)
entry_email = tk.Entry(frame)
entry_email.grid(row=10, column=1)

label_linkedin = tk.Label(frame, text="LinkedIn:")
label_linkedin.grid(row=12, column=0)
entry_linkedin = tk.Entry(frame)
entry_linkedin.grid(row=12, column=1)

label_status_emprego = tk.Label(frame, text="Status de Emprego:")
label_status_emprego.grid(row=14, column=0)
entry_status_emprego = tk.Entry(frame)
entry_status_emprego.grid(row=14, column=1)

label_expectativa_salarial = tk.Label(frame, text="Expectativa Salarial:")
label_expectativa_salarial.grid(row=16, column=0)
entry_expectativa_salarial = tk.Entry(frame)
entry_expectativa_salarial.grid(row=16, column=1)

label_experiencia = tk.Label(frame, text="Experiência:")
label_experiencia.grid(row=18, column=0)
text_experiencia = tk.Text(frame, height=5, width=30)
text_experiencia.grid(row=18, column=1)

file_path = ""
file_path_label = tk.Label(frame, text="Currículo anexado: Nenhum arquivo selecionado")
file_path_label.grid(row=20, column=0, columnspan=2)
anexar_button = tk.Button(frame, text="Anexar Currículo", command=anexar_curriculo)
anexar_button.grid(row=22, column=0, columnspan=2)

submit_button = tk.Button(frame, text="Submeter", command=salvar_dados)
submit_button.grid(row=24, column=0, columnspan=2)

root.mainloop()
