from socket import *

class Cliente:

    def __init__(self, address):
        # a porta eh constante
        self.SERVER_PORT = 6667
        self._cliente = socket(AF_INET, SOCK_STREAM)
        self._cliente.connect((address, self.SERVER_PORT))

    # conecta com o servidor utilizando o usuario e o nick fornecido, e verifica se o nickname eh valido
    def autenticar(self, nickname, nomeReal, modo: int):
        self._cliente.send("PASS redesGrupoAfp")
        self._cliente.send(f"NICK {nickname}\r\n".encode("utf-8"))

        # verificacao pra ver se o nickname eh valido
        

        self._cliente.send(f"USER {nickname} {modo} * :{nomeReal}\r\n".encode("utf-8"))

    def entrar_canal(canal):
        cliente.send(f"JOIN {canal}\r\n".encode("utf-8"))

    def enviar_msg(msg, canal):
        cliente.send(f"PRIVMSG {canal}:{msg}\r\n".encode("utf-8"))

    autenticar()
        
    entrar_canal(input("Nome do canal para entrar: "))

    while (True):
        msg = cliente.recv(1500).decode("utf-8")

        if (msg.find("PING") != -1): # -1 é erro
            string = "ping\r\n".encode("utf-8")
            cliente.send(f"PONG :{string}")

            if (msg.split()[0] == ""):
                pass