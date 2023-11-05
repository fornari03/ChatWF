from socket import *
from time import sleep

# quando for pra coisas que n eh iniciar conexao, tem que definir a porta como non-blocking

class Cliente:

    def __init__(self, serverAddress):
        # a porta eh constante
        self.SERVER_PORT = 6667
        self._cliente = socket(AF_INET, SOCK_STREAM)
        self._server = serverAddress
        try:
            self._cliente.connect((serverAddress, self.SERVER_PORT))
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
                i = ans.find("PING ")
                self._cliente.send(f"PONG {ans[i+5:ans[i+5:].find(' ')]}\r\n".encode())
                ans = ans.replace("PING ", "")


        if ans.find("001") != -1:
            # pegar o servidor que enviou a mensagem
            self._server = ans.split("\r\n")[0].split()[0][1:]
            # acha o fim do burst ou se teve algum problema de nick
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
        
        return dados

    def messageProcessing(self, message: bytes):
        # metodo que vai receber uma lista de mensagens, e delas vai decidir qual metodo chamar
        # vai retornar uma tupla, o tipo de comando e as informacoes que tirou dele
        serverB = b':' + bytes(self._server, "utf-8")

        if b'PING ' in message:
            self.sendPong(message)
            return "ping", None
        elif b'JOIN ' in message or serverB + b' 323' in message or serverB + b' 473' in message or serverB + b' 471' in message or serverB + b' 474' in message or serverB + b' 475' in message or serverB + b' 323' in message:
            return self.joinReply(message)
        elif b'PART ' in message:
            return self.recvPart(message)
        elif b' PRIVMSG ' in message:
            return self.recvPrivMsg(message)
        elif b'401 ' in message and b':No such nick' in message:
            return "nickOuCanalInexistente", message.split(b' ')[-2]
        elif b'404 ' in message or b'411 ' in message or b'412 ' in message or b'413 ' in message or b'414 ' in message:
            return self.recvPrivMsg(message)
        elif b'301 ' in message:
            return self.recvAway(message)
        elif b'ERROR :Closing Link:' in message:
            return "conexaoEncerradaPeloServidor"
        else:
            return "MsgIgnorada", None

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
        for i in msgRecv:
            try:
                mensagens.append(i.decode())
            except:
                pass

        while (ans.find(b':' + bytes(self._server, "utf-8") + b' 323') == -1):
            ans = self._cliente.recv(512)
            msgRecv = (msgFalta + ans).split(b'\r\n')
            msgFalta = b''
            if ans[-2:] != b'\r\n':
                msgFalta = msgRecv[-1]
                msgRecv.pop()
            for i in msgRecv:
                try:
                    mensagens.append(i.decode())
                except:
                    pass

        while (ans[-2:] != b'\r\n'):
            ans = self._cliente.recv(512)
            msgRecv = (msgFalta + ans).split(b'\r\n')
            msgFalta = b''
            if ans[-2:] != b'\r\n':
                msgFalta = msgRecv[-1]
                msgRecv.pop()
            for i in msgRecv:
                try:
                    mensagens.append(i.decode())
                except:
                    pass
        
        for msg in mensagens:
            msg = msg.split()
            for i in range(len(msg)):
                if '#' in msg[i]:
                    canais.append((msg[i], msg[i+1], " ".join(msg[i+2:])[1:]))
                    break
        
        return canais
    
    def sendPrivMsg(self, message, receiver):
        # se eh canal, manda o receiver junto com o #
        self._cliente.send(f"PRIVMSG {receiver} :{message}\r\n".encode())
        # a gente ve se a mensagem foi bem recebida no getMessages, que talvez venha uma mensagem de erro

    def recvPrivMsg(self, message: bytes):
        msg = message.split(b' ')
        sender = msg[0].split(b'!')[0][1:]
        channel = msg[2]
        text = b' '.join(msg[3:])[1:]

        try:
            sender = sender.decode()
        except:
            for i in sender:
                if i > 0x7f:
                    sender.replace(bytes({i}), b'?')
            sender = sender.decode()
        
        try:
            text = text.decode()
        except:
            for i in text:
                if i > 0x7f:
                    text.replace(bytes({i}), b'?')
            text = text.decode()
        
        try:
            channel = channel.decode()
            # no caso da mensagem ser pro usuario, a gente coloca que o canal eh none
            if channel == self.nickname:
                channel = None
        except:
            return "privMsgError", "nao foi possivel decodificar o nickname ou channel aonde a mensagem quer chegar"        # acho que nunca vai entrar aqui, mas vai que ne
        
        return "privMsg", [sender, text, channel]

    def recvPrivMsgError(self, message: bytes):
        msg = message.split(b' ')
        return "erroEnvioPrivMsg", msg[-1].decode()[1:]
    
    def recvAway(self, message: bytes):
        msg = message.split(b' ')
        try:
            return "userAway", [msg[-2].decode(), msg[-1].decode()[1:]]
        except:
            nick = msg[-2]
            awayMsg = msg[-1]
            for i in nick:
                if i > 0x7f:
                    nick.replace(bytes({i}), b'?')
            nick = nick.decode()

            for i in awayMsg:
                if i > 0x7f:
                    awayMsg.replace(bytes({i}), b'?')
            awayMsg = awayMsg.decode()

            return "userAway", [nick, awayMsg]          

    def sendPong(self, msgPing: bytes):
        ping = msgPing.decode().split()
        for i in range(len(ping)):
            if ping[i] == "PING":
                server = ping[i+1]
                break
        
        self._cliente.send(f"PONG {server}\r\n".encode())

    def joinChannel(self, channel):
        # channel ja tem que vir com o # ou &
        if ("#" not in channel and "&" not in channel) or " " in channel or "," in channel or "\x07" in channel:
            return "nomeCanalInvalido"
        
        self._cliente.send(f"JOIN {channel}\r\n".encode())
        # o servidor vai mandar um JOIN com o nickname do usuario de volta, mas ai a gente ve isso no message processing

    def leaveChannel(self, channel):
        if ("#" not in channel and "&" not in channel) or " " in channel or "," in channel or "\x07" in channel:
            return "nomeCanalInvalido"
        
        self._cliente.send(f"PART {channel}\r\n".encode())

    def joinReply(self, message: bytes):
        msg = message.split(b' ')
        if b'JOIN ' in message:
            newUser = msg[0].split(b'!')[0][1:]     # pega so o nick da pessoa, tirando o : que ta no comeco da mensagem
            channel = msg[2]                        # o msg[1] eh o JOIN
            try:
                return "newUser", [newUser.decode(), channel.decode()]
            except:
                return "nonDecodableUsername", None
        elif b'332 ' in message:
            channel = msg[-2]
            topic = msg[-1]
            try:
                return "topic", [channel.decode(), topic[1:].decode()]
            except:
                for i in topic:
                    if i > 0x7f:
                        topic.replace(bytes({i}), b'?')
                return "topic", [channel.decode(), topic[1:].decode()]
        # talvez tenha que colocar mais um if pro caso de ser uma mensagem de quem ta no canal (codigo 353 pra RPL_NAMREPLY e 366 pra RPL_ENDOFNAMES)
        else:
            return "joinError", [msg[-2].decode(), msg[-1].decode()]           # retorna a [canal, mensagem de erro]
        
    def recvPart(self, message: bytes):
        msg = message.split(b' ')
        user = msg[0].split(b'!')[0][1:]
        # msg[1] eh o 'PART'
        channel = msg[2]
        partMsg = b''
        if len(msg) > 3:
            partMsg = msg[3]
        
        try:
            return "part", [user.decode(), channel.decode(), partMsg.decode()]
        except:
            for i in user:
                if i > 0x7f:
                    user.replace(bytes({i}), b'?')
            for i in partMsg:
                if i > 0x7f:
                    partMsg.replace(bytes({i}), b'?')
            
            return "part", [user.decode(), channel.decode(), partMsg.decode()]

    def quit(self):
        self._cliente.send("QUIT\r\n".encode())
        self._cliente.close()
        self.open = False
