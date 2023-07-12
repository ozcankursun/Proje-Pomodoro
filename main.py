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
    def __init__(self):
        super(PomodoroUI,self).__init__()
        loadUi("./UI/pomodoro.ui",self)
        self.tur = 0
        self.bitis = 4
        self.addTask.clicked.connect(self.addData)
        self.doneButton.clicked.connect(self.succes)
        self.labelAsNotFinishedButton.clicked.connect(self.fail)
        self.goToMainMenuButton.clicked.connect(self.main)


        self.tur = 0
        self.bitis = 4
        while self.tur<4:
            self.tur += 1  # Increment the current break cycle
            print(self.tur)
            
            self.startStopButton.clicked.connect(self.startTimer)
        
        
        #self.tasksCombo.clicked.connect(self.drop_down_menu) 

        self.timer = QTimer()
        self.timer.setInterval(1000)  # Her bir saniye için tetikleme
        self.timer.timeout.connect(self.updateTime)
        self.remainingTime = 1 * 3 # Başlangıçta 25 dakika

        # self.tur= 0
        # self.bitis= 4
    
    def main(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def addData(self):
        conn= sqlite3.connect('data.db')
        curr= conn.cursor()
        task_name= self.taskInput.text()
        # Veritabanında proje adını sorgulama
        curr.execute("SELECT * FROM project WHERE project_name=?",(task_name,))
        result = curr.fetchone()


        if result is not None:
            self.errorTextProjectLabel.setText('Bu proje veritabanında mevcut.')
        else:
            # Proje bilgilerini veritabanına ekliyor.
            curr.execute("INSERT INTO project (project_name) VALUES (?)", (task_name,))
            conn.commit()
            self.errorTextProjectLabel.setText('Proje veritabanına eklendi.')
        # Veritabanı bağlantısını kapat
        conn.close()


    def succes(self):
        conn = sqlite3.connect("database.db")
        curr = conn.cursor()
        veri = True
        curr.execute("INSERT INTO session (succes) VALUES (?)", (veri,))
        conn.commit()
        conn.close()

    def fail(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        veri = False
        cursor.execute("INSERT INTO session (succes) VALUES (?)", (veri,))
        conn.commit()
        conn.close()

    

    def startTimer(self):
        self.timer.start()
        print(self.tur)
       
        
    
    def updateTime(self):
        self.remainingTime -= 1
        minutes = self.remainingTime // 60
        seconds = self.remainingTime % 60
        self.timeLabel.setText(f"{minutes:02d}:{seconds:02d}")
        

        if self.remainingTime == 0:
            self.timer.stop()
            print("Bölüm tamamlandı.")
            

            if self.tur == self.bitis:
                self.go_to_long_break()
            else:
                self.go_to_short_break()



    # def startTimer(self):
    #     self.tur= 4
    #     self.timer.start()
    #     #self.tur -= 1
        
    # def updateTime(self):
    #     self.remainingTime -= 1
    #     minutes = self.remainingTime // 60
    #     seconds = self.remainingTime % 60
    #     self.timeLabel.setText(f"{minutes:02d}:{seconds:02d}")
        
        # if self.remainingTime == 0 and self.tur==self.bitis:
        #     self.timer.stop()
        #     print("Bolum tamamlandi.")
        #     self.go_to_long_break() #go_to_long_break
        # else:
        #     self.go_to_short_break()

        # if self.remainingTime == 0:
        #     self.timer.stop()
        #     print("Bölüm tamamlandı.")
        #     self.tur -=1
        #     if self.tur == 0:
        #         self.go_to_long_break()
        #     else:
        #         self.go_to_short_break()
        # else:
        #     self.go_to_short_break()




    def go_to_long_break(self):
        long_break_page = LongBreakUI()
        widget.addWidget(long_break_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_to_short_break(self):
        short_break_page = ShortBreakUI()
        widget.addWidget(short_break_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

        


class ShortBreakUI(QDialog):
    def __init__(self):
        super(ShortBreakUI,self).__init__()
        loadUi("./UI/shortBreak.ui",self)
        self.setWindowTitle("Short Break")
        self.goToMainMenuButton.clicked.connect(self.go_to_main_menu)
        self.skipButton.clicked.connect(self.skip)
        self.startButton.clicked.connect(self.startTimer)
        

        self.timer = QTimer()
        self.timer.setInterval(1000)  # Her bir saniye için tetikleme
        self.timer.timeout.connect(self.updateTime)
        self.remainingTime = 1 * 3  # 5 dakika olmasi icin


    def go_to_main_menu (self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def skip (self):
        pomodoro_page= PomodoroUI ()
        widget.addWidget(pomodoro_page)
        widget.setCurrentIndex(widget.currentIndex() +1)
    
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
            self.pomodoro()

    def pomodoro(self):
        pomodoro_page= PomodoroUI()
        widget.addWidget(pomodoro_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

            

class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI,self).__init__()
        loadUi("./UI/longBreak.ui",self)
        self.goToMainMenuButton.clicked.connect(self.go_to_main_menu)
        self.skipButton.clicked.connect(self.pomodoro_page)
        self.startButton.clicked.connect(self.startTimer)

        self.timer = QTimer()
        self.timer.setInterval(1000)  # Her bir saniye için tetikleme
        self.timer.timeout.connect(self.updateTime)
        self.remainingTime = 1 * 3  # 5 dakika olmasi icin

    def go_to_main_menu(self):
        main= MainMenuUI()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def pomodoro_page(self):
        pomodoro= PomodoroUI()
        widget.addWidget(pomodoro)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
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
            self.pomodoro_page()

    



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