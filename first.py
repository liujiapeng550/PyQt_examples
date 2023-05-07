import sys
import os
import pytesseract
from PIL import ImageGrab
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTextEdit
from PyQt5.QtGui import QPixmap

class OCRTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('OCR Tool')
        self.setGeometry(100, 100, 640, 480)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 640, 480)

        self.button = QPushButton('Capture', self)
        self.button.setGeometry(10, 10, 100, 30)
        self.button.clicked.connect(self.capture)

        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(10, 50, 620, 420)

    def capture(self):
        im = ImageGrab.grab()
        im.save('capture.png')
        self.label.setPixmap(QPixmap('capture.png'))

        text = pytesseract.image_to_string(im)
        options = text.split('\n')
        self.textEdit.setPlainText('\n'.join(options))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ocr = OCRTool()
    ocr.show()
    sys.exit(app.exec_())
