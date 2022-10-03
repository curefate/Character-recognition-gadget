from PyQt5 import QtCore, QtGui, QtWidgets


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, MainWindow, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.ui = MainWindow
        self.createMenu()

    def createMenu(self):
        self.setToolTip('おなかすいたなの！')
        self.menu = QtWidgets.QMenu()

        self.showAction = QtWidgets.QAction("显示主界面", self, triggered=self.show_window)
        self.P2TAction = QtWidgets.QAction("识别印刷体文字", self, triggered=self.ui.on_print_to_text)
        self.H2TAction = QtWidgets.QAction("识别手写体文字", self, triggered=self.ui.on_hand_to_text)
        self.TOFAction = QtWidgets.QAction("识别公式", self, triggered=self.ui.on_to_formula)
        self.quitAction = QtWidgets.QAction("关闭程序", self, triggered=self.quit)

        self.menu.addAction(self.showAction)
        self.menu.addAction(self.P2TAction)
        self.menu.addAction(self.H2TAction)
        self.menu.addAction(self.TOFAction)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)

        # 设置图标
        self.setIcon(QtGui.QIcon('asset/icon2.png'))
        #self.icon = self.MessageIcon()
        # 把鼠标点击图标的信号和槽连接
        self.activated.connect(self.onIconClicked)

    def show_window(self):
        # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        self.ui.showNormal()
        self.ui.activateWindow()

    def quit(self):
        self.ui.tray = None
        QtWidgets.qApp.quit()

    # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
    def onIconClicked(self, reason):
        if reason == 2 or reason == 3:
            # self.showMessage("Message", "skr at here", self.icon)
            if self.ui.isMinimized() or not self.ui.isVisible():
                # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                self.ui.showNormal()
                self.ui.activateWindow()
                self.ui.setWindowFlags(QtCore.Qt.Window)
                self.ui.show()
            else:
                # 若不是最小化，则最小化
                self.ui.showMinimized()
                self.ui.setWindowFlags(QtCore.Qt.SplashScreen)
                self.ui.show()
