import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
import logging
import webbrowser


def filtrar_candidatos():
    cidade = entry_cidade.get()
    estado = entry_estado.get()
    expectativa_salarial = entry_expectativa_salarial.get()
    area_trabalho = entry_area_trabalho.get()

    conn = mysql.connector.connect(host='localhost',
                     user='root',
                     passwd='',
                     database='desenvolvedores_db')
    cursor = conn.cursor()

    query = "SELECT * FROM candidatos c left join status_candidatos sc on c.id = sc.id_candidato WHERE 1=1 and sc.id is null"
    if cidade:
        query += f" AND cidade = '{cidade}'"
    if estado:
        query += f" AND estado = '{estado}'"
    if expectativa_salarial:
        query += f" AND expectativa_salarial = {expectativa_salarial}"
    if area_trabalho:
        query += f" AND area_trabalho = '{area_trabalho}'"

    cursor.execute(query)
    candidatos = cursor.fetchall()

    for row in tabela.get_children():
        tabela.delete(row)

    for candidato in candidatos:
        tabela.insert("", "end", values=candidato)

    conn.close()
    
def acao_botao_visualizar():
    item = tabela.selection()

    
    id_candidato =  tabela.item(item, "values")[0]
   
    visualizar_dados_candidato(id_candidato)
    
def acao_botao_revisar():
    item = tabela.selection()

    
    id_candidato =  tabela.item(item, "values")[0]
   
    criar_janela_aprovacao(id_candidato)


def criar_janela_aprovacao(id_candidato):
    conn = mysql.connector.connect(host='localhost',
                     user='root',
                     passwd='',
                     database='desenvolvedores_db')
    cursor = conn.cursor()

    select_query = "SELECT * FROM candidatos WHERE id = " + id_candidato
    cursor.execute(select_query)
    candidato = cursor.fetchone()
    
    conn.close()
    
    janela_aprovacao = tk.Toplevel(root)
    janela_aprovacao.title("Aprovar/Negar Candidato")

    frame_aprovacao = tk.Frame(janela_aprovacao)
    frame_aprovacao.pack(padx=160, pady=160)

    label_aprovacao = tk.Label(frame_aprovacao, text=f"Aprovar ou Negar Candidato: {candidato[1]}")
    label_aprovacao.pack()

    escolha_aprovacao = tk.StringVar()
    escolha_aprovacao.set("Aprovar") 
    radio_aprovar = tk.Radiobutton(frame_aprovacao, text="Aprovar", variable=escolha_aprovacao, value="Aprovado")
    radio_aprovar.pack()
    radio_negar = tk.Radiobutton(frame_aprovacao, text="Negar", variable=escolha_aprovacao, value="Negado")
    radio_negar.pack()


    botao_confirmar = tk.Button(frame_aprovacao, text="Confirmar", command=lambda: atualizar_status_candidato(id_candidato, escolha_aprovacao.get()))
    botao_confirmar.pack()

def visualizar_dados_candidato(id_candidato):
    conn = mysql.connector.connect(host='localhost',
                     user='root',
                     passwd='',
                     database='desenvolvedores_db')
    cursor = conn.cursor()


    select_query = "SELECT * FROM candidatos WHERE id = " + id_candidato
    cursor.execute(select_query)
    candidato = cursor.fetchone()

    if candidato:
        janela_visualizacao = tk.Toplevel(root)
        janela_visualizacao.title("Detalhes do Candidato")

        frame_visualizacao = tk.Frame(janela_visualizacao)
        frame_visualizacao.pack(padx=100, pady=100)

        label_nome = tk.Label(frame_visualizacao, text=f"Nome: {candidato[1]}")
        label_nome.pack()
        label_idade = tk.Label(frame_visualizacao, text=f"Idade: {candidato[2]}")
        label_idade.pack()
        label_cidade_visualizar = tk.Label(frame_visualizacao, text=f"Cidade: {candidato[3]}")
        label_cidade_visualizar.pack()
        label_estado_visualizar = tk.Label(frame_visualizacao, text=f"Estado: {candidato[4]}")
        label_estado_visualizar.pack()
        label_telefone = tk.Label(frame_visualizacao, text=f"Telefone: {candidato[5]}")
        label_telefone.pack()
        label_email = tk.Label(frame_visualizacao, text=f"Email: {candidato[6]}")
        label_email.pack()
        label_experiencia = tk.Label(frame_visualizacao, text=f"Experiencia: {candidato[7]}")
        label_experiencia.pack()
        label_linkedin_visualizar = tk.Label(frame_visualizacao, text=f"LinkedIn: {candidato[9]}")
        label_linkedin_visualizar.pack()
        label_status_visualizar = tk.Label(frame_visualizacao, text=f"Status Emprego: {candidato[10]}")
        label_status_visualizar.pack()
        label_expectativa_salarial = tk.Label(frame_visualizacao, text=f"Expectativa: {candidato[11]}")
        label_expectativa_salarial.pack()
        botao_visualizar = tk.Button(frame_visualizacao, text="Visualizar Curriculo", command=webbrowser.open(candidato[8]))
        botao_visualizar.pack()
        
    conn.close()

