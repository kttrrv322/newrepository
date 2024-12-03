import sqlite3
import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication
from release.main_form import Ui_Form
from release.addEditCoffeeForm import Ui_Dialog
from PyQt6.QtWidgets import QWidget, QTableWidgetItem


class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.con = sqlite3.connect("D:/MyPythonProjects/PythonProject2/data/coffee.sqlite")
        self.ui.pushButton.clicked.connect(self.add_edit_item)
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffe ORDER BY id").fetchall()
        self.ui.tableWidget.setRowCount(len(result))
        self.ui.tableWidget.setColumnCount(len(result[0]))
        titles = [description[0] for description in cur.description]
        self.ui.tableWidget.setHorizontalHeaderLabels(titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def add_edit_item(self):
        self.new_window = QtWidgets.QDialog()
        self.ui_window = Ui_Dialog()
        self.ui_window.setupUi(self.new_window)
        self.new_window.show()
        self.ui_window.pushButton.clicked.connect(self.add_item)
        self.ui_window.pushButton_2.clicked.connect(self.edit_item)

    def add_item(self):
        if self.ui_window.textEdit.toPlainText():
            self.ui_window.con = sqlite3.connect("D:/MyPythonProjects/PythonProject2/data/coffee.sqlite")
            cur = self.ui_window.con.cursor()
            try:
                elements = list(map(lambda x: x.strip(), self.ui_window.textEdit.toPlainText().split(sep='_')))
                elements[-1] = int(elements[-1])
                elements[-2] = int(elements[-2])
                elements[0] = int(elements[0])
                elements = tuple(elements)
                if len(elements) == 7 and elements[0] in list(
                        map(lambda x: x[0], cur.execute('''SELECT id FROM coffe WHERE name LIKE "%"''').fetchall())):
                    raise BufferError
                cur.execute('''INSERT INTO coffe VALUES (?, ?, ?, ?, ?, ?, ?)''', elements)
                self.ui_window.con.commit()
                self.ui_window.con.close()
                cur = self.con.cursor()
                result = cur.execute("SELECT * FROM coffe ORDER BY id").fetchall()
                self.ui.tableWidget.setRowCount(len(result))
                self.ui.tableWidget.setColumnCount(len(result[0]))
                titles = [description[0] for description in cur.description]
                self.ui.tableWidget.setHorizontalHeaderLabels(titles)
                for i, elem in enumerate(result):
                    for j, val in enumerate(elem):
                        self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            except BufferError:
                self.ui_window.textEdit.setText('Такой индекс уже существует')
            except Exception:
                self.ui_window.textEdit.setText('Ошибка ввода')
            self.new_window.close()
        else:
            self.ui_window.textEdit.setText('Введите данные')

    def edit_item(self):
        if self.ui_window.textEdit.toPlainText():
            self.ui_window.con = sqlite3.connect("D:/MyPythonProjects/PythonProject2/data/coffee.sqlite")
            cur = self.ui_window.con.cursor()
            try:
                elements = list(map(lambda x: x.strip(), self.ui_window.textEdit.toPlainText().split(sep='_')))
                elements[-1] = int(elements[-1])
                elements[-2] = int(elements[-2])
                elements[0] = int(elements[0])
                elements = tuple(elements)
                if len(elements) == 7 and elements[0] not in list(
                        map(lambda x: x[0], cur.execute('''SELECT id FROM coffe WHERE name LIKE "%"''').fetchall())):
                    raise BufferError
                cur.execute('''DELETE FROM coffe WHERE id = ?''', (elements[0],))
                cur.execute('''INSERT INTO coffe VALUES (?, ?, ?, ?, ?, ?, ?)''', elements)
                self.ui_window.con.commit()
                self.ui_window.con.close()
                cur = self.con.cursor()
                result = cur.execute("SELECT * FROM coffe ORDER BY id").fetchall()
                self.ui.tableWidget.setRowCount(len(result))
                self.ui.tableWidget.setColumnCount(len(result[0]))
                titles = [description[0] for description in cur.description]
                self.ui.tableWidget.setHorizontalHeaderLabels(titles)
                for i, elem in enumerate(result):
                    for j, val in enumerate(elem):
                        self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            except BufferError:
                self.ui_window.textEdit.setText('Такого индекса не существует')
            except Exception:
                self.ui_window.textEdit.setText('Ошибка ввода')
            self.new_window.close()
        else:
            self.ui_window.textEdit.setText('Введите данные')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
