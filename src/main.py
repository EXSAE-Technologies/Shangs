from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QToolBar,
    QStyle
)
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import os

class mainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Shangs Browser")
        self.source_dir = os.path.abspath(os.path.dirname(__file__))
        self.setWindowIcon(QIcon(os.path.join(self.source_dir, "images/s.svg")))

        self.browser = QWebEngineView()

        navtab = QToolBar("Navigation")
        navtab.setIconSize(QSize(16,16))
        self.addToolBar(navtab)

        back_btn = QAction(QIcon(os.path.join(self.source_dir, "images/left-arrow.svg")),"Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        navtab.addAction(back_btn)

        forward_btn = QAction(QIcon(os.path.join(self.source_dir, "images/right-arrow.svg")),"Forward", self)
        forward_btn.setStatusTip("Forward to next page")
        forward_btn.triggered.connect(self.browser.forward)
        navtab.addAction(forward_btn)

        reload_btn = QAction(QIcon(os.path.join(self.source_dir, "images/refresh.svg")),"Reload", self)
        reload_btn.setStatusTip("Reload current page")
        reload_btn.triggered.connect(self.browser.reload)
        navtab.addAction(reload_btn)
        
        home_btn = QAction(QIcon(os.path.join(self.source_dir, "images/home.svg")),"Homepage", self)
        home_btn.setStatusTip("Go to home page")
        home_btn.triggered.connect(self.navigate_home)
        navtab.addAction(home_btn)
        
        self.httpsicon = QAction(QIcon(os.path.join(self.source_dir, "images/lock-open.svg")),"SSL", self)
        self.httpsicon.setStatusTip("Secure connection")
        navtab.addAction(self.httpsicon)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_url)
        navtab.addWidget(self.url_bar)
        
        stop_btn = QAction(QIcon(os.path.join(self.source_dir, "images/cancel.svg")),"Stop", self)
        stop_btn.setStatusTip("Stop")
        stop_btn.triggered.connect(self.browser.stop)
        navtab.addAction(stop_btn)

        file_menu = self.menuBar().addMenu("&File")
        
        open_file_action = QAction(QIcon(os.path.join(self.source_dir, "images/html-file.svg")),"Open", self)
        open_file_action.setStatusTip("Open local file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)
        
        save_file_action = QAction(QIcon(os.path.join(self.source_dir, "images/save.svg")),"Save", self)
        save_file_action.setStatusTip("Save to local file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        self.browser.setUrl(QUrl("https://google.com"))
        self.setCentralWidget(self.browser)

        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.loadFinished.connect(self.update_title)
    
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Hypertext Markup Language (*.html *.html);;" "All files (*.*)")
        if filename:
            self.browser.setUrl(QUrl(filename))

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "", "Hypertext Markup Language (*.htm *.html);;" "All files (*.*)")
        if filename:
            self.browser.page().save(filename)

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("Shangs Browser: %s" % title)
    
    def update_url_bar(self, q):
        if q.scheme() == "https":
            self.httpsicon.setIcon(QIcon(os.path.join(self.source_dir, "images/lock-closed.svg")))
        else:
            self.httpsicon.setIcon(QIcon(os.path.join(self.source_dir, "images/lock-open.svg")))
        
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)
    
    def navigate_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)
    
    def navigate_home(self):
        self.browser.setUrl(QUrl("https://google.com"))

app = QApplication(sys.argv)
window = mainWindow()
window.show()
app.exec_()
