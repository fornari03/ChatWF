from PyQt5 import QtWidgets, uic
from TelaChat import *
from Cliente import *
from TelaEscolhaCanal import *
from Pilha import *
from testeInstancia import *


class TelaAutenticacao:
    def __init__(self):
        self.app=QtWidgets.QApplication([])
        try:
            self.call=uic.loadUi(r"interfaces\ModeloAutenticacao.ui")
        except:
            self.call=uic.loadUi(r"src\interfaces\ModeloAutenticacao.ui")

        # configurações iniciais dos widgets da tela
        self.call.lineEditNickname.setFocus()
        modo_possiveis = ["Selecione um modo", "Normal", "Invisível"]
        for modo in modo_possiveis:
            self.call.comboBoxModo.addItem(modo)

        # styleSheets dos widgets
        self.call.pushButtonConectar.setStyleSheet("""                                
            QPushButton#pushButtonConectar {
                background-color: #0074D9;
                color: #FFFFFF;
                border: 2px solid #0056b3;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#pushButtonConectar:hover {
                background-color: #0056b3;
                color: #FFFFFF;
                border: 2px solid #003f7f;
            }
        """)

        # conexões de widgets com métodos
        self.call.pushButtonConectar.clicked.connect(self.action_Conectar)

        # mostra a tela e inicia a aplicação
        self.call.show()
        self.app.exec()


    # retorna todos os fields ao estado inicial
    def limpar_fields(self):
        self.call.lineEditNickname.setText("")
        self.call.lineEditNomeReal.setText("")
        self.call.lineEditSenha.setText("")
        self.call.comboBoxModo.setCurrentIndex(0)
        self.call.lineEditNickname.setFocus()


    # instancia uma caixa de mensagem
    def throw_message_box(self, titulo, texto):
        # self.limpar_fields()
        aviso = QtWidgets.QMessageBox()
        aviso.setIcon(QtWidgets.QMessageBox.Warning)
        aviso.setText(texto)
        aviso.setWindowTitle(titulo)
        aviso.exec_()


    # muda para a tela de escolha de canais
    def abre_lista_channels(self):
        self.channels = TelaEscolhaCanal(self.app, self.cliente)
        pilha_telas.append(self)
        self.call.hide()


    # tenta fazer a conexão com o servidor a partir dos dados fornecidos
    def action_Conectar(self):
        if self.call.lineEditNickname.text().strip() == "":
            self.throw_message_box("Atenção", "Você deve preencher todos os campos!")
            self.call.lineEditNickname.setFocus()
            self.call.lineEditNickname.setText("")
        elif self.call.lineEditNomeReal.text().strip() == "":
            self.throw_message_box("Atenção", "Você deve preencher todos os campos!")
            self.call.lineEditNomeReal.setFocus()
            self.call.lineEditNomeReal.setText("")
        elif self.call.lineEditSenha.text().strip() == "":
            self.throw_message_box("Atenção", "Você deve preencher todos os campos!")
            self.call.lineEditSenha.setFocus()
            self.call.lineEditNickname.setText("")
        elif self.call.lineEditServidor.text().strip() == "":
            self.throw_message_box("Atenção", "Você deve preencher todos os campos!")
            self.call.lineEditServidor.setFocus()
            self.call.lineEditServidor.setText("")
        elif (self.call.comboBoxModo.currentIndex() == 0 or
              self.call.comboBoxModo.currentIndex() == -1):
            self.throw_message_box("Atenção", "Selecione um modo!")
            self.call.comboBoxModo.setFocus()
            self.call.comboBoxModo.setCurrentIndex(0)

        else :
            # envia pro servidor a tentativa de autenticação
            self.cliente = Cliente(self.call.lineEditServidor.text())
            if self.cliente.open:
                if self.call.comboBoxModo.currentIndex() == 1:
                    modo = 0    # normal
                else:
                    modo = 8    # invisível
                retorno = self.cliente.autenticar(self.call.lineEditSenha.text().strip(), self.call.lineEditNickname.text().strip(), self.call.lineEditNomeReal.text().strip(), modo)

                # se ja tiver algum nick com o nome digitado:
                if retorno == "nickError":
                    self.throw_message_box("Atenção", "O nickname digitado já está em uso.")
                    self.call.lineEditNickname.setFocus()
                    self.call.lineEditNickname.setText("")
                elif retorno == "semBurstWelcome":
                    self.throw_message_box("Erro", "Não foi possível se conectar ao servidor.")
                    self.call.lineEditServidor.setText("")
                    self.call.lineEditServidor.setFocus()
                else:
                    self.abre_lista_channels()
                    
            else:    
                self.throw_message_box("Erro", "Não foi possível se conectar ao servidor.")
                self.call.lineEditServidor.setText("")
                self.call.lineEditServidor.setFocus()



if __name__ == "__main__":
    app = TelaAutenticacao()