from PyQt5 import QtWidgets, uic
from datetime import datetime
from Cliente import *
from TelaChat import *
from Pilha import *

class TelaEscolhaCanal:
    def __init__(self, app, cliente):
        self.app = app
        self.cliente = cliente
        self.call=uic.loadUi(r"interfaces\ModeloListaChats.ui")

        self.call.tableWidgetCanais.setColumnWidth(0, 136)
        self.call.tableWidgetCanais.setColumnWidth(1, 40)
        self.call.tableWidgetCanais.setColumnWidth(2, 205)

        self.call.itemSelectionChanged.connect(self.action_row_clicked)
        self.call.lineEditPesquisar.setPlaceholderText("Pesquise por um canal ou usuário")
        
        self.call.pushButtonEntrarPesquisa.clicked.connect(self.action_entrar_pesquisa)
        self.call.lineEditPesquisar.returnPressed.connect(self.action_entrar_pesquisa)

        self.call.carregarTabela()

        self.call.show()


    def carregarTabela(self):
        # ALTERAR MÉTODO
        # quando getChanneList estiver pronto
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
                chat = TelaChat(self.app, self.cliente, canal)
                pilha_telas.append(self)
                self.call.hide()
            else:
                aviso = QtWidgets.QMessageBox()
                aviso.setIcon(QtWidgets.QMessageBox.Information)
                aviso.setText("Atenção")
                aviso.setWindowTitle("Selecione um canal para entrar!")
                aviso.exec_()
        except:
            aviso = QtWidgets.QMessageBox()
            aviso.setIcon(QtWidgets.QMessageBox.Warning)
            aviso.setText("Erro inesperado")
            aviso.setWindowTitle("Não foi possível se conectar.")
            aviso.exec_()

    def action_voltar(self):
        self.call.hide()
        pilha_telas.pop().call.show()


    def action_row_clicked(self):
        return self.call.tableWidgetCanais.currentRow()
    

    def action_entrar_pesquisa(self):
        pass