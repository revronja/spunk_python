from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QPlainTextEdit

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


import requests

authToken = ""


class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.username = QtWidgets.QLineEdit(self)
        self.password = QtWidgets.QLineEdit(self)
        self.password.setEchoMode(self.password.Password)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.login_handler)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.buttonLogin)

    def login_handler(self):
        global authToken
        url = "https://10.0.0.62:8089/services/auth/login"
        data = {"username":self.username.text(),
        "password":self.password.text()}
        r = requests.post(url, data=data, verify=False)
        if r.ok:
            self.accept()
            #print(r.content)
            root = ET.fromstring(r.content)
            myElement = root.find('sessionKey')
            authToken = myElement.text

        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')

   

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle('MainWindow')
        self.statusBar()
        self.home() 
    """
    This function could be seen as initUI(self)
    """
    def home(self):

        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)

        self.btn = QPushButton('quit', self)
        self.btn.clicked.connect(self.close_application)

        self.btn.resize(self.btn.sizeHint())
        self.btn.move(0, 100)

        self.btn3 = QPushButton('submit', self)
        self.btn3.move(15,75)
        self.btn3.clicked.connect(self.submit)
        self.btn3.resize(self.btn3.sizeHint())
        
        # Add textview 
        self.tv = QPlainTextEdit(self)
        self.tv.move(400,20)
        self.tv.resize(100,250)
        self.tv.textChanged.connect(self.submit)
        #self.tv.setLineWrapMode(self.tv.LineWrapMode)
        #self.tv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.tv.setPlainText()

        self.show()   

    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'A message goes here', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")

    def submit(self):
        # get textbox text
        textboxText = self.textbox.text()
        # TO-DO : 
        # check null, print to label
        

        url = "https://10.0.0.62:8089/services/search/jobs"
        auth_str = "Splunk {}".format(authToken)
        headers = {
            "Authorization": auth_str
        }
        payload = {
            "search": textboxText
            #"search":"buttercupgames(error OR fail * OR severe"
        }
        r = requests.post(url, headers=headers, params=payload, verify=False)
        print(r.content)
        root = ET.fromstring(r.content)
        #print(root)
        myElement = root.find('sid')
        sid = myElement.text
        if r.ok:
           #print(r.status_code)
           QtWidgets.QMessageBox.warning(self, 'search created', str(r.status_code))
        else:
            print(authToken)
            QtWidgets.QMessageBox.warning(self, 'Error', str(r.status_code))


    def close_application(self):
        sys.exit()
    
    

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())