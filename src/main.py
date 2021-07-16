from PyQt5.QtGui import QIcon, QMovie, QPainter, QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QLineEdit,
    QMainWindow,
    QSplashScreen,
    QTabWidget,
    QToolBar
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

        self.tabs = QTabWidget()
        self.homepageUrl = QUrl("https://google.com")

        navtab = QToolBar("Navigation")
        navtab.setIconSize(QSize(16,16))
        self.addToolBar(navtab)

        back_btn = QAction(QIcon(os.path.join(self.source_dir, "images/left-arrow.svg")),"Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtab.addAction(back_btn)

        forward_btn = QAction(QIcon(os.path.join(self.source_dir, "images/right-arrow.svg")),"Forward", self)
        forward_btn.setStatusTip("Forward to next page")
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtab.addAction(forward_btn)

        reload_btn = QAction(QIcon(os.path.join(self.source_dir, "images/refresh.svg")),"Reload", self)
        reload_btn.setStatusTip("Reload current page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
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
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtab.addAction(stop_btn)

        add_tab_action = QAction(QIcon(os.path.join(self.source_dir, "images/add-boxed.svg")), "Add", self)
        add_tab_action.setStatusTip("Add tab")
        add_tab_action.triggered.connect(lambda: self.add_new_tab(QUrl("https://google.com")))
        navtab.addAction(add_tab_action)

        file_menu = self.menuBar().addMenu("&File")
        
        open_file_action = QAction(QIcon(os.path.join(self.source_dir, "images/html-file.svg")),"Open", self)
        open_file_action.setStatusTip("Open local file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)
        
        save_file_action = QAction(QIcon(os.path.join(self.source_dir, "images/save.svg")),"Save", self)
        save_file_action.setStatusTip("Save to local file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)
        
        print_to_pdf_action = QAction(QIcon(os.path.join(self.source_dir, "images/pdf.svg")),"Print to PDF", self)
        print_to_pdf_action.setStatusTip("Print to pdf file")
        print_to_pdf_action.triggered.connect(self.print_to_pdf)
        file_menu.addAction(print_to_pdf_action)

        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.setIconSize(QSize(16,16))
        self.setCentralWidget(self.tabs)

        self.anim = QMovie()
        self.anim.setFileName(os.path.join(self.source_dir, "images/loading.gif"))
        self.anim.frameChanged.connect(self.set_tab_icon_loading)

        self.add_new_tab(self.homepageUrl)
    
    def set_tab_icon_loading(self):
        self.anim.start()
        self.tabs.setTabIcon(self.tabs.currentIndex(), QIcon(self.anim.currentPixmap()))

    def current_tab_changed(self,i):
        browser = self.tabs.currentWidget()
        self.update_url_bar(browser)
        self.update_title(browser)
    
    def close_current_tab(self,i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)
    
    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl == None:
            qurl = self.homepageUrl
        
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, QIcon(os.path.join(self.source_dir, "images/web.svg")), label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda: self.update_url_bar(browser))
        browser.loadStarted.connect(self.anim.start)
        browser.loadFinished.connect(lambda: self.update_title(browser))
    
    def print_to_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Print to PDF", "", "PDF (*.pdf*)")
        if filename:
            browser = self.tabs.currentWidget()
            browser.page().printToPdf(filename)
    
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Hypertext Markup Language (*.html *.html);;" "All files (*.*)")
        if filename:
            browser = self.tabs.currentWidget()
            browser.setUrl(QUrl(filename))

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "", "Hypertext Markup Language (*.htm *.html);;" "All files (*.*)")
        if filename:
            browser = self.tabs.currentWidget()
            browser.page().save(filename)

    def update_title(self, browser):
        title = browser.page().title()
        self.anim.stop()
        icon = browser.page().icon()
        if icon:
            self.tabs.setTabIcon(self.tabs.currentIndex(), QIcon(icon))

        self.setWindowTitle("Shangs Browser: %s" % title)
        self.tabs.setTabText(self.tabs.currentIndex(), title)
    
    def update_url_bar(self, browser):
        if browser == self.tabs.currentWidget():
            q = browser.url()
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

        browser = self.tabs.currentWidget()
        browser.setUrl(q)
    
    def navigate_home(self):
        browser = self.tabs.currentWidget()
        browser.setUrl(QUrl("https://google.com"))

if __name__ == "__main__":
    source_dir = os.path.abspath(os.path.dirname(__file__))

    app = QApplication(sys.argv)
    
    splash_pix = QPixmap(os.path.join(source_dir, "images/s.svg"))
    splash = QSplashScreen(splash_pix)
    splash.setMask(splash_pix.mask())
    splash.show()

    app.processEvents()

    window = mainWindow()
    window.show()
    splash.finish(window)
    app.exec_()
