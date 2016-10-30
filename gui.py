
from from_archive import ArchiveParser

import sys
from PyQt4.QtGui import *
from exporters import * 

a = QApplication(sys.argv)


class MainWindow(QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.target = None

    def export(self):
        filename = QFileDialog.getExistingDirectory(self, 'Open File', '/')
        print(filename)

    def load_archive(self):
        self.archiver = ArchiveParser(QFileDialog.getExistingDirectory(w, 'Open File', '/'))
        self.search_box.setEnabled(True)
        self.exp_txt_btn.setEnabled(True)
        self.list_widget.clear()
        self.persons = self.archiver.get_candidates(self.search_box.text())
        for l in self.persons:
            self.list_widget.addItem(l["name"])
    
    def get_candidates(self, text):
        self.list_widget.clear()
        self.persons = self.archiver.get_candidates(self.search_box.text())
        for l in self.persons:
            self.list_widget.addItem(l["name"])

    def set_candidate(self, c):
        self.target = self.persons[c]["thread"]

    def export(self):
        if self.target != None:
            filename = QFileDialog.getSaveFileName(self, 'Select output file', '~')
            exporter = TextExporter(filename=filename)
            self.archiver.export_messages(self.target, exporter)
        else:
            QMessageBox.information(self, "Select target", "You need to select target", "OK").show()
        

    def initUI(self):
        self.resize(200,200)
        self.setWindowTitle("Facebook export messages from archive")


        self.load_btn = QPushButton('Load archive', self)
        self.load_btn.clicked.connect(self.load_archive)

        self.search_box = QLineEdit(self)
        self.search_box.setEnabled(False)
        self.search_box.textChanged.connect(self.get_candidates)

        hl = QHBoxLayout()
        hl.addWidget(self.load_btn)
        hl.addWidget(self.search_box)

        # Now we add footer with export buttons 
        self.exp_txt_btn = QPushButton("Export as text", self)
        self.exp_txt_btn.setEnabled(False)
        self.exp_txt_btn.clicked.connect(self.export)
        hl2 = QHBoxLayout()
        hl2.addStretch(1)
        hl2.addWidget(self.exp_txt_btn)

        self.list_widget = QListWidget(self)
        self.list_widget.currentRowChanged.connect(self.set_candidate)


        vl = QVBoxLayout()
        vl.addLayout(hl)
        vl.addWidget(self.list_widget)
        vl.addLayout(hl2)

        self.setLayout(vl)

        self.show()

w = MainWindow()


sys.exit(a.exec_())
