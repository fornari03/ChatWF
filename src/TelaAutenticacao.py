from PyQt5 import QtWidgets, uic
from TelaChat import *
from Cliente import *
from TelaEscolhaCanal import *


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

    def throw_message_box(self, titulo, texto):
        self.limpar_fields()
        popup = QtWidgets.QMessageBox()
        popup.setIcon(QtWidgets.QMessageBox.Warning)
        popup.setText(texto)
        popup.setWindowTitle(titulo)
        popup.exec_()

    def abre_lista_channels(self):
        channels = TelaEscolhaCanal(self.app, self.cliente)
        self.call.hide()

    def action_login(self):
        if (self.call.lineEditNickname.text().strip() == "" or 
        self.call.lineEditUserkname.text().strip() == "" or 
        self.call.lineEditSenha.text().strip() == "" or 
        self.call.lineEditServidor.text().strip() == "" or 
        self.call.comboBoxStatus.index() == 0 or 
        self.call.comboBoxStatus.index() == -1):
            self.throw_message_box("Atenção", "Você deve preencher todos os campos!")

        else :
            # envia pro servidor a tentativa de autenticação
            # se ja tiver algum nick com o nome digitado:
            self.cliente = Cliente(self.call.lineEditServidor.text())
            if self.cliente.open:
                retorno = self.cliente.autenticar(self.call.lineEditSenha.text(), self.call.lineEditNickname.text(), self.call.lineEditUsername.text(), self.call.comboBoxStatus.currentIndex()-1)


                if retorno == "pingInesperado":
                    self.throw_message_box("Atenção", "Ping inesperado!")
                elif retorno == "nickError":
                    self.throw_message_box("Atenção", "O nickname digitado já está em uso.")
                elif retorno == "semBurstWelcome":
                    pass
                else:
                    self.abre_lista_channels()
                    
            else:    
                self.throw_message_box("Atenção", "Não foi possível se conectar ao servidor.")
                self.call.lineEditServidor.setText("")
                self.call.lineEditServidor.setFocus()



if __name__ == "__main__":
    app = TelaAutenticacao()