import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic


form_class = uic.loadUiType("C:\\Users\\memo_practice.ui")[0]   # ui 경로


class WindowSearch(QDialog):
    def __init__(self, parent):
        super(WindowSearch, self).__init__(parent)
        uic.loadUi("C:\\Users\\Dialog.ui", self)    # ui 경로
        self.show()
        
        self.p = parent # 부모 메인윈도우

class WindowClass(QMainWindow, form_class): # 메인윈도우, ui경로
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 메뉴바 '파일' 연결
        self.action_open.triggered.connect(self.openFunction)
        self.action_save.triggered.connect(self.saveFunction)
        self.action_saveAs.triggered.connect(self.saveAsFunction)
        self.action_close.triggered.connect(self.close) # close 이벤트 연결
        
        # 메뉴바 '편집' 연결
        self.action_selectAll.triggered.connect(self.select_all)
        self.action_cut.triggered.connect(self.cut)
        self.action_search.triggered.connect(self.searchFunction)
        
        self.Fname = '제목 없음'
        self.edit_Fname = ''
        
        
    def closeEvent(self, event):    # 종료시 이벤트 발생
        ret = self.save_changed_data()
        print("close!!")
        if ret == 2:    # 반환값이 2(취소)일시 
            event.ignore() # 이벤트 취소
            
    def save_changed_data(self):
        msgBox = QMessageBox()  # 창 종료시 closeEvent -> save_change_data 함수 실행, 메세지 박스 띄우기
        msgBox.setText('변경 내용을 \'{}\'에 저장하시겠습니까?' .format(self.Fname))
        msgBox.setWindowTitle("hi all")
        msgBox.addButton('저장', QMessageBox.YesRole)   # 0 반환
        msgBox.addButton('저장하지 않음', QMessageBox.NoRole)   # 1
        msgBox.addButton('취소', QMessageBox.RejectRole)    # 2
        ret = msgBox.exec_()
        return ret  # 0, 1, 2 반환
        
# 메뉴 파일저장
    def openFunction(self):
        try: 
            self.Fname = QFileDialog.getOpenFileName(self)[0]
            with open(self.Fname, encoding='utf8') as f:
                data = f.read()
            self.plainTextEdit.setPlainText(data)
            self.edit_Fname = self.Fname
            print('open!')
        except:
            pass
            self.Fname = self.edit_Fname
        
    def saveFunction(self):
        try:
            if self.Fname == '제목 없음':
                self.Fname = QFileDialog.getSaveFileName(self)[0]
            data = self.plainTextEdit.toPlainText()
            with open(self.Fname, 'w', encoding='utf8') as f:
                f.write(data)
            self.edit_Fname = self.Fname
            print('save!')
        except:
            pass
            self.Fname = self.edit_Fname
        
    def saveAsFunction(self):
        try:
            self.Fname = QFileDialog.getSaveFileName(self)[0]
            data = self.plainTextEdit.toPlainText()
            with open(self.Fname, 'w', encoding='utf8') as f:
                f.write(data)
            self.edit_Fname = self.Fname
            print('save as!')
        except:
            pass
            self.Fname = self.edit_Fname
            
# 메뉴 편집
    def cut(self):
        self.plainTextEdit.cut()
        
    def select_all(self):
        self.plainTextEdit.selectAll()
        
    def searchFunction(self):
        WindowSearch(self)

app = QApplication(sys.argv)
mainWindow = WindowClass()
mainWindow.show()
app.exec_()
