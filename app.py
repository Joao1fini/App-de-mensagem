import os
import sqlite3
import questionary
user = sqlite3.connect("usuarios.db")

cursor = user.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha BCRYPT NOT NULL
) """)

cursor.execute("""CREATE UNIQUE INDEX IF NOT EXISTS id_user ON usuarios(nome)""")
user.commit()
def login():
    nome = input("Digite seu nome de usuario: ")
    senha = input("Digite sua senha: ")
    logon = cursor.execute("""
    SELECT * FROM usuarios WHERE nome = ? AND senha = ?""",(nome,senha))  
    result = logon.fetchone()
    if result:
        print(f"Bem vindo de volta {nome}")
        return True
    else:
        print("Usuario não encontrado")
    # verificar se senha=senha
def cadastro():
    while True:
        try:
            os.system("cls")
            print("Tela de cadastro")
            nome = input("Digite o nome que seja utilizado: ")
            senha = input("Dinite sua senha: ")
            cursor.execute("""
            INSERT INTO usuarios (nome, senha)
            VALUES(?,?)""",(nome, senha))
            user.commit()
            print("Cadastro efetuado")
        except sqlite3.IntegrityError:
            escolha = questionary.select("a existe um usuario com esse nome, deseja fazer login ou entar novamente",
                        choices=[
                            "Ir para login",
                            "Tentar novamente"
                        ])
            if escolha.startswith("I"):
                return login()
            else:
                continue
cadastro()
os.system("cls")
login()
