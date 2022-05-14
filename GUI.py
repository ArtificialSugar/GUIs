import sys
import cv2
import time
import sqlite3
import numpy as np
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QMainWindow, QApplication

# Sign In GUI
class Ui_SignIn(QDialog):
    def __init__(self):
        super(Ui_SignIn, self).__init__()
        loadUi("signin.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.go_to_register.clicked.connect(self.openUiVideo)
        self.contin.clicked.connect(self.validate_account)

    # Open register GUI
    def openUiRegister(self):
        self.usernamefield.setText("")
        self.passwordfield.setText("")
        register = Ui_Register()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    # Open video GUI
    def openUiVideo(self):
        widget.close()
        self.window = Ui_Video()
        self.window.show()

    # Validate username 
    def validate_account(self):
        user = self.usernamefield.text()
        password = self.passwordfield.text()
        conn = sqlite3.connect("accounts.db")
        c = conn.cursor()
        c.execute("SELECT * FROM account_details WHERE username =:u", {"u": user})
        try:
            account_values = c.fetchall()
            username = account_values[0][0]
            p = account_values[0][1]
        except:
            self.processinput.setText("Username not found")
        if account_values == []:
            self.processinput.setText("Invalid username or password")
        elif password != p:
            self.processinput.setText("Invalid username or password")
        elif len(user) == 0 or len(password) == 0:
            self.processinput.setText("Please fill in all boxes")
        elif user == username and password == p:
            self.openUiVideo()
        
            
# Register GUI
class Ui_Register(QDialog):
    def __init__(self):
        super(Ui_Register, self).__init__()
        loadUi("register.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.goback.clicked.connect(self.return_signin)
        self.signup.clicked.connect(self.validate_register)
        self.user = self.usernamefield.text()
        self.password = self.passwordfield.text()

    # Return to Sign in GUI
    def return_signin(self,_):
        self.usernamefield.setText("")
        self.passwordfield.setText("")
        self.processinput.setText("")
        self.genderfield.setText("")
        self.agefield.setText("")
        self.countryfield.setText("")
        self.cityfield.setText("")
        signin = Ui_SignIn()
        widget.addWidget(signin)
        widget.setCurrentIndex(widget.currentIndex()-1)
    
    # Validate registration info against database accounts
    def validate_register(self):
        user = self.usernamefield.text()
        password = self.passwordfield.text()
        gender = self.genderfield.text()
        age = self.agefield.text()
        country = self.countryfield.text()
        city = self.cityfield.text()
        conn = sqlite3.connect("accounts.db")
        c = conn.cursor()
        user_validate = c.execute("SELECT * FROM account_details WHERE username =:u", {"u": user})
        user_validate = c.fetchall()
        print(user_validate)
        try:
            user_validate = user_validate[0][0]
        except IndexError:
            pass
        conn.commit()
        conn.close()

        if len(user) == 0 or len(password) == 0 or len(gender) == 0 or len(age) == 0 or len(country) == 0 or len(city) == 0:
            self.processinput.setText("Please fill in all boxes")

        elif user == user_validate:
            self.processinput.setText("Username exists")
         
        else:
            conn = sqlite3.connect("accounts.db")
            c = conn.cursor()
            user_info = [user, password, gender, age, country, city]
            c.execute('INSERT INTO account_details (username, password, gender, age, country, city) VALUES (?,?,?,?,?,?)', user_info)
            self.processinput.setText("Account created")
            conn.commit()
            conn.close()

# Worker thread to control cam
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    end_pixmap_signal = pyqtSignal()
    fps_signal = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cam= cv2.VideoCapture(0, cv2.CAP_DSHOW)
        frame_time_1 = 0
        #time.sleep(.01)
        while self._run_flag:
            ret, cv_img = cam.read()
            time.sleep(.01)
            frame_time_2 = time.time()
            fps = (1/(frame_time_2-frame_time_1))
            frame_time_1 = frame_time_2
            fps = fps
            if ret:
                self.change_pixmap_signal.emit(cv_img)
                self.fps_signal.emit(int(fps))
        self.end_pixmap_signal.emit()

# Dashboard GUI
class Ui_Video(QMainWindow):
    def __init__(self):
        super(Ui_Video, self).__init__()
        loadUi("video.ui", self)
        print(cv2.__version__)
        self.setFixedWidth(775)
        self.setFixedHeight(550)
        self.setWindowTitle('Product Explorer')
        self.setWindowIcon(QtGui.QIcon('icons\gui\logo.ico'))
        self.display_width = 640
        self.display_height = 480
        self.stop_video.setEnabled(False)
        self.fps_label.setText("0")
        self.start_video.clicked.connect(self.start_feed)
        self.stop_video.clicked.connect(self.stop_feed)
            
    # Start video feed
    def start_feed(self):
        self.disp_fps = 0
        self.thread = QThread()
        self.worker = VideoThread()
        self.worker.moveToThread(self.thread)
        self.worker.change_pixmap_signal.connect(self.update_image)
        self.thread.started.connect(self.worker.run)
        self.worker.end_pixmap_signal.connect(self.thread.quit)
        self.worker.end_pixmap_signal.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.fps_signal.connect(self.display_fps)
        self.thread.start()
        self.start_video.setEnabled(False)
        self.stop_video.setEnabled(True)        

    # Update image_label with an img (cv or .png)
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        if self.worker._run_flag == False:
            self.image_label.setPixmap(QtGui.QPixmap())
        else:
            self.image_label.setPixmap(qt_img)

    # Convert cv img to QPixmap
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


    # Display FPS
    @pyqtSlot(int)
    def display_fps(self, n):
        if self.worker._run_flag:
            self.fps_label.setText(f"{n}")
        else:
            self.fps_label.setText("0")

    # Stop video feed
    def stop_feed(self):
        self.worker._run_flag = False
        self.start_video.setEnabled(True)
        self.stop_video.setEnabled(False)

# Program start and exit
app = QApplication(sys.argv)
signin = Ui_SignIn()
widget = QStackedWidget()
widget.addWidget(signin)
widget.setFixedHeight(800)
widget.setFixedWidth(376)
widget.setWindowTitle('Product Explorer')
widget.setWindowIcon(QtGui.QIcon('icons\gui\logo.ico'))
widget.show()
sys.exit(app.exec_())

