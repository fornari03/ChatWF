from PyQt5 import QtWidgets, uic
from datetime import datetime
from Cliente import *
from TelaChat import *

class TelaEscolhaCanal:
    def __init__(self, app, cliente):
        self.app = app
        self.cliente = cliente
        self.call=uic.loadUi(r"interfaces\ModeloListaChats.ui")

        self.call.tableWidgetCanais.setColumnWidth(0, 136)
        self.call.tableWidgetCanais.setColumnWidth(1, 40)
        self.call.tableWidgetCanais.setColumnWidth(2, 205)

        self.call.itemSelectionChanged.connect(self.action_row_clicked)


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
        # ADICIONAR PILHA
        linha = self.action_row_clicked()
        try:
            if linha != -1:
                canal = self.channels[linha]
                chat = TelaChat(self.app, self.cliente, canal)
                self.call.hide()
            else:
                popup = QtWidgets.QMessageBox()
                popup.setIcon(QtWidgets.QMessageBox.Information)
                popup.setText("Atenção")
                popup.setWindowTitle("Selecione um canal para entrar!")
                popup.exec_()
        except:
            popup = QtWidgets.QMessageBox()
            popup.setIcon(QtWidgets.QMessageBox.Warning)
            popup.setText("Erro inesperado")
            popup.setWindowTitle("Não foi possível se conectar.")
            popup.exec_()

    def action_voltar(self):
        # chama a pilha
        pass


    def action_row_clicked(self):
        return self.call.tableWidgetCanais.currentRow()