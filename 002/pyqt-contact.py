from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import json
import os


class myApp(QMainWindow):
    def __init__(self):
        super(myApp, self).__init__()
        self.open = open("data_contact.json", "r")
        self.userContact = json.loads(self.open.read())
        self.mainUI()
        self.mainLayout()
        self.setCentralWidget(self.mainWidget)
        self.menuBars()
        self.setMenuBar(self.menu)
        self.setFixedSize(350, 300)
        self.toolBars()
        self.addToolBar(self.toolBar)

    def mainUI(self):
        self.firstTabs = firstTab()
        self.secondTabs = secondTab()
        self.thirdTabs = thirdTab()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.firstTabs, "Contact")
        self.tabs.addTab(self.secondTabs, "Favorite")
        self.tabs.addTab(self.thirdTabs, "Add Contact")

    def toolBars(self):
        self.toolBar = QToolBar()
        button_tools = QAction(QIcon("icon/contact.png"), "Help", self)
        self.toolBar2 = QToolBar()
        button_tools = QAction(QIcon("icon/contact.png"), "Help", self)
        self.toolBar.addAction(button_tools)
        button_tools.triggered.connect(self.popupHelp)
        self.toolBar2.addAction(button_tools)
        button_tools.triggered.connect(self.popupHelp)

    def popupHelp(self):
        msg_pop = "PyQT Contact Help Center!"
        QMessageBox.information(self, "Help Center", msg_pop)

    def menuBars(self):
        self.menu = self.menuBar()
        test = self.menu.addMenu("File")
        test2 = self.menu.addMenu("App")
        test.addAction("Tentang Aplikasi")
        test2.addAction("Contact Book List")

    def mainLayout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.layout)


# Show Data Contact
class firstTab(QWidget):
    def __init__(self):
        super(firstTab, self).__init__()
        self.dataFavorite = {}
        self.open = open("data_contact.json", "r")
        self.userContact = json.loads(self.open.read())
        self.FavoriteTable()
        self.mainUI()
        self.setLayout(self.layout)

    def mainUI(self):
        self.btnAddFavorite = QPushButton("Add to Favorite")
        self.btnAddFavorite.clicked.connect(self.addToFavorite)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tablePlaces)
        self.layout.addWidget(self.btnAddFavorite)

    # add favorite in list
    def addToFavorite(self):
        for i in self.userContact:
            if self.dataFavorite['nama'] == i['nama']:
                i['favorite'] = 1
        toJson = json.dumps(self.userContact, indent=4)
        fwrite = open('data_contact.json', 'w')
        fwrite.write(toJson)

    # fetch favorite in list
    def fetchFavorite(self, row, column):
        favoriteData = []
        rwf = row
        clf = column
        for x in range(len(self.head)):
            res = self.tablePlaces.item(int(rwf), int(x)).text()
            favoriteData.append(res)
        for i in self.userContact:
            if favoriteData[0] == i['nama']:
                self.dataFavorite.update(i)

    # Logic to Favorite Tabs
    def FavoriteTable(self):
        self.head = ["name", "phone number"]
        row = len(list(self.userContact))
        self.tablePlaces = QTableWidget()
        self.tablePlaces.setRowCount(row)
        self.tablePlaces.setColumnCount(len(self.head))
        for row in range(len(self.userContact)):
            for col in range(len(self.head)):
                if col == 0:
                    self.tablePlaces.setItem(
                        row, col, QTableWidgetItem(self.userContact[row]["nama"]))
                elif col == 1:
                    self.tablePlaces.setItem(row, col, QTableWidgetItem(
                        self.userContact[row]["nomor_hp"]))

        self.tablePlaces.setHorizontalHeaderLabels(self.head)

        self.tablePlaces.cellClicked.connect(self.fetchFavorite)


# Add to Favorite Contact List
class secondTab(QWidget):
    def __init__(self):
        super(secondTab, self).__init__()
        self.open = open("data_contact.json", "r")
        self.userContact = json.loads(self.open.read())
        self.dataFavorite = {}
        self.favoriteContact()
        self.mainUI()
        self.setLayout(self.layout)

    def mainUI(self):
        self.btnDeleteFavorite = QPushButton("Delete favorite Contact")
        self.btnDeleteFavorite.clicked.connect(self.deleteFromfavorite)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableFavs)
        self.layout.addWidget(self.btnDeleteFavorite)

    # get from mainUI
    def favoriteContact(self):
        self.head = ["name", "phone number"]
        self.contactFav = list(
            filter(lambda a: a["favorite"] == 1, self.userContact))
        row = len(self.contactFav)
        self.tableFavs = QTableWidget()
        self.tableFavs.setRowCount(row)
        self.tableFavs.setColumnCount(len(self.head))
        for row in range(len(self.contactFav)):
            for col in range(len(self.head)):
                if col == 0:
                    self.tableFavs.setItem(row, col, QTableWidgetItem(
                        self.contactFav[row]["nama"]))
                elif col == 1:
                    self.tableFavs.setItem(row, col, QTableWidgetItem(
                        self.contactFav[row]["nomor_hp"]))

        self.tableFavs.setHorizontalHeaderLabels(self.head)
        self.tableFavs.cellClicked.connect(self.fetchFavorite)

    # fetch favorite in list
    def fetchFavorite(self, row, column):
        favoriteData = []
        rw = row
        cl = column
        for x in range(len(self.head)):
            res = self.tableFavs.item(int(rw), int(x)).text()
            favoriteData.append(res)
        for i in self.userContact:
            if favoriteData[0] == i['nama']:
                self.dataFavorite.update(i)

    # delete favorite if click nama in list
    def deleteFromfavorite(self):
        for i in self.userContact:
            if self.dataFavorite['nama'] == i['nama']:
                i['favorite'] = 0
        toJson = json.dumps(self.userContact, indent=4)
        fwrite = open('data_contact.json', 'w')
        fwrite.write(toJson)

# Add New Contact to Contact List


class thirdTab(QWidget):
    def __init__(self):
        super(thirdTab, self).__init__()
        self.mainUI()
        self.setLayout(self.layout)
        self.open = open("data_contact.json", "r")
        self.userContact = json.loads(self.open.read())

    # logic add
    def mainUI(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Set Name")
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setPlaceholderText("Set Phone Number")
        self.buttonAdd = QPushButton("Add To Contact List")
        self.buttonAdd.clicked.connect(self.addContact)
        self.lineEdit.returnPressed.connect(self.addContact)
        self.lineEdit2.returnPressed.connect(self.addContact)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.lineEdit2)
        self.layout.addWidget(self.buttonAdd)

    # get from MainUI

    def addContact(self):
        name = self.lineEdit.text()
        phone = self.lineEdit2.text()
        params = {"nama": name, "nomor_hp": phone, "favorite": 0}
        self.userContact.append(params)
        toJson = json.dumps(self.userContact, indent=4)
        fwrite = open('data_contact.json', 'w')
        fwrite.write(toJson)


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


if __name__ == "__main__":
    app = QApplication([])
    window = myApp()
    window.setWindowTitle("PyQt5 Contact")
    window.show()
    sys.exit(app.exec_())
