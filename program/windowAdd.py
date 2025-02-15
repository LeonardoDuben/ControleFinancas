from PySide6.QtWidgets import (QWidget, QGridLayout, QLabel, QLineEdit,
                               QPushButton)
from utils import valueName,checkNum, currentDate, connectClicked
from csv_ import File
from windowsW import WindowError, WindowDialog
from typing import Callable
import sqlite3


class AddWindow(QWidget):
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)



        # Conectar ao banco de dados
        self.conn = sqlite3.connect('financas.db')
        self.cursor = self.conn.cursor()

        # Criar tabela, caso não exista
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS financas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nomeDoGasto TEXT NOT NULL,
                valor FLOAT,
                data TEXT
            )
        ''')
        self.conn.commit()

        # Configurações
        self.setWindowTitle(f"Adicionar")
        layout = QGridLayout()
        self.setLayout(layout)
        self.file = File()    
        self.resize(450, 100)

        # Widgets da janela
        self.textoAdd = QLabel('Nome do gasto:')
        self.displayName = QLineEdit()
        self.textoValor = QLabel('Valor do gasto:')
        self.displayValue = QLineEdit()
        self.confirmed = QPushButton('Confirmar')

        # Configurações dos widgets

        # Conexões
        connectClicked(self.confirmed, lambda: self.addExpense())

        # Adicionar ao layout
        layout.addWidget(self.textoAdd, 0, 0)
        layout.addWidget(self.displayName, 0, 1)
        layout.addWidget(self.textoValor, 1, 0)
        layout.addWidget(self.displayValue, 1, 1)
        layout.addWidget(self.confirmed, 2, 1)
        

    def addExpense(self) -> None:
        nome: str = self.displayName.text()
        valor: str = self.displayValue.text()
        self.displayName.clear()
        self.displayValue.clear()

        chkNum: bool = checkNum(valor)
        chkValues: bool = valueName(nome, valor)

        if not chkNum:
            self.showError('Valor inválido!')
            return
        
        if chkValues:
            self.file.add([{'Data' : f'{currentDate}',
                                     'Nome' : f'{nome}', 
                                     'Valor' : f'R${float(valor):.2f}'}])
            try:
                self.cursor.execute(
                    'INSERT INTO financas (nomeDoGasto, valor, data) VALUES (?, ?, ?)',
                    (nome, float(valor), currentDate)
                )
                self.conn.commit()
                self.showDialog('Gasto adicionado com sucesso!')
            except Exception as e:
                self.showError(f'Erro ao salvar no banco: {e}')
            return
        self.showError('Você não digitou algum dos campos')

    def showError(self, msg: str) -> None:
        self.windowError = WindowError(msg)
        self.windowError.show()
    
    
    def showDialog(self, msg: str) -> None:
        self.windowError = WindowDialog(msg)
        self.windowError.show()
