from PyQt5 import QtWidgets, uic
from TelaChat import *


class TelaAutenticacao:
    def __init__(self):
        self.app=QtWidgets.QApplication([])
        self.call=uic.loadUi(r"interfaces\ModeloAutenticacao.ui")

        self.call.lineEditNickname.setFocus()

        status_possiveis = ["Selecione um status", "Invisível"]
        for status in status_possiveis:
            self.call.comboBoxStatus.addItem(status)

        self.call.pushButtonLogin.clicked.connect(self.action_login)

        self.call.show()
        self.app.exec()



    def limpar_fields(self):
        self.call.lineEditNickname.setText("")
        self.call.lineEditUsername.setText("")
        self.call.lineEditSenha.setText("")
        self.call.comboBoxStatus.setCurrentIndex(0)
        self.call.lineEditNickname.setFocus()

    def abre_chat(self):
        self.second = TelaChat(self.app)
        self.call.hide()

    def action_login(self):
        # envia pro servidor a tentativa de autenticação
        # se ja tiver algum nick com o nome digitado:
        if self.call.lineEditSenha.text() == '123': # apenas para teste
            self.limpar_fields()
            popup = QtWidgets.QMessageBox()
            popup.setIcon(QtWidgets.QMessageBox.Warning)
            popup.setText("Este nickname já está sendo utilizado!")
            popup.setWindowTitle("Atenção")
            popup.exec_()
        else:
            self.abre_chat()



if __name__ == "__main__":
    app = TelaAutenticacao()