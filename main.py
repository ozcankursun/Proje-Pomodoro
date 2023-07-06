from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sqlite3
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer

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
        self.addProjectButton.clicked.connect(self.addProject)
        self.addSubjectButton.clicked.connect(self.addSubject)
        self.errorTextProjectLabel.setText('')
        self.errorTextSubjectLabel.setText('')
        
        
    def addProject(self):
        conn= sqlite3.connect('data.db')
        curr= conn.cursor()
        project_name= self.addProjectInput.text()
        # Veritabanında proje adını sorgulama
        curr.execute("SELECT * FROM project WHERE project_name=?",(project_name,))
        result = curr.fetchone()
        
        if result is not None:
            self.errorTextProjectLabel.setText('Bu proje veritabanında mevcut.')
        else:
            # Proje bilgilerini veritabanına ekliyor.
            curr.execute("INSERT INTO project (project_name) VALUES (?)", (project_name,))
            conn.commit()
            self.errorTextProjectLabel.setText('Proje veritabanına eklendi.')
        # Veritabanı bağlantısını kapat
        conn.close()
        
        
    def addSubject(self):
        conn= sqlite3.connect('data.db')
        curr= conn.cursor()
        subject_name= self.addSubjectInput.text()
        # Veritabanında proje adını sorgulama
        curr.execute("SELECT * FROM subject WHERE subject_name=?",(subject_name,))
        result = curr.fetchone()
        
        if result is not None:
            self.errorTextSubjectLabel.setText('Bu subject veritabanında mevcut.')
        else:
            # Proje bilgilerini veritabanına ekliyor.
            curr.execute("INSERT INTO subject (subject_name) VALUES (?)", (subject_name,))
            conn.commit()
            self.errorTextSubjectLabel.setText('Subject veritabanına eklendi.')
        # Veritabanı bağlantısını kapat
        conn.close()
            

class PomodoroUI(QDialog):
    # kodlar neredeyse hazir
    #Yunus (Emre)
    def __init__(self):
        super(PomodoroUI,self).__init__()
        loadUi("./UI/pomodoro.ui",self)
        #self.taskInput.clicked.connect(self.taskInputClicked)
        # self.addTask.clicked.connect(self.addData) # !!!!!!!!!
        # self.doneButton.clicked.connect(self.succes)
        # self.labelAsNotFinishedButton.clicked.connect(self.fail)
        # self.goToMainMenuButton.clicked.connect(self.go_main_menu)
        self.startStopButton.clicked.connect(self.startTimer)

        self.timer = QTimer()
        self.timer.setInterval(1000)  # Her bir saniye için tetikleme
        self.timer.timeout.connect(self.updateTime)
        self.remainingTime = 25 * 60  # Başlangıçta 25 dakika

        #def taskInputClicked(self): #!!!!!!!
        #task = self.taskInput.text()



    #def addData(self):
    #     conn = sqlite3.connect('./data.db')
    #     curr = conn.cursor()
    
    #     # Kullanicinin girdigi task 'task' degiskenine atanir
    #     task = self.taskInput.text()

    #     # database'e ekleme islemi
    #     curr.execute("INSERT INTO tasks (task_name) VALUES (?)", (task,))
    
    #     # deigisklikler kaydedilip baglanti kapatilir
    #     conn.commit()
    #     conn.close()


    # def succes(self):
    #     conn = sqlite3.connect("database.db")
    #     cursor = conn.cursor()
    #     veri = True
    #     cursor.execute("INSERT INTO session (succes) VALUES (?)", (veri,))
    #     conn.commit()
    #     conn.close()

    # def fail(self):
    #     conn = sqlite3.connect("database.db")
    #     cursor = conn.cursor()
    #     veri = False
    #     cursor.execute("INSERT INTO session (succes) VALUES (?)", (veri,))
    #     conn.commit()
    #     conn.close()

    def startTimer(self):
        self.timer.start()
        
    def updateTime(self):
        self.remainingTime -= 1
        minutes = self.remainingTime // 60
        seconds = self.remainingTime % 60
        self.timeLabel.setText(f"{minutes:02d}:{seconds:02d}")
        
        if self.remainingTime == 0:
            self.timer.stop()
            print("Bolum tamamlandi.")


class ShortBreakUI(QDialog):
    def __init__(self):
        super(ShortBreakUI,self).__init__()
        loadUi("./UI/shortBreak.ui",self)
        self.goToMainMenuButton.clicked.connect(self.go_main_menu)
        self.startButton.clicked.connect(self.startTimer)

        self.timer = QTimer()
        self.timer.setInterval(1000)  # Her bir saniye için tetikleme
        self.timer.timeout.connect(self.updateTime)
        self.remainingTime = 5 * 60  # 5 dakika olmasi icin

class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI,self).__init__()
        loadUi("./UI/longBreak.ui",self)


app = QApplication(sys.argv)
UI = PomodoroUI() # This line determines which screen you will load at first

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
