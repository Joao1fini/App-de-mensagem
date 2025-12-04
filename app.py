import os
import sqlite3
import questionary
import shutil
import threading
import time
import random
import datetime
user = sqlite3.connect("usuarios.db")
os.makedirs("chat", exist_ok=True)   

tecla = None
#variaveis (ficou muito complicado)
nome = ""
id_user=""
achar=""

cursor = user.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    senha BCRYPT NOT NULL
) """)
def login():
    global nome, id_user
    nome = input("Digite seu nome de usuario: ").lower()
    senha = input("Digite sua senha: ")
    logon = cursor.execute("""
    SELECT * FROM usuarios WHERE nome = ? AND senha = ?""",(nome,senha))  
    result = logon.fetchone()
    if result:
        os.system("cls")
        print(f"Bem vindo de volta {nome}")
        cursor.execute("SELECT id FROM usuarios WHERE nome = ?",(nome,))
        id_u = cursor.fetchone()
        id_user = str(id_u).strip("(),")
        return id_user
    else:
        print("Usuario não encontrado")
        return True
    # verificar se senha=senha
def cadastro():
    global nome, id_user
    while True:
        try:
            os.system("cls")
            print("Tela de cadastro")
            nome = input("Digite o nome que seja utilizado: ").lower()
            senha = input("Dinite sua senha: ")
            cursor.execute("SELECT nome FROM usuarios WHERE nome = ?",(nome,))
            validar = cursor.fetchone()
            if validar == None:
                id = random.randint(1000,4000)
                cursor.execute("""
                INSERT INTO usuarios (id, nome, senha)
                VALUES(?,?,?)""",(id, nome, senha))
                user.commit()
                print("Cadastro efetuado")
                id_user =str(id)
                os.makedirs("chat/"+id_user,exist_ok=True)
                time.sleep(1)
                os.system("cls")
            else:
                escolha = questionary.select("ja existe um usuario com esse nome, deseja fazer login ou entar novamente",
                        choices=[
                            "Ir para login",
                            "Tentar novamente"
                        ]).ask()
                if escolha.startswith("I"):
                    id_user = login()
                    if id_user:
                        return id_user
                    else:
                        continue
                else:
                    continue
            return id_user
        except sqlite3.IntegrityError:
            return False
def menu_de_conversa(id_user):
    global achar
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
            add_user = input("qual o nome que quer se conectar ")
            cursor.execute("SELECT nome FROM usuarios WHERE nome = ?",(add_user,))
            try:
                achar = cursor.fetchone()
                achar = str(achar).strip("'()',")
                cursor.execute("SELECT id FROM usuarios WHERE nome = ?",(add_user,))
                add_amigo = cursor.fetchone()
                add_user = str(add_amigo[0])
                if not os.path.exists("chat/"+id_user + "/"+ achar + ".txt"):
                    if add_user != nome:
                        open("chat/"+id_user + "/" + achar + ".txt", "a").close()
                        if not os.path.exists("chat/"+add_user + "/"+ achar + ".txt"):
                            if not os.path.exists(add_user + "/" + id_user + ".txt"):
                                open("chat/"+add_user + "/" + nome + ".txt", "a").close()
                    #alterar depois para criar uma pasta sempre com o nome dos dois usuarios
                else:
                    os.system("cls")
                    print("Usuario ja adicionado")
            except:
                print(f"usuario \033[31m{add_user}\033[0m não existe")
        else:
            return False
def conversa(id_user):
    try:
        caminho = os.path.join("chat",id_user)
        caminho2 = sorted(f for f in os.listdir(caminho))
        os.system("cls")
        caminho2.append("sair")
        print("\033[33m/v\033[0m para voltar;\n\033[33m/del\033[0m para apagar as ultimas mensagens;")
        escolha = questionary.select("",
            choices=caminho2
        ).ask()
        if escolha.startswith("sair"):
            return
        path = os.path.join(caminho, escolha)
        id = escolha[:-4]
        cursor.execute ("SELECT id FROM usuarios WHERE nome = ?", (id,))
        id_amigo = cursor.fetchone()
        id_amigo = str(id_amigo[0])
        path2 = os.path.join("chat",id_amigo,nome+".txt")
    except (FileNotFoundError,ValueError):
        print("Você ainda não iniciou nenhuma conversa")
        time.sleep(1)
        return
    print("/v para Voltar")
    time.sleep(0.5)
    os.system("cls")
    while True:
            chate(path,path2)
            break
def mostrar(path, stop_event):
    pos = 0
    while not stop_event.is_set():
        size = os.path.getsize(path)
        if size>pos:
            with open(path, "r") as arquivo:
                    arquivo.seek(pos)
                    chat = arquivo.read()
                    pos = arquivo.tell()
                    achar = os.path.splitext(os.path.basename(path))[0]
                    if f"{nome}>" in chat:
                        chat = chat.replace(f"{nome}>", f"\033[34m{nome}>\033[0m")  # azul
                    if f"{achar}>" in chat:
                        chat = chat.replace(f"{achar}>", f"\033[31m{achar}>\033[0m")  # azul
                    print(chat, end="",flush=True)
def chate(path,path2):
    stop_event = threading.Event()
    t = threading.Thread(target=mostrar, args=(path,stop_event),daemon=True)
    t.start()
    while True:
        tempo = datetime.datetime.now()
        datahora = tempo.strftime("%H:%M")
        with open(path, "a") as arquivo:
            msg = (f"{nome}>"+input("\033[33m/v\033[0m"+" "*2))
            tam = 100 - len(msg)
            if  "/v".strip() in msg:
                stop_event.set() 
                os.system("cls")
                break
            elif "/del".strip() in msg:
                    with open(path, "r") as oi:
                        linha = oi.readlines()
                    if linha:
                        linha.pop()
                    with open(path, "w") as oi:
                        oi.writelines(linha)
                        print("\033[F\033[K", end="")
            else:
                msg += (" "*tam)+datahora
                arquivo.write(msg +"\n")
            print("\033[F\033[K", end="")
        time.sleep(0.2)
        if path != path2:
            shutil.copyfile(path,path2)#copia o chat da pessoa 1 para a pessoa 2
def menu():
    while True:
        escolha = questionary.select(
            "CENTRAL DE CONVERSAS FINI",
            choices=[
                "Login",
                "Cadastro",
                "Sair"
            ]
        ).ask()
        if escolha.startswith("L"):
            id_user = login()
        elif escolha.startswith("C"):
            id_user = cadastro()
        elif escolha.startswith("S"):
            break
        if not id_user == True:
            id_user = str(id_user)
            if id_user:
                menu_de_conversa(id_user)
#Estrutura de funcionamento 
#⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇
os.system("cls")
menu()