def atualizar_status_candidato(id_candidato, status):
    conn = mysql.connector.connect(host='localhost',
                     user='root',
                     passwd='',
                     database='desenvolvedores_db')
    cursor = conn.cursor()

    update_query = "INSERT INTO status_candidatos (id_candidato, status) VALUES (%s, %s)"
    data = (id_candidato, status)
    cursor.execute(update_query, data)
    conn.commit()
    conn.close()

    filtrar_candidatos()


root = tk.Tk()
root.title("Recrutador")

frame = tk.Frame(root)
frame.pack(padx=50, pady=50)

label_cidade = tk.Label(frame, text="Cidade:")
label_cidade.grid(row=0, column=0)
entry_cidade = tk.Entry(frame)
entry_cidade.grid(row=0, column=1)

label_estado = tk.Label(frame, text="Estado:")
label_estado.grid(row=2, column=0)
entry_estado = tk.Entry(frame)
entry_estado.grid(row=2, column=1)

label_expectativa_salarial = tk.Label(frame, text="Expectativa Salarial:")
label_expectativa_salarial.grid(row=4, column=0)
entry_expectativa_salarial = tk.Entry(frame)
entry_expectativa_salarial.grid(row=4, column=1)

label_area_trabalho = tk.Label(frame, text="Area de trabalho:")
label_area_trabalho.grid(row=6, column=0)
entry_area_trabalho = tk.Entry(frame)
entry_area_trabalho.grid(row=6, column=1)

filtrar_button = tk.Button(frame, text="Filtrar Candidatos", command=filtrar_candidatos)
filtrar_button.grid(row=8, column=0, columnspan=2)


tabela = ttk.Treeview(frame, columns=("ID", "Nome", "Idade", "Cidade", "Estado", "Telefone", "Email", "Experiencia", "Curriculo", "linkedin", "status_emprego","expectativa_salarial"))
tabela.heading("ID", text="ID")
tabela.heading("Nome", text="Nome")
tabela.heading("Idade", text="Idade")
tabela.heading("Cidade", text="Cidade")
tabela.heading("Estado", text="Estado")
tabela.heading("Telefone", text="Telefone")
tabela.heading("Email", text="Email")
tabela.heading("Experiencia", text="Experiencia")
tabela.heading("Curriculo", text="Curriculo")
tabela.heading("linkedin", text="linkedin")
tabela.heading("status_emprego", text="status_emprego")
tabela.heading("expectativa_salarial", text="expectativa_salarial")
tabela.column("ID", width=10)
tabela.column("Nome", width=60)
tabela.column("Idade", width=50)
tabela.column("Cidade", width=100)
tabela.column("Estado", width=60)
tabela.column("Telefone", width=60)
tabela.column("Email", width=60)
tabela.column("Experiencia", width=60)
tabela.column("Curriculo", width=100)
tabela.column("linkedin", width=100)
tabela.column("status_emprego", width=100)
tabela.column("expectativa_salarial", width=60)

tabela.grid(row=10, column=0, columnspan=2)

botao_editar = ttk.Button(frame, text="Visualizar", command=acao_botao_visualizar)
botao_editar.grid(row=12, column=0, columnspan=2)
botao_editar = ttk.Button(frame, text="Revisar", command=acao_botao_revisar)
botao_editar.grid(row=12, column=1, columnspan=2)

root.mainloop()
