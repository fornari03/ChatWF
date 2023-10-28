from socket import *

# infos do servidor
SERVER_ADDRESS = ""
SERVER_PORT = 5050
IRC_PORT = 194
# server = gethostbyname(gethostname()) : pega o ip do computador
# para abrir a conexão com o servidor -> fsockopen() ?



# infos do cliente
nickname = "fulaninhogameplays12"
user = "fulaninhogameplays12"
canais = [] # uma lista de canais talvez



# funcoes criadas para facilitar o uso
def autenticar():
    cliente.send(f"USER {user}\r\n".encode("utf-8"))
    cliente.send(f"NICK {nickname}\r\n".encode("utf-8"))

def entrar_canal(canal):
    cliente.send(f"JOIN {canal}\r\n".encode("utf-8"))

def enviar_msg(msg, canal):
    cliente.send(f"PRIVMSG {canal}:{msg}\r\n".encode("utf-8"))


cliente = socket(AF_INET, SOCK_STREAM)
# endereço será (host + porta)

cliente.connect((SERVER_ADDRESS, SERVER_PORT))

autenticar()
    
entrar_canal(input("Nome do canal para entrar: "))

while (True):
    msg = cliente.recv(1500).decode("utf-8")

    if (msg.find("PING") != -1): # -1 é erro
        string = "ping\r\n".encode("utf-8")
        cliente.send(f"PONG :{string}")

        if (msg.split()[0] == ""):

    