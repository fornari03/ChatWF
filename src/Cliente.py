from socket import *
from time import sleep

# quando for pra coisas que n eh iniciar conexao, tem que definir a porta como non-blocking

class Cliente:

    def __init__(self, address):
        # a porta eh constante
        self.SERVER_PORT = 6667
        self._cliente = socket(AF_INET, SOCK_STREAM)
        self._server = address
        try:
            self._cliente.connect((address, self.SERVER_PORT))
            self.open = True
        except:
            self.open = False

    # conecta com o servidor utilizando o usuario e o nick fornecido, e verifica se o nickname eh valido
    def autenticar(self, senha, nickname, nomeReal, modo: int):
        self.nickname = nickname
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
        elif ans.find("433") != -1 or ans.find("432") != -1 or ans.find("434") != -1 or ans.find("437") != -1:
            self._cliente.close()
            self.open = False
            return "nickError"
        else:
            self._cliente.close()
            self.open = False
            return "semBurstWelcome"

    # implementacao ruim, eh bom a gente ver as mensagens e analisar uma a uma no objeto, e tbm a posicao do try ta ruim
    def getMessages(self):
        semMsg = False
        self._cliente.setblocking(False)
        messages = []
        dados = []
        ans = b''
        while not semMsg:
            try:
                ans += self._cliente.recv(512)
                if ans[-2:] == b'\r\n':
                    messages.extend(ans.split(b'\r\n'))
                    ans = b''
                else:
                    ans = ans.split(b'\r\n')
                    messages.extend(ans[:-1])
                    ans = ans[-1]
            except:
                semMsg = True
        
        for msg in messages:
            dados.append(self.messageProcessing(msg))

    def messageProcessing(self, message: bytes):
        # metodo que vai receber uma lista de mensagens, e delas vai decidir qual metodo chamar
        # vai retornar uma tupla, o tipo de comando e as informacoes que tirou dele
        #TODO
        pass

    def getChannelList(self):
        # tem que arrumar esse codigo ainda, acho que eh bom mexer em algumas coisas, como botar em uma lista
        # e tbm a gente so retorna os canais que seu nome e descricao podem ser decodificados pra utf-8
        mensagens = []
        canais = []

        self._cliente.setblocking(True)
        self._cliente.send("LIST\r\n".encode())
        sleep(0.5)

        ans = self._cliente.recv(1024)
        msgRecv = ans.split(b'\r\n')
        msgFalta = b''
        if ans[-2:] != b'\r\n':
            msgFalta = msgRecv[-1]
            msgRecv.pop()

        while (ans.find(b':' + bytes(self._server, "utf-8") + b' 323') == -1):
            for i in msgRecv:
                try:
                    mensagens.append(i.decode())
                except:
                    pass
            ans = self._cliente.recv(512)
            msgRecv = (msgFalta + ans).split(b'\r\n')
            msgFalta = b''
            if ans[-2:] != b'\r\n':
                msgFalta = msgRecv[-1]
                msgRecv.pop()

        while (ans[-2:] != b'\r\n'):
            for i in msgRecv:
                try:
                    mensagens.append(i.decode())
                except:
                    pass
            ans = self._cliente.recv(512)
            msgRecv = (msgFalta + ans).split(b'\r\n')
            msgFalta = b''
            if ans[-2:] != b'\r\n':
                msgFalta = msgRecv[-1]
                msgRecv.pop()
        
        for msg in mensagens:
            msg = msg.split()
            for word in msg:
                if '#' in word:
                    canais.append(word)
                    break
        
        return canais
    
    def sendPrivMsg(self, message, receiver):
        # se eh canal, manda o receiver junto com o #
        self._cliente.send(f"PRIVMSG {receiver} :{message}".encode())
        # a gente ve se a mensagem foi bem recebida no getMessages, que talvez venha uma mensagem de erro

    def sendPong(self, msgPing):
        ping = msgPing.split()
        for i in range(len(ping)):
            if ping[i] == "PING":
                server = ping[i+1]
                break
        
        self._cliente.send(f"PONG {server}")

    def quit(self):
        self._cliente.send("QUIT\r\n".encode())
        self._cliente.close()
        self.open = False
