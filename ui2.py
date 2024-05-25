import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QFileDialog, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from dsl.InterpreterJSON import *
from dsl.InterpreterDSL import *

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'File Format Selector'
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 240
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QVBoxLayout()

        # Заголовок "Choose file format"
        self.label = QLabel('Choose file format:')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Горизонтальный layout для радиокнопок
        hbox = QHBoxLayout()
        self.radio_json = QRadioButton('JSON')
        self.radio_dsl = QRadioButton('DSL')
        hbox.addWidget(self.radio_json)
        hbox.addWidget(self.radio_dsl)
        layout.addLayout(hbox)

        # Кнопка "Open File"
        self.btn_open = QPushButton('Open File', self)
        self.btn_open.clicked.connect(self.openFileNameDialog)
        layout.addWidget(self.btn_open)

        # Метка для отображения состояния файла
        self.file_label = QLabel('No file selected')
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setStyleSheet("color: red;")
        layout.addWidget(self.file_label)

        # Кнопка "Open Logs File"
        self.btn_open_logs = QPushButton('Open Logs File', self)
        self.btn_open_logs.clicked.connect(self.openLogsFileNameDialog)
        layout.addWidget(self.btn_open_logs)

        # Метка для отображения состояния файла журналов
        self.logs_file_label = QLabel('No logs file selected')
        self.logs_file_label.setAlignment(Qt.AlignCenter)
        self.logs_file_label.setStyleSheet("color: red;")
        layout.addWidget(self.logs_file_label)

        # Кнопка "Find Antipatterns"
        self.btn_find = QPushButton('Find Antipatterns', self)
        self.btn_find.setEnabled(False)  # Кнопка недоступна, пока не выбраны оба файла
        self.btn_find.clicked.connect(self.findAntipatternsAction)
        layout.addWidget(self.btn_find)

        self.setLayout(layout)
        
        self.file_selected = False
        self.logs_file_selected = False
        self.file_path = None
        self.logs_file_path = None

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;JSON Files (*.json);;DSL Files (*.dsl)", options=options)
        if fileName:
            if self.radio_json.isChecked():
                self.file_label.setText(f'Selected JSON file: {fileName}')
                self.file_label.setStyleSheet("color: green;")
                self.file_selected = True
            elif self.radio_dsl.isChecked():
                self.file_label.setText(f'Selected DSL file: {fileName}')
                self.file_label.setStyleSheet("color: green;")
                self.file_selected = True
            else:
                QMessageBox.warning(self, "Warning", "Please select a file format.")
            self.file_path = fileName
        else:
            self.file_label.setText('No file selected')
            self.file_label.setStyleSheet("color: red;")
            self.file_selected = False
            self.file_path = None

        self.updateFindButtonState()

    def openLogsFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Log Files (*.log)", options=options)
        if fileName:
            self.logs_file_label.setText(f'Selected logs file: {fileName}')
            self.logs_file_label.setStyleSheet("color: green;")
            self.logs_file_selected = True
            self.logs_file_path = fileName
        else:
            self.logs_file_label.setText('No logs file selected')
            self.logs_file_label.setStyleSheet("color: red;")
            self.logs_file_selected = False
            self.logs_file_path = None

        self.updateFindButtonState()

    def updateFindButtonState(self):
        if self.file_selected and self.logs_file_selected:
            self.btn_find.setEnabled(True)
        else:
            self.btn_find.setEnabled(False)
    
    def findAntipatternsAction(self):
        selected_format = "JSON" if self.radio_json.isChecked() else "DSL" if self.radio_dsl.isChecked() else "None"
        if selected_format == "JSON":
            interpretator = Interpretator(file=self.file_path, logs_path=self.logs_file_path)
            interpretator.run()
        elif selected_format == "DSL":
            interpretator = InterpreterDSL(self.file_path, self.logs_file_path)
            interpretator.run()
        QMessageBox.information(self, "Success", "Report successfully generated")
        


        # Здесь можно добавить логику для обработки файлов и поиска антипаттернов

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
