from PyQt5 import QtWidgets, QtCore, uic
from datetime import datetime
from Cliente import *
from random import randint
from Pilha import *

class TelaChat:
    def __init__(self, app, cliente, channel):
        self.app = app
        self.channel = channel
        # channel é uma tupla com (nome_canal, numero_usuarios, tópico)
        self.cliente = cliente
        self.usuarios = {}
        self.call=uic.loadUi(r"interfaces\ModeloChat.ui")

        self.call.pushButtonEnviar.clicked.connect(self.action_enviar)
        self.call.lineEditMensagem.returnPressed.connect(self.action_enviar)
        self.call.pushButtonVoltar.clicked.connect(self.action_voltar)

        self.call.lineEditMensagem.setFocus()
        self.call.lineEditMensagem.setPlaceholderText("Mensagem")


        self.atualiza_mensagens = QtCore.QTimer(self)
        self.atualiza_mensagens.timeout.connect(self.receber)
        self.atualiza_mensagens.start(1000)

        self.call.show()


    def fancy_chat_print(self, msg, user="Você"):
        horario = datetime.now().strftime("%H:%M")
        msg = f"<span style='color: {self.usuarios.get(user, 'green')};'>{user}:</span> {msg} <span style='color: gray; font-size: small;'>{horario}</span>"
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
        #if self.cliente.rcvPrivMsg()
        mensagem = ("user", "blablabla")
        if mensagem[0] not in self.usuarios.keys():
            cor = self.define_cor()
            self.usuarios[mensagem[0]] = cor

        self.fancy_chat_print(mensagem[1], mensagem[0])

    
    def define_cor(self):
        while True:
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            cor = f"rgb({r}, {g}, {b})"
            if cor not in self.usuarios.values():
                return cor

    
    def action_voltar(self):
        self.call.hide()
        pilha_telas.pop().call.show()

