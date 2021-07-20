import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

SERVER_URL = "http://localhost:8000"
COMPANY_URL = "http://atolmaker.me"

DEBUG = False

if DEBUG:
    ORIGIN_URL = SERVER_URL
else:
    ORIGIN_URL = COMPANY_URL

class NetworkBrowserWindow(QMainWindow):
    def __init__(self):
        super(NetworkBrowserWindow, self).__init__()
        self.AddressView = QWebEngineView()
        self.AddressView.JumpToOriginAddress = self.AddressViewJumpToOriginAddress
        self.AddressView.AddressViewChange = self.AddressViewChangePermitted
        self.CURRENT_ADDRESS_VIEW = ""
        self.REQUESTED_ADDRESS_VIEW = ""
        self.AddressViewJumpToOriginAddress()
        self.setCentralWidget(self.AddressView)
        self.setFixedWidth(960)
        self.setFixedHeight(720)
        self.show()

        # UX
        InputBox = QToolBar()
        self.addToolBar(InputBox)

        # Origin
        JumpToOriginAddressButton = QAction("Home", self)
        JumpToOriginAddressButton.triggered.connect(self.AddressView.JumpToOriginAddress)
        InputBox.addAction(JumpToOriginAddressButton)

        # Address box
        self.URL_Bar = QLineEdit()
        self.URL_Bar.returnPressed.connect(self.AddressViewChangeRequested)
        InputBox.addWidget(self.URL_Bar)

        # Reload
        ReloadAtAddressButton = QAction("Reload", self)
        ReloadAtAddressButton.triggered.connect(self.AddressView.reload)
        InputBox.addAction(ReloadAtAddressButton)

        # Forward
        HTMLBlockForwardButton = QAction("Forward", self)
        HTMLBlockForwardButton.triggered.connect(self.AddressView.forward)
        InputBox.addAction(HTMLBlockForwardButton)

        # Back
        HTMLBlockBackButton = QAction("Back", self)
        HTMLBlockBackButton.triggered.connect(self.AddressView.back)
        InputBox.addAction(HTMLBlockBackButton)

    def AddressViewChangeRequested(self):
        self.AddressViewGetInput()
        self.AddressViewChangePermitted()

    def AddressViewGetInput(self):
        self.REQUESTED_ADDRESS_VIEW = self.URL_Bar.text()

    def AddressViewChangePermitted(self):
        self.REQUESTED_ADDRESS_VIEW = self.URL_Bar.text()
        self.AddressView.setUrl(QUrl(self.REQUESTED_ADDRESS_VIEW))
        self.onAddressViewChange(self.REQUESTED_ADDRESS_VIEW)

    def AddressViewJumpToOriginAddress(self):
        self.AddressView.setUrl(QUrl(ORIGIN_URL))
        self.onAddressViewChange(ORIGIN_URL)

    def onAddressViewChange(self, URL):
        self.CURRENT_ADDRESS_VIEW = URL

NetworkBrowser = QApplication(sys.argv)
NetworkBrowser.setApplicationName("NetworkBrowser24")
NetworkBrowserObject = NetworkBrowserWindow()
NetworkBrowser.exec()
