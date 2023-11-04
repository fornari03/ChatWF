from PyQt5 import QtWidgets, QtCore, uic
from Cliente import *
from Pilha import *

class Teste:
    def __init__(self, app):
        self.app = app
        try:
            self.call=uic.loadUi(r"interfaces\teste.ui")
        except:
            self.call=uic.loadUi(r"src\interfaces\teste.ui")

        self.call.pushButton.clicked.connect(self.voltar)


        self.call.show()

    def voltar(self):
        self.call.hide()
        pilha_telas.pop().call.show()

