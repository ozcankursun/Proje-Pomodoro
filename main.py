from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sqlite3
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class LoginUI(QDialog):
    
    def __init__(self):
        super(LoginUI,self).__init__()
        loadUi("./UI/login.ui",self)
        self.signUpButton.clicked.connect(self.createuserfunc)
        # This is example of changing screen
        self.loginButton.clicked.connect(self.go_main_menu)
        
     
    def createuserfunc(self):
        conn= sqlite3.connect('./data.db')
        curr= conn.cursor()   
        #name ve email adresleri kullanicidan alinir ve bir degiskene atanir
        name = self.nameInputSignUp.text()
        email = self.emailInputSignUp.text()
        if '@' not in email or name =='' or email =='':
            self.errorTextSignUp.setText('Lütfen geçerli bir email adresi giriniz.')            
        else:                   
            curr.execute('SELECT email FROM User WHERE email =?',(email,))   
            if curr.fetchone() is not None:
                self.errorTextSignUp.setText('Bu email adresi daha once alinmis.')
            else:
                curr.execute('INSERT INTO User (Name, Email) VALUES (?,?)',(name, email))
                conn.commit()
                print('Hesap olusturuldu')
            
    def go_main_menu(self):
        conn= sqlite3.connect('data.db')
        curr= conn.cursor()
        userx = self.emailInputLogin.text()
        if len(userx)!=0:
            curr.execute('SELECT COUNT(*) FROM User WHERE email =?',(userx,))   
            count= curr.fetchone()[0]
            curr.close()
            conn.close()         
            if count > 0:
                print('Başarılı bir şekilde giriş yapıldı.')
                main_menu = MainMenuUI()
                widget.addWidget(main_menu)
                widget.setCurrentIndex(widget.currentIndex()+1)
            else: 
                self.errorTextLogin.setText('Bir hesabınız yoksa kayıt olunuz.')
        else:
            self.errorTextLogin.setText('Lütfen geçerli bir email adresi giriniz.')  
           
class MainMenuUI(QDialog):
    #Bunu yapacagiz (Ozcan)
    def __init__(self):
        super(MainMenuUI,self).__init__()
        loadUi("./UI/mainMenu.ui",self)

class PomodoroUI(QDialog):
    #bu kisim bana ait
    #Yunus (Emre)
    def __init__(self):
        super(PomodoroUI,self).__init__()
        loadUi("./UI/pomodoro.ui",self)


class ShortBreakUI(QDialog):
    def __init__(self):
        super(ShortBreakUI,self).__init__()
        loadUi("./UI/shortBreak.ui",self)

class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI,self).__init__()
        loadUi("./UI/longBreak.ui",self)


app = QApplication(sys.argv)
UI = LoginUI() # This line determines which screen you will load at first

# You can also try one of other screens to see them.
    # UI = MainMenuUI()
    # UI = PomodoroUI()
    # UI = ShortBreakUI()
    # UI = LongBreakUI()

widget = QtWidgets.QStackedWidget()
widget.addWidget(UI)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.setWindowTitle("Time Tracking App")
widget.show()
sys.exit(app.exec_())
