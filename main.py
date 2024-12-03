import sqlite3
import sys
import io
from enum import UNIQUE

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem

template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>968</width>
    <height>688</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QTableWidget" name="tableWidget">
   <property name="geometry">
    <rect>
     <x>50</x>
     <y>90</y>
     <width>871</width>
     <height>491</height>
    </rect>
   </property>
  </widget>
  <widget class="QTextEdit" name="textEdit">
   <property name="geometry">
    <rect>
     <x>50</x>
     <y>50</y>
     <width>871</width>
     <height>41</height>
    </rect>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton">
   <property name="geometry">
    <rect>
     <x>390</x>
     <y>580</y>
     <width>241</width>
     <height>51</height>
    </rect>
   </property>
   <property name="text">
    <string>Добавить</string>
   </property>
  </widget>
  <widget class="QLabel" name="label">
   <property name="geometry">
    <rect>
     <x>120</x>
     <y>10</y>
     <width>701</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>Через пробел введите id, название сорта, степень обжарки, молотый/в зернах, описание вкуса, цена, объем упаковки</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        design = io.StringIO(template)
        uic.loadUi(design, self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.add_item)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.modified = {}
        self.titles = None
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffe").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        titles = [description[0] for description in cur.description]
        self.tableWidget.setHorizontalHeaderLabels(titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def add_item(self):
        if self.textEdit.toPlainText():
            cur = self.con.cursor()
            try:
                elements = self.textEdit.toPlainText().split()
                elements[-1] = int(elements[-1])
                elements[-2] = int(elements[-2])
                elements[0] = int(elements[0])
                elements = tuple(elements)
                if len(elements) == 7 and elements[0] in list(
                        map(lambda x: x[0], cur.execute('''SELECT id FROM coffe WHERE name LIKE "%"''').fetchall())):
                    raise BufferError
                cur.execute('''INSERT INTO coffe VALUES (?, ?, ?, ?, ?, ?, ?)''', elements)
                self.con.commit()
                result = cur.execute("SELECT * FROM coffe").fetchall()
                self.tableWidget.setRowCount(len(result))
                self.tableWidget.setColumnCount(len(result[0]))
                titles = [description[0] for description in cur.description]
                self.tableWidget.setHorizontalHeaderLabels(titles)
                for i, elem in enumerate(result):
                    for j, val in enumerate(elem):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            except BufferError:
                self.textEdit.setText('Такой индекс уже существует')
            except Exception:
                self.textEdit.setText('Ошибка ввода')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
