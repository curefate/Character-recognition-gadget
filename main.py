import os
import sys
import qdarkstyle
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow

os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    mw = MainWindow()
    sys.exit(app.exec_())
