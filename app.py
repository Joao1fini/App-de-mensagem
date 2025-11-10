import os
import sqlite3
import questionary

user = sqlite3.connect("usuarios.db")

os.makedirs("chat", exist_ok=True)   


cursor = user.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha BCRYPT NOT NULL
) """)

cursor.execute("""CREATE UNIQUE INDEX IF NOT EXISTS id_user ON usuarios(nome)""")
user.commit()

cursor.execute("SELECT id FROM usuarios")
lista = cursor.fetchall()
for i in range(1,(len(lista)+1)):
    e = str(i)
    os.makedirs("chat/"+e,exist_ok=True)

def login():
    nome = input("Digite seu nome de usuario: ")
    senha = input("Digite sua senha: ")
    logon = cursor.execute("""
    SELECT * FROM usuarios WHERE nome = ? AND senha = ?""",(nome,senha))  
    result = logon.fetchone()
    if result:
        print(f"Bem vindo de volta {nome}")
        cursor.execute("SELECT id FROM usuarios WHERE nome = ?",(nome,))
        id_u = cursor.fetchone()
        return id_u
    else:
        print("Usuario não encontrado")
        return True
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

def menu(id_user):
    escolha = questionary.select("",
            choices=[
                "Ver conversas",
                "Adicionar conversas",
                "Sair"
            ]).ask()
    if escolha.startswith("V"):
        print("legal")
    elif escolha.startswith("A"):
        add_user = input("qual o nome do usuario que quer se conectar ")
        cursor.execute("SELECT id OR nome FROM usuarios WHERE nome = ? OR id = ?",(add_user,add_user))
        achar = cursor.fetchone()
        if achar:
            if not os.path.exists(id_user + "/" + add_user + ".txt"):
                open("chat/"+id_user + "/" + add_user + ".txt", "a").close()
            if not os.path.exists(add_user + "/" + id_user + ".txt"):
                open("chat/"+add_user + "/" + id_user + ".txt", "a").close()
                #alterar depois para criar uma pasta sempre com o nome dos dois usuarios
        else:
            print("usuario não existe")
    else:
        return False

def conversa():
    caminho = os.path.join("chat",id_user)
    caminho2 = sorted(f for f in os.listdir(caminho))
    os.system("cls")
    escolha = questionary.select("Conversas",
        choices=caminho2
        
    ).ask()
    path = os.path.join(caminho, escolha)
    with open(path,"r+") as arquivo:
        chat = arquivo.read()
    print(chat)
    escolha = questionary.select("",
        choices=[
        "escrever",
        "sair"]
    ).ask()
    if escolha.startswith("e"):
        with open(path, "w") as arquivo:
            msg = ("0"+input(""))
            arquivo.write(msg)
    
id_user = login()
if not id_user == True:
    id_user = str(id_user[0])
    #if id_user:
    #    menu(id_user)
    conversa()

        