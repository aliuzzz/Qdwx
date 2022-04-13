import sys
import ctypes
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget
from Ui_mtrtools import Ui_MainWindow  #导入你写的界面类
 
class MyMainWindow(QMainWindow,Ui_MainWindow): #这里也要记得改
    def __init__(self,parent =None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  #设置任务栏图标
    myWin.show()
    sys.exit(app.exec_())    