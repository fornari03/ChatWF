from socket import *
from time import sleep

# quando for pra coisas que n eh iniciar conexao, tem que definir a porta como non-blocking

class Cliente:

    def __init__(self, address):
        # a porta eh constante
        self.SERVER_PORT = 6667
        self._cliente = socket(AF_INET, SOCK_STREAM)
        try:
            self._cliente.connect((address, self.SERVER_PORT))
            self.open = True
        except:
            self.open = False

    # conecta com o servidor utilizando o usuario e o nick fornecido, e verifica se o nickname eh valido
    def autenticar(self, senha, nickname, nomeReal, modo: int):
        # tem que fazer ainda o try catch do timeoutError
        self._cliente.send(f"PASS {senha}\r\n".encode())
        self._cliente.send(f"NICK {nickname}\r\n".encode())
        self._cliente.send(f"USER {nickname} {modo} * :{nomeReal}\r\n".encode())

        # verificar se o nickname eh valido
        # so podemos fazer essa verificacao depois do user pq nao tem mensagem de confirmacao do nick :|
        ans = self._cliente.recv(512).decode()
        while ans[-2:] != "\r\n" or (ans.find("001") == -1 and ans.find("433") == -1 and ans.find("432") == -1 and ans.find("434") == -1 and ans.find("437") == -1):
            ans += self._cliente.recv(1024).decode()
            # espaco pq pode ter palavras que tem ping no burst de boas vindas, entao a mensagem de PING sempre tem um espaco depois, por especificacao do protocolo
            if ans.find("PING ") != -1:
                self._cliente.close()
                self.open = False
                return "pingInesperado"


        if ans.find("001") != -1:
            burst = ans[ans.find("001"):]
            while burst.find("End of /MOTD command") == -1 and burst[-2:] != "\r\n":
                burst += self._cliente.recv(512).decode()
            sleep(0.5)
            self._cliente.setblocking(False)
            try:
                ans = self._cliente.recv(1536)
                # mensagem que nao eh de erro que a gente encontrou testando em serenity.fl.us.del.net, em que nicks seriam iguais
                if ans.find("This nick is owned by someone else."):
                    self._cliente.close()
                    self.open = False
                    return "nickError"
            except:
                pass
        else:
            self._cliente.close()
            self.open = False
            return "semBurstWelcome"