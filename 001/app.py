from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QProgressBar, QPushButton, QSlider, QInputDialog, QListView, QButtonGroup, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt, QAbstractListModel
import sys


class ListModels(QAbstractListModel):
    def __init__(self, datalist=""):
        super(ListModels, self).__init__()
        self.datalists = datalist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            text = self.datalists[index.row()]
            return text

    def rowCount(self, index):
        return len(self.datalists)


class MainList(QMainWindow):
    def __init__(self):
        super(MainList, self).__init__()
        self.Vlayout = QVBoxLayout()
        self.mainUI()
        self.setLayout()
        self.setWidget()
        self.setCentralWidget(self.Widget)
        # self.progBar.setValue(self.model.datalists.count())

    def mainUI(self):
        self.listView()
        self.buttonAdd = QPushButton("Add")
        self.buttonAdd.clicked.connect(self.addDataList)
        self.buttonRemove = QPushButton("Remove")
        self.buttonRemove.clicked.connect(self.removeDataList)
        self.buttonUpdate = QPushButton("Update")
        self.buttonUpdate.clicked.connect(self.updateDataList)
        self.buttonClear = QPushButton("Clear")
        self.buttonClear.clicked.connect(self.clearDataList)
        self.buttonDuplicate = QPushButton("Duplicate")
        self.buttonDuplicate.clicked.connect(self.duplicateDataList)
        self.mes = QMessageBox()
        self.progBar = QProgressBar()
        self.slider = QSlider(Qt.Horizontal)

    def listView(self):
        self.list = QListView()
        self.model = ListModels()
        self.model = ListModels(datalist=[])
        self.list.setModel(self.model)

    def addDataList(self):
        add, ok = QInputDialog.getText(self.Widget, "Tambah Data", "")
        if len(add):
            self.model.datalists.append(add)
            self.model.layoutChanged.emit()

        self.progBar.setValue(len(self.model.datalists))

    def updateDataList(self):
        selectedIndex = self.list.selectedIndexes()
        if selectedIndex:
            data, ok = QInputDialog.getText(
                self.Widget, "Perbaharui Data", "Masukkan data terbaru")
            if len(data):
                selectedIndexes = selectedIndex[0]
                self.model.datalists[selectedIndexes.row()] = data
                self.model.layoutChanged.emit()
        else:
            self.mes.information(self, "Warning", "Silakan pilih data dulu!")

        self.progBar.setValue(len(self.model.datalists))

    def removeDataList(self):
        selectedIndex = self.list.selectedIndexes()
        if selectedIndex:
            selectedIndexes = selectedIndex[0]
            del self.model.datalists[selectedIndexes.row()]
            self.model.layoutChanged.emit()
        else:
            self.mes.information(
                self, "Warning", "Silakan pilih data dulu!")

        self.progBar.setValue(len(self.model.datalists))

    def clearDataList(self):
        self.model.datalists.clear()
        self.model.layoutChanged.emit()
        self.progBar.setValue(len(self.model.datalists))

    def duplicateDataList(self):
        selectedIndex = self.list.selectedIndexes()
        valueSlider = self.slider.value()
        if selectedIndex:
            selectedIndexes = selectedIndex[0]
            for x in range(valueSlider):
                self.model.datalists.append(
                    self.model.datalists[selectedIndexes.row()])
                self.model.layoutChanged.emit()
        else:
            self.mes.information(
                self, "Warning", "Silakan pilih data dulu!")
        self.progBar.setValue(len(self.model.datalists))

    def set_width(self):
        widget = QWidget()
        layoutHorizontal = QHBoxLayout()
        layoutHorizontal.addWidget(self.list)
        layoutHorizontal.addWidget(self.setBtnLayout())
        widget.setLayout(layoutHorizontal)
        return widget

    def setLayout(self):
        self.Vlayout.addWidget(self.set_width())
        self.Vlayout.addWidget(self.progBar)
        self.Vlayout.addWidget(self.slider)

    def setBtnLayout(self):
        btnWidget = QWidget()
        Vlayout = QVBoxLayout()
        Vlayout.addWidget(self.buttonAdd)
        Vlayout.addWidget(self.buttonUpdate)
        Vlayout.addWidget(self.buttonRemove)
        Vlayout.addWidget(self.buttonDuplicate)
        btnWidget.setLayout(Vlayout)
        return btnWidget

    def setWidget(self):
        self.Widget = QWidget()
        self.Widget.setLayout(self.Vlayout)


if __name__ == "__main__":
    app = QApplication([])
    window = MainList()
    window.show()
    window.setWindowTitle("List Model App")
    app.exec_()
