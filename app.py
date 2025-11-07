import os
import sqlite3

user = sqlite3.connect("usuarios.db")

cursor = user.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL
) """)
user.commit()
def login():
    nome = input("Digite seu nome de usuario: ")
    senha = input("Digite sua senha: ")
    logon = cursor.execute(""""
    SELECT nome usuarios WHERE nome = ? AND senha = ?""")   
    if not nome in logon:
        print("Usuario não encontrado")
    else:
        print(logon)
    # verificar se senha=senha
def cadastro():
    os.system("cls")
    print("Tela de cadastro")
    nome = input("Digite o nome que seja utilizado: ")
    senha = input("Dinite sua senha: ")
    cursor.execute("""
    INSERT INTO usuarios (nome, senha)
    VALUES(?,?)""",(nome, senha))
    user.commit()
    user.close()
    print("Cadastro efetuado")



login()