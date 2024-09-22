import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import json

# Dicionário para armazenar as famílias
familias = {}

# Funções de Persistência
def salvar_dados():
    with open('familias.json', 'w') as f:
        json.dump(familias, f)

def carregar_dados():
    global familias
    try:
        with open('familias.json', 'r') as f:
            familias = json.load(f)
    except FileNotFoundError:
        familias = {}

# Função para cadastrar uma nova família
def cadastrar_familia(nome_responsavel, telefone, conjuge, filhos):
    familias[nome_responsavel] = {
        'telefone': telefone,
        'conjuge': conjuge,
        'filhos': filhos,
        'retiradas': [],
        'historico': []
    }
    messagebox.showinfo("Sucesso", f"Família de {nome_responsavel} cadastrada com sucesso.")
    salvar_dados()

# Função para registrar uma retirada de alimentos
def registrar_retirada(nome_responsavel, nome_alimento, quantidade):
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    retirada = {
        "data": data_hoje,
        "alimento": {
            "nome_alimento": nome_alimento,
            "quantidade": quantidade
        }
    }

    if nome_responsavel in familias:
        familias[nome_responsavel]['retiradas'].append(retirada)
        familias[nome_responsavel]['historico'].append(retirada)
        messagebox.showinfo("Sucesso", f"Retirada de {quantidade} unidades de {nome_alimento} registrada para {nome_responsavel}.")
        salvar_dados()
    else:
        messagebox.showerror("Erro", f"Família de {nome_responsavel} não encontrada.")

# Função para exibir todas as famílias e a última retirada de cada uma
def exibir_familias_ultima_retirada():
    info = ""
    for nome, dados in familias.items():
        if dados['retiradas']:
            ultima_retirada = dados['retiradas'][-1]
            info += f"Família: {nome}, Última Retirada: {ultima_retirada['alimento']['quantidade']} unidades de {ultima_retirada['alimento']['nome_alimento']} em {ultima_retirada['data']}\n"
        else:
            info += f"Família: {nome}, Última Retirada: Nenhuma retirada registrada.\n"
    messagebox.showinfo("Últimas Retiradas", info)

# Função para verificar se há famílias sem receber alimentos há mais de um mês
def verificar_familias_sem_retirada():
    um_mes_atras = datetime.now() - timedelta(days=30)
    alertas = ""
    for nome, dados in familias.items():
        if dados['retiradas']:
            ultima_retirada_data = datetime.strptime(dados['retiradas'][-1]['data'], "%d/%m/%Y")
            if ultima_retirada_data < um_mes_atras:
                alertas += f"Alerta: {nome} não recebe alimentos há mais de um mês.\n"
        else:
            alertas += f"Alerta: {nome} nunca recebeu alimentos.\n"
    if alertas:
        messagebox.showwarning("Famílias sem Retirada", alertas)
    else:
        messagebox.showinfo("Tudo OK", "Todas as famílias receberam alimentos no último mês.")

# Função para exibir todo o histórico de retiradas de uma família
def exibir_historico(nome_responsavel):
    if nome_responsavel in familias:
        historico = familias[nome_responsavel]['historico']
        if historico:
            info = f"Histórico de retiradas para {nome_responsavel}:\n"
            for retirada in historico:
                info += f"- Data: {retirada['data']}, {retirada['alimento']['quantidade']} unidades de {retirada['alimento']['nome_alimento']}\n"
            messagebox.showinfo(f"Histórico de {nome_responsavel}", info)
        else:
            messagebox.showinfo("Histórico Vazio", f"Família de {nome_responsavel} não tem retiradas registradas.")
    else:
        messagebox.showerror("Erro", f"Família de {nome_responsavel} não encontrada.")

# Função para exibir a tela de cadastro de famílias
def abrir_tela_cadastro():
    tela_cadastro = tk.Toplevel()
    tela_cadastro.title("Cadastrar Família")
    tela_cadastro.geometry("450x300+420+100")

    # Labels e campos de entrada para cadastro de famílias
    tk.Label(tela_cadastro, text="Nome do Responsável").grid(row=0, column=0, padx=(50,0), pady=(10,0))
    tk.Label(tela_cadastro, text="Telefone").grid(row=1, column=0, padx=(50,0), pady=(10,0))
    tk.Label(tela_cadastro, text="Cônjuge").grid(row=2, column=0, padx=(50,0), pady=(10,0))
    tk.Label(tela_cadastro, text="Filhos (nome e idade)").grid(row=3, column=0, padx=(50,0), pady=(10,0))

    nome_entry = tk.Entry(tela_cadastro)
    telefone_entry = tk.Entry(tela_cadastro)
    conjuge_entry = tk.Entry(tela_cadastro)
    filhos_entry = tk.Entry(tela_cadastro)

    nome_entry.grid(row=0, column=1, padx=(50,0), pady=(10,0))
    telefone_entry.grid(row=1, column=1, padx=(50,0), pady=(10,0))
    conjuge_entry.grid(row=2, column=1, padx=(50,0), pady=(10,0))
    filhos_entry.grid(row=3, column=1, padx=(50,0), pady=(10,0))

    def registrar_familia():
        nome = nome_entry.get()
        telefone = telefone_entry.get()
        conjuge = conjuge_entry.get()
        filhos = filhos_entry.get()
        cadastrar_familia(nome, telefone, conjuge, filhos)

    # Botão para registrar a família
    tk.Button(tela_cadastro, text="Registrar Família", command=registrar_familia).grid(row=4, column=1, padx=(50,0), pady=(10,0))

