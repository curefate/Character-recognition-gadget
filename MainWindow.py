import ScreenCapture
import Tray
import XF_H2T
import XF_TOF
import XF_P2T
import pyperclip

from enum import Enum, unique
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    class status(Enum):
        NONE = 0
        P2T = 1
        H2T = 2
        TOF = 3

    def __init__(self):
        super().__init__()
        self.initUI()

        # 截屏
        self.capture = ScreenCapture.SnippingWidget()
        self.capture.capture_done.connect(self.on_capture_done)
        # 托盘图标
        self.tray = Tray.TrayIcon(self)
        self.tray.show()
        # 状态枚举类
        self.myStatus = self.status.NONE
        # 调用讯飞
        self.tof = XF_TOF.Help()
        self.p2t = XF_P2T.Help()
        self.h2t = XF_H2T.Help()

        self.show()

    def initUI(self):
        # 设置主窗口相关
        self.setWindowTitle('Little Gadget')
        self.setWindowIcon(QtGui.QIcon('asset/icon3.png'))
        self.setFixedSize(350, 50)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowOpacity(0.9)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 中心组件
        self.centralWidget = QtWidgets.QWidget(self)

        # 设置按钮
        self.btn_print = QtWidgets.QPushButton('识别印刷体文字', self.centralWidget)
        self.btn_print.setToolTip('点击后截图印刷体文字，识别结果将复制进您的剪切板中')
        self.btn_print.clicked.connect(self.on_print_to_text)
        self.btn_hand = QtWidgets.QPushButton('识别手写体文字', self.centralWidget)
        self.btn_hand.clicked.connect(self.on_hand_to_text)
        self.btn_hand.setToolTip('点击后截图手写体文字，识别结果将复制进您的剪切板中')
        self.btn_formula = QtWidgets.QPushButton('识别公式', self.centralWidget)
        self.btn_formula.setToolTip('点击后截图公式，此公式的LATEX代码将会复制进您的剪切板中')
        self.btn_formula.clicked.connect(self.on_to_formula)

        # 设置布局
        self.layout_h = QtWidgets.QHBoxLayout(self.centralWidget)
        self.layout_h.addWidget(self.btn_print)
        self.layout_h.addWidget(self.btn_hand)
        self.layout_h.addWidget(self.btn_formula)

        # 设置中心组件
        self.setCentralWidget(self.centralWidget)

    @pyqtSlot()
    def on_print_to_text(self):
        self.myStatus = self.status.P2T
        self.capture.showFullScreen()
        QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
        self.hide()

    @pyqtSlot()
    def on_hand_to_text(self):
        self.myStatus = self.status.H2T
        self.capture.showFullScreen()
        QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
        self.hide()

    @pyqtSlot()
    def on_to_formula(self):
        self.myStatus = self.status.TOF
        self.capture.showFullScreen()
        QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
        self.hide()

    @pyqtSlot()
    def on_capture_done(self):
        self.show()
        str = ''
        if self.myStatus == self.status.TOF:
            str = self.tof.call_url()
        elif self.myStatus == self.status.P2T:
            str = self.p2t.call_url()
        elif self.myStatus == self.status.H2T:
            str = self.h2t.call_url()
        pyperclip.copy(str)

    # 用于控制最小化时的任务栏图标
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                event.ignore()
                self.setWindowFlags(QtCore.Qt.SplashScreen)
                return
            else:
                self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

    # 用于解决程序关闭后托盘图标不消失
    def closeEvent(self, event):
        self.tray = None
        QtWidgets.qApp.quit()
