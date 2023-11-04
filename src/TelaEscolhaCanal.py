from PyQt5 import QtWidgets, uic
from datetime import datetime
from Cliente import *
from TelaChat import *
from Pilha import *

class TelaEscolhaCanal:
    def __init__(self, app, cliente):
        self.app = app
        self.cliente = cliente
        try:
            self.call=uic.loadUi(r"interfaces\ModeloListaChats.ui")
        except:
            self.call=uic.loadUi(r"src\interfaces\ModeloListaChats.ui")

        self.call.tableWidgetCanais.setColumnWidth(0, 130)
        self.call.tableWidgetCanais.setColumnWidth(1, 40)
        self.call.tableWidgetCanais.setColumnWidth(2, 205)

        self.call.pushButtonEntrar.clicked.connect(self.action_entrar)
        self.call.pushButtonCriar.clicked.connect(self.action_criar)
        self.call.lineEditCriar.returnPressed.connect(self.action_criar)
        self.call.lineEditPesquisar.setPlaceholderText("Pesquise por um canal ou usuário")
        self.call.lineEditCriar.setPlaceholderText("Nome do canal a ser criado")

        self.call.tableWidgetCanais.setStyleSheet("""
            QTableWidget::item {
                padding: 5px;
                font-size: 14px;
            }

            QTableWidget::item:selected {
                background-color: #0074D9;
                color: #FFFFFF;
            }
        """)

        self.call.tableWidgetCanais.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

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

        self.call.pushButtonEntrarPesquisa.setStyleSheet("""
            QPushButton#pushButtonEntrarPesquisa {
                background-color: #0074D9;
                color: #FFFFFF; 
                border: 2px solid #0056b3; 
                border-radius: 5px; 
                padding: 5px 15px;
                font-size: 10px;
                font-weight: bold;
            }
                                                 
            QPushButton#pushButtonEntrarPesquisa:hover {
                background-color: #0056b3;
                color: #FFFFFF;
                border: 2px solid #003f7f;
            }
        """)

        self.call.pushButtonCriar.setStyleSheet("""
            QPushButton#pushButtonCriar {
                background-color: #0074D9;
                color: #FFFFFF; 
                border: 2px solid #0056b3; 
                border-radius: 5px; 
                padding: 5px 15px;
                font-size: 10px;
                font-weight: bold;
            }
                                                 
            QPushButton#pushButtonCriar:hover {
                background-color: #0056b3;
                color: #FFFFFF;
                border: 2px solid #003f7f;
            }
        """)

        self.call.pushButtonEntrar.setStyleSheet("""
            QPushButton#pushButtonEntrar {
                background-color: #0074D9;
                color: #FFFFFF; 
                border: 2px solid #0056b3; 
                border-radius: 5px; 
                padding: 5px 15px;
                font-size: 14px;
                font-weight: bold;
            }
                                                 
            QPushButton#pushButtonEntrar:hover {
                background-color: #0056b3;
                color: #FFFFFF;
                border: 2px solid #003f7f;
            }
        """)

        self.call.pushButtonEntrarPesquisa.clicked.connect(self.action_entrar_pesquisa)
        self.call.lineEditPesquisar.returnPressed.connect(self.action_entrar_pesquisa)
        self.call.pushButtonVoltar.clicked.connect(self.action_voltar)

        self.carregarTabela()

        self.call.show()


    def carregarTabela(self):
        self.channels = self.cliente.getChannelList()
        self.call.tableWidgetCanais.setRowCount(len(self.channels))
        for row, channel in enumerate(self.channels):
            self.call.tableWidgetCanais.setItem(row, 0, QtWidgets.QTableWidgetItem(channel[0]))
            self.call.tableWidgetCanais.setItem(row, 1, QtWidgets.QTableWidgetItem(str(channel[1])))
            self.call.tableWidgetCanais.setItem(row, 2, QtWidgets.QTableWidgetItem(channel[2]))

        

    def action_entrar(self):
        linha = self.action_row_clicked()
        try:
            if linha != -1:
                canal = self.channels[linha]
                self.cliente.joinChannel(canal)
                self.chat = TelaChat(self.app, self.cliente, canal)
                pilha_telas.append(self)
                self.call.hide()
            else:
                aviso = QtWidgets.QMessageBox()
                aviso.setIcon(QtWidgets.QMessageBox.Information)
                aviso.setText("Selecione um canal para entrar!")
                aviso.setWindowTitle("Atenção")
                aviso.exec_()
        except:
            aviso = QtWidgets.QMessageBox()
            aviso.setIcon(QtWidgets.QMessageBox.Warning)
            aviso.setText("ENão foi possível se conectar.")
            aviso.setWindowTitle("Erro inesperado")
            aviso.exec_()


    def action_voltar(self):
        self.call.hide()
        self.cliente.quit()
        pilha_telas.pop().call.show()


    def action_row_clicked(self):
        return self.call.tableWidgetCanais.currentRow()
    

    def action_entrar_pesquisa(self):
        encontrou = False
        for channel in self.channels:
            if channel[0] == self.call.lineEditPesquisar.text():
                if self.cliente.joinChannel(channel[0]) == "nomeCanalInvalido":
                    aviso = QtWidgets.QMessageBox()
                    aviso.setIcon(QtWidgets.QMessageBox.Warning)
                    aviso.setText("Nome do canal inválido!")
                    aviso.setWindowTitle("Atenção")
                    aviso.exec_()
                    self.call.lineEditPesquisar.setText("")
                    self.call.lineEditPesquisar.setFocus()

                else:
                    self.chat = TelaChat(self.app, self.cliente, channel)
                    pilha_telas.append(self)
                    self.call.hide()
                    encontrou = True

        # se nao encontrou um canal, procura o usuário
        if not encontrou:
            if False:
                pass

            else:
                aviso = QtWidgets.QMessageBox()
                aviso.setIcon(QtWidgets.QMessageBox.Warning)
                aviso.setText("Canal ou usuário não encontrado!")
                aviso.setWindowTitle("Atenção")
                aviso.exec_()


    def action_criar(self):
        if self.cliente.joinChannel(self.call.lineEditCriar.text()) == "nomeCanalInvalido":
            aviso = QtWidgets.QMessageBox()
            aviso.setIcon(QtWidgets.QMessageBox.Warning)
            aviso.setText("Nome do canal inválido!")
            aviso.setWindowTitle("Atenção")
            aviso.exec_()
            self.call.lineEditCriar.setText("")
            self.call.lineEditCriar.setFocus()

        else:
            canal = (self.call.lineEditCriar.text(), 1, "Welcome")
            self.chat = TelaChat(self.app, self.cliente, canal)
            pilha_telas.append(self)
            self.call.hide()