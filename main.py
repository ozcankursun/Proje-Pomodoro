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
        #global userx 
        self.userx= self.emailInputLogin.text()
        LoginUI.userx=self.userx
        if len(self.userx)!=0:
            curr.execute('SELECT COUNT(*) FROM User WHERE email =?',(self.userx,))   
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
    
    # project_name=''
    # project_id=0
    # subject_name=''
    # subject_id=0
    def __init__(self):
        super(MainMenuUI,self).__init__()
        loadUi("./UI/mainMenu.ui",self)
       
        self.addProjectButton.clicked.connect(self.addProject)
        self.addSubjectButton.clicked.connect(self.addSubject)
        #self.addSubjectOnProjectCombo.clear()
        # self.showSummaryButton.clicked.connect(self.showSummary)
        # self.sendEmailThisSummaryButton.clicked.connect(self.sendEmailThisSummary)
        self.errorTextProjectLabel.setText('')
        self.errorTextSubjectLabel.setText('')
        self.startPomodoroButton.clicked.connect(self.startPomodoro)
        conn= sqlite3.connect('data.db')
        curr= conn.cursor()
        curr.execute("SELECT project_name FROM Project WHERE user_id_fk = (SELECT user_id_pk FROM User WHERE email = ?)", (LoginUI.userx,)
)
        result = curr.fetchall()
        result2=list(result)
        for re in result2:
            self.addSubjectOnProjectCombo.addItem(re[0])
            self.projectDeleteCombo.addItem(re[0])
            self.showSummaryProjectCombo.addItem(re[0])
            self.selectProjectCombo.addItem(re[0])
        
    # def showSummary(self):
    #     conn= sqlite3.connect('data.db')  
    #     curr= conn.cursor()
    #     sqlquery= 'SELECT create_date,start,finish,succes FROM session'
    #     tablerow=0
    #     for row in curr.execute(sqlquery):
    #         print(row)
    #         self.summaryTableValuesWidget.setItem(tablerow,0,QtWidgets.QsummaryTableValuesWidgetItem(row[0]))
    #         self.summaryTableValuesWidget.setItem(tablerow,1,QtWidgets.QsummaryTableValuesWidgetItem(row[0]))
    #         self.summaryTableValuesWidget.setItem(tablerow,2,QtWidgets.QsummaryTableValuesWidgetItem(row[0]))
    #         self.summaryTableValuesWidget.setItem(tablerow,3,QtWidgets.QsummaryTableValuesWidgetItem(row[0]))
    #         self.summaryTableValuesWidget.setItem(tablerow,4,QtWidgets.QsummaryTableValuesWidgetItem(row[0]))
            
    #         tablerow+=1
        # pass   
    def sendEmailThisSummary(self):
        pass
            
    def addProject(self):
        conn= sqlite3.connect('data.db')
        curr= conn.cursor()
        self.project_name= self.addProjectInput.text()
        MainMenuUI.project_name=self.project_name
        # Veritabanında proje adını sorgulama
        curr.execute("SELECT * FROM Project WHERE project_name=?",(self.project_name,))
        result = curr.fetchone()
        
        if len(self.project_name)==0:
            self.errorTextProjectLabel.setText('Bir project giriniz.')
        else:
            if result is not None:
                self.errorTextProjectLabel.setText('Bu proje veritabanında mevcut.')
            else:
                # Proje bilgilerini veritabanına ekliyor.
                curr.execute("SELECT user_id_pk FROM User WHERE email = ?",(LoginUI.userx,))
                
                self.emails= curr.fetchone()[0]
                #son= curr.execute(user_id_fk)
                curr.execute("INSERT INTO Project (project_name, user_id_fk) VALUES (?,?)", (self.project_name, self.emails ))
                
                conn.commit()
                
                self.addSubjectOnProjectCombo.addItem(self.project_name)
                self.projectDeleteCombo.addItem(self.project_name)
                self.showSummaryProjectCombo.addItem(self.project_name)
                self.selectProjectCombo.addItem(self.project_name)
                self.errorTextProjectLabel.setText('Proje veritabanına eklendi.')
        # Veritabanı bağlantısını kapat
        conn.close()
    
        
        
    def addSubject(self):
        conn= sqlite3.connect('data.db')
        curr= conn.cursor()
        self.subject_name= self.addSubjectInput.text()
        MainMenuUI.subject_name=self.subject_name
        # Veritabanında proje adını sorgulama
        curr.execute("SELECT * FROM Subject WHERE subject_name=?",(self.subject_name,))
        result = curr.fetchone()
        
        if len(self.subject_name)==0:
            self.errorTextSubjectLabel.setText('Bir subject giriniz.')
        else:
            if result is not None:
                self.errorTextSubjectLabel.setText('Bu subject veritabanında mevcut.')
            else:
                # Proje bilgilerini veritabanına ekliyor.
                #curr.execute("SELECT project_id_pk FROM Project WHERE project = ?",(userx,))
                #project= curr.fetchone()
                curr.execute("SELECT user_id_pk FROM User WHERE email = ?",(LoginUI.userx,))
                
                self.emails= curr.fetchone()[0]
                
                curr.execute("SELECT project_id_pk FROM Project WHERE email = ?",(LoginUI.userx,))
                
                self.emails2= curr.fetchone()[0]
                
                curr.execute("INSERT INTO Subject (project_id_fk,user_id_fk,subject_name) VALUES (?,?,?)", (self.emails, self.emails2, self.subject_name,))
                conn.commit()
                self.errorTextSubjectLabel.setText('Subject veritabanına eklendi.')
        # Veritabanı bağlantısını kapat
        conn.close()
    
    def startPomodoro(self):
        pomodoro_menu= PomodoroUI()
        widget.addWidget(pomodoro_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)     
        

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
