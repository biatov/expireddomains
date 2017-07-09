from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QLineEdit, QFileDialog, QApplication, QPushButton)
import csv
import sys


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        btn1 = QPushButton("Browse+Convert", self)
        btn1.setStatusTip('Выбор файла csv + автоматическая конвертация.')
        btn1.move(250, 20)

        btn1.clicked.connect(self.showDialog)
        self.textbox = QLineEdit(self)
        self.textbox.setStatusTip('Ввод названия файла txt. Например: simple.')
        self.textbox.move(20, 20)
        self.textbox.resize(220, 30)
        self.statusBar()
        self.resize(370, 70)
        self.center()
        self.setWindowTitle('CSV to TXT file')
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showDialog(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/')[0]
        txt_file_name = self.textbox.text()
        if txt_file_name:
            try:
                with open(fname, newline='') as file:
                    text_reader = csv.reader(file)
                    data = list()
                    for row in text_reader:
                        data.append(row[0].split(';')[5].replace('"', ''))

                txt_file = open('%s.txt' % txt_file_name, 'w')
                for item in data[1:]:
                    txt_file.write("%s\n" % item)
                txt_file.close()
            except:
                pass
        else:
            pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
