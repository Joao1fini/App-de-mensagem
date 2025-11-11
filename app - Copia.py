import os
import sqlite3
import questionary
import shutil

user = sqlite3.connect("usuarios.db")
os.makedirs("chat", exist_ok=True)   

#variaveis (ficou muito complicado)
nome = ""
id_user=""

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
    global nome
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
            (cursor.execute("SELECT id FROM usuarios WHERE nome = ?", (nome,)))
            id_user = cursor.fetchone()

            return id_user
        except sqlite3.IntegrityError:
            return False

def menu_de_conversa(id_user):
    while True:
        escolha = questionary.select("",    
                choices=[
                    "Ver conversas",
                    "Adicionar conversas",
                    "Sair"
                ]).ask()
        if escolha.startswith("V"):      
            conversa(id_user)
        elif escolha.startswith("A"):
            add_user = input("qual o nome ou id do usuario que quer se conectar ")
            cursor.execute("SELECT nome FROM usuarios WHERE nome = ? OR id = ?",(add_user,add_user))
            achar = cursor.fetchone()
            achar = str(achar).strip("'()',")
            cursor.execute("SELECT id FROM usuarios WHERE nome = ? OR id = ?",(add_user,add_user))
            add_user = cursor.fetchone()
            add_user = str(add_user[0])
            if achar:
                if not os.path.exists(id_user + "/"+ achar + ".txt"):
                    open("chat/"+id_user + "/" + achar + ".txt", "a").close()
                if not os.path.exists(add_user + "/" + id_user + ".txt"):
                    open("chat/"+add_user + "/" + nome + ".txt", "a").close()
                    #alterar depois para criar uma pasta sempre com o nome dos dois usuarios
                else:
                    print("Usuario ja adicionado")
            else:
                print("usuario não existe")
        
            
        else:
            return False

def conversa(id_user):
    caminho = os.path.join("chat",id_user)
    caminho2 = sorted(f for f in os.listdir(caminho))
    os.system("cls")
    escolha = questionary.select("Conversas",
        choices=caminho2
    ).ask()
    path = os.path.join(caminho, escolha)
    seila = escolha[:-4]
    cursor.execute ("SELECT id FROM usuarios WHERE nome = ?", (seila,))
    id_amigo = cursor.fetchone()
    id_amigo = str(id_amigo[0])
    print(id_amigo)
    path2 = os.path.join("chat",id_amigo,nome+".txt")

     

    
    while True:
        escolha = questionary.select("",
            choices=[
            chate(path,path2)
            ]
        ).ask()
        if escolha.startswith(None):
            break

def chate(path,path2):
    while True:
        with open(path, "r") as arquivo:
                chat = arquivo.read()
        print(chat)
        with open(path, "a") as arquivo:
                msg = (f"{nome}>"+input(""))
                arquivo.write(msg +"\n")
        shutil.copyfile(path,path2)#copia o chat da pessoa 1 para a pessoa 2
        os.system("cls")
def menu():
    while True:
        print("CENTRAL DE CONVERSAS FINI")
        escolha = questionary.select("",
            choices=[
                "Login",
                "Cadastro",
                "Sair"
            ]
        ).ask()
        if escolha.startswith("L"):
            id_user = login()
        elif escolha.startswith("C"):
            if cadastro():
                escolha == "L"
                continue
            else:
                escolha = questionary.select("a existe um usuario com esse nome, deseja fazer login ou entar novamente",
                        choices=[
                            "Ir para login",
                            "Tentar novamente"
                        ]).ask()
                if escolha.startswith("I"):
                    login()
                else:
                    continue
        else:
            break
        if not id_user == True:
            id_user = str(id_user[0])
            if id_user:
                menu_de_conversa(id_user)
        else:
            continue
#Estrutura de funcionamento 
#⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇

os.system("cls")
menu()
    