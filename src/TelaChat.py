from PyQt5 import QtWidgets, QtCore, uic
from datetime import datetime
from Cliente import *
from random import randint
from Pilha import *

class TelaChat:
    def __init__(self, app, cliente, channel):
        self.app = app
        self.cliente = cliente
        # channel é uma tupla com (nome_canal, numero_usuarios, tópico)
        self.channel = channel
        # usuarios é um dicionário para verificar as cores de cada user do chat
        self.usuarios = {}

        try:
            self.call=uic.loadUi(r"interfaces\ModeloChat.ui")
        except:
            self.call=uic.loadUi(r"src\interfaces\ModeloChat.ui")

        # configurações iniciais dos widgets da tela
        self.call.textEditChat.setReadOnly(True)
        self.call.lineEditMensagem.setFocus()
        self.call.lineEditMensagem.setPlaceholderText("Mensagem")
        self.call.labelNomeCanal.setText(self.channel[0])


        # styleSheets dos widgets
        self.call.pushButtonVoltar.setStyleSheet("""
            QPushButton#pushButtonVoltar {
                background-color: #0074D9;
                color: #FFFFFF; 
                border: 2px solid #0056b3; 
                border-radius: 5px; 
                padding: 5px 15px;
                font-size: 11px;
                font-weight: bold;
            }
                                                 
            QPushButton#pushButtonVoltar:hover {
                background-color: #0056b3;
                color: #FFFFFF;
                border: 2px solid #003f7f;
            }
        """)

        self.call.pushButtonEnviar.setStyleSheet("""
            QPushButton#pushButtonEnviar {
                background-color: #0074D9;
                color: #FFFFFF; 
                border: 2px solid #0056b3; 
                border-radius: 5px; 
                padding: 5px 15px;
                font-size: 11px;
                font-weight: bold;
            }
                                                 
            QPushButton#pushButtonEnviar:hover {
                background-color: #0056b3;
                color: #FFFFFF;
                border: 2px solid #003f7f;
            }
        """)

        # conexões de widgets com métodos
        self.call.pushButtonEnviar.clicked.connect(self.action_enviar)
        self.call.lineEditMensagem.returnPressed.connect(self.action_enviar)
        self.call.pushButtonVoltar.clicked.connect(self.action_voltar)

        # mostra a tela
        self.call.show()


    # print estilizado para o chat
    def fancy_chat_print(self, msg, user="Você"):
        horario = datetime.now().strftime("%H:%M")
        msg = f"<span style='color: {self.usuarios.get(user, 'green')};'>{user}:</span> {msg} <span style='color: gray; font-size: small;'>{horario}</span>"
        self.call.textEditChat.append(msg)


    # envia uma mensagem no chat
    def action_enviar(self):
        msg = self.call.lineEditMensagem.text()
        if msg.strip() != "": # verifica se digitou algo
            self.cliente.sendPrivMsg(msg, self.channel[0])
            self.fancy_chat_print(msg)
        self.call.lineEditMensagem.setText("")
        self.call.lineEditMensagem.setFocus()


    # recebe uma mensagem no chat
    def receber(self, mensagem):
        # atualiza o chat quando outro user manda msg
        if mensagem[1][0] not in self.usuarios.keys():
            cor = self.define_cor()
            self.usuarios[mensagem[1][0]] = cor

        self.fancy_chat_print(mensagem[1][1], mensagem[1][0])

    
    # define a cor do usuário no chat
    def define_cor(self):
        while True:
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            cor = f"rgb({r}, {g}, {b})"
            if cor not in self.usuarios.values():
                return cor

    
    # volta para a tela de escolher canal
    def action_voltar(self):
        self.call.hide()
        self.cliente.leaveChannel(self.channel[0])
        pilha_telas.pop().call.show()

