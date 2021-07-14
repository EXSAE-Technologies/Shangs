from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow
)
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

class mainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Shangs Browser")

        browser = QWebEngineView()
        browser.setUrl(QUrl("https://google.com"))
        self.setCentralWidget(browser)

app = QApplication(sys.argv)
window = mainWindow()
window.show()
app.exec_()
