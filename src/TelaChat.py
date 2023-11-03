from PyQt5 import QtWidgets, uic
from datetime import datetime
from Cliente import *

class TelaChat:
    def __init__(self, app, cliente, channel):
        self.app = app
        self.channel = channel
        # channel é uma tupla com (nome_canal, numero_usuarios, tópico)
        self.cliente = cliente
        self.call=uic.loadUi(r"interfaces\ModeloChat.ui")

        self.call.pushButtonEnviar.clicked.connect(self.action_enviar)
        self.call.lineEditMensagem.returnPressed.connect(self.action_enviar)
        self.call.pushButtonEVoltar.clicked.connect(self.action_voltar)

        self.call.lineEditMensagem.setFocus()

        self.call.show()


    def fancy_chat_print(self, msg):
        # considerar colocar o horario da msg estilizado
        horario = datetime.now().strftime("%H:%M")
        msg = f"<span style='color: green;'>You:</span> {msg} <span style='color: gray; font-size: small;'>{horario}</span>"
        self.call.textEditChat.append(msg)


    def action_enviar(self):
        msg = self.call.lineEditMensagem.text()
        if msg.strip() != "": # verifica se digitou algo
            self.cliente.sendPrivMsg(msg, self.channel)
            self.fancy_chat_print(msg)
        self.call.lineEditMensagem.setText("")
        self.call.lineEditMensagem.setFocus()


    def receber(self):
        # atualizar o chat quando outro user manda msg
        #if cliente.rcvPrivMsg()
        pass

    
    def action_voltar(self):
        # pilha
        pass