# Função para exibir a tela de registrar retirada de alimentos
def abrir_tela_retirada():
    tela_retirada = tk.Toplevel()
    tela_retirada.title("Registrar Retirada de Alimentos")
    tela_retirada.geometry("450x300+420+100")

    # Labels e campos de entrada para registrar retiradas
    tk.Label(tela_retirada, text="Nome do Responsável").grid(row=0, column=0, padx=(50,0), pady=(10,0))
    tk.Label(tela_retirada, text="Nome do Alimento").grid(row=1, column=0, padx=(50,0), pady=(10,0))
    tk.Label(tela_retirada, text="Quantidade").grid(row=2, column=0, padx=(50,0), pady=(10,0))

    nome_retirada_entry = tk.Entry(tela_retirada)
    nome_alimento_entry = tk.Entry(tela_retirada)
    quantidade_entry = tk.Entry(tela_retirada)

    nome_retirada_entry.grid(row=0, column=1, padx=(50,0), pady=(10,0))
    nome_alimento_entry.grid(row=1, column=1, padx=(50,0), pady=(10,0))
    quantidade_entry.grid(row=2, column=1, padx=(50,0), pady=(10,0))

    def registrar_alimento():
        nome = nome_retirada_entry.get()
        alimento = nome_alimento_entry.get()
        quantidade = quantidade_entry.get()
        registrar_retirada(nome, alimento, quantidade)

    # Botão para registrar retirada
    tk.Button(tela_retirada, text="Registrar Retirada", command=registrar_alimento).grid(row=3, column=1, padx=(50,0), pady=(10,0))

# Função para construir a interface gráfica principal
def iniciar_interface():
    root = tk.Tk()
    root.title("Sistema de Gerenciamento de Retiradas")
    root.geometry("450x300+420+100")

    # Botões para abrir as telas de cadastro e retirada
    tk.Button(root, text="Cadastrar Família", command=abrir_tela_cadastro).grid(row=0, column=0, padx=(20,0), pady=(0,0))
    tk.Button(root, text="Registrar Retirada de Alimentos", command=abrir_tela_retirada).grid(row=0, column=0, padx=(20,0), pady=(70,0))

    # Botões para acessar outras funcionalidades
    tk.Button(root, text="Verificar Últimas Retiradas", command=exibir_familias_ultima_retirada).grid(row=1, column=0, padx=(20,0), pady=(80,0))
    tk.Button(root, text="Verificar Famílias sem Retirada", command=verificar_familias_sem_retirada).grid(row=1, column=1, padx=(20,0), pady=(80,0))

    # Campo e botão para verificar histórico
    tk.Label(root, text="Nome do Responsável (Histórico)").grid(row=0, column=1)
    nome_historico_entry = tk.Entry(root)
    nome_historico_entry.grid(row=0, column=1,pady=(40,0))

    def mostrar_historico():
        nome = nome_historico_entry.get()
        exibir_historico(nome)

    tk.Button(root, text="Exibir Histórico", command=mostrar_historico).grid(row=0, column=1, padx=(0,0),pady=(90,0))

    root.mainloop()


# Carrega os dados ao iniciar o programa
carregar_dados()

# Executa a interface gráfica
iniciar_interface()

from datetime import datetime,timedelta

familias = {}

def cadastro_familias(nome_responsavel, telefone,conjuge,filhos):
    familias[nome_responsavel]= {
        "telefone":telefone,
        "conjuge":conjuge,
        "filhos":filhos,
        "retirada":[],
        "historico":[]
    }
    print(f"Familia de {nome_responsavel} cadastrada com sucesso.")

def registra_retirada(nome_responsavel,nome_alimento,quantidade):
    data_hoje = datetime.now()
    retirada = {
        "data":data_hoje,
        "alimento":{
            "nome_alimento":nome_alimento,
            "quantidade":quantidade
        }
    }

    if nome_responsavel in familias:
        familias[nome_responsavel]["retirada"].append(retirada)
        familias[nome_responsavel]["historico"].apend(retirada)
        print(f"Retirada de {quantidade}unidades de {nome_alimento}")
    else:
        print(f"Familia de {nome_responsavel}nao encontrada.")


    def exibir_ultima_retirada():
        for nome,valor in familias.items():
            if valor["retirada"]:
                ultima_retirada = valor["retirada"][-1]
                print(f"familia:{nome_responsavel},ultima retirada:{ultima_retirada["alimento"]["quantidade"]}unidades de {ultima_retirada["alimento"]["nome_alimento"]}em {ultima_retirada["data"]}")
            else:
                print(f"Familia:{nome_responsavel},ultima retirada: nenhuma")


    def verificar_familias_sem_retiradas():
        um_mes_atras = datetime.now() - timedelta(days=30)
        for nome,dados in familias.items():
            if dados["retiradas"]:
                ultima_retirada_data = datetime.strftime(dados["retiradas"][-1]["data"],"%d/%m/%Y")
                if ultima_retirada_data > um_mes_atras:
                    print(f"Alerta: {nome} nao recebe alimentos ha mais de um mes.")

            else:
                print(f"Alerta:{nome} nunca recebeu alimentos")

    def exibir_historico(nome_responsavel):
        if nome_responsavel in familias:
            historico = familias[nome_responsavel]["historico"]
            if historico:
                print(f"Historico de retirada para {nome_responsavel}")
                for retirada in historico:
                    print(f" data: {retirada["data"]},{retirada["alimento"]["quantidade"]} unidades de {retirada["aliemtento"]["nome_alimento"]}")
            else:
                print(f"Família de {nome_responsavel} não tem retiradas registradas.")
        else:
            print(f"Família de {nome_responsavel} não encontrada.")