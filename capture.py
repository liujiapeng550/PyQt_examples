import sys
import pytesseract
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QDesktopWidget,QTextEdit,QAction,QMenu
from PyQt5.QtGui import QPixmap, QCursor, QPainter,QGuiApplication,QKeySequence
from PyQt5.QtCore import Qt, QPoint, QRect

class ScreenShot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        # 初始化界面
        self.initUI()
        
    def initUI(self):
        # 设置主窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 添加截屏按钮
        self.shotBtn = QPushButton('截屏', self)
        self.shotBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.shotBtn.setFixedSize(80, 30)
        self.shotBtn.clicked.connect(self.onShotBtnClicked)
        
        # 添加取消按钮
        self.cancelBtn = QPushButton('取消', self)
        self.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancelBtn.setFixedSize(80, 30)
        self.cancelBtn.clicked.connect(self.close)


        # 添加识别文字按钮
        self.ocrBtn = QPushButton('识别文字', self)
        self.ocrBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.ocrBtn.setFixedSize(80, 30)
        self.ocrBtn.clicked.connect(self.onOcrtexture)
        
        # 添加标签显示截屏图片
        self.imageLabel = QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        
        
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(10, 50, 620, 420)
        self.textEdit.hide()
        # 添加右键菜单
        self.textEdit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.textEdit.customContextMenuRequested.connect(self.show_context_menu)

        # 添加复制操作
        copy_action = QAction('复制', self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.textEdit.copy)
        self.addAction(copy_action)
        # 添加布局管理器
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.imageLabel)
        
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.shotBtn)
        self.hbox.addWidget(self.cancelBtn)
        self. hbox.addWidget(self.ocrBtn)
        self.hbox.addStretch(1)
        
        self.vbox.addLayout(self.hbox)
        
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)
        self.setCentralWidget(self.widget)
        self.setGeometry(0, 0, QDesktopWidget().screenGeometry().width(), QDesktopWidget().screenGeometry().height()-200)

    def onOcrtexture(self):
        self.textEdit.show()
        # 打开图片
        self.new_window = QWidget()
        layout = QVBoxLayout()
        self.new_window.setLayout(layout)

        image = Image.open('screenshot.png')
        # 将图片转换成字符串
        text = pytesseract.image_to_string(image, lang='chi_sim')
        options = text.split('\n')
        self.textEdit.setPlainText('\n'.join(options))
        layout.addWidget(self.textEdit)
        #layout.addWidget(image)
        self.new_window.setWindowFlags(Qt.WindowStaysOnTopHint) # 设置新窗口始终在最前面
        self.new_window.show()
        QApplication.instance().exec_() 

    def show_context_menu(self, pos):
        menu = QMenu(self)
        copy_action = menu.addAction('复制')
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.text_edit.copy)
        menu.exec_(self.text_edit.viewport().mapToGlobal(pos))

    def onShotBtnClicked(self):
        # 隐藏截屏按钮和取消按钮
        self.shotBtn.hide()
        self.cancelBtn.hide()
        self.ocrBtn.hide()
        # 截取屏幕
        screen = QGuiApplication.primaryScreen()
        pixmap = screen.grabWindow(QApplication.desktop().winId())
        
        # 显示截屏图片
        #self.shotLabel.setPixmap(pixmap)
        self.imageLabel.setPixmap(pixmap)
        # 设置鼠标跟踪
        self.setMouseTracking(True)
        self.setCursor(QCursor(Qt.CrossCursor))
        
    def mousePressEvent(self, event):
        # 记录起始点
        self.startPoint = event.pos()
        self.endPoint = QPoint()
    
    def mouseMoveEvent(self, event):
        # 记录结束点
        self.endPoint = event.pos()
        
        # 绘制矩形框
        self.update()
        
    def mouseReleaseEvent(self, event):
        # 截取选中的矩形区域
        rect = QRect(self.startPoint, self.endPoint)
        pixmap = self.imageLabel.pixmap().copy(rect)
        pixmap.save('screenshot.png')
        # 显示截取的图片
        self.imageLabel.setPixmap(pixmap)
        
        # 显示截屏按钮和取消按钮
        self.shotBtn.setText('重新截屏')
        self.shotBtn.show()

        self.cancelBtn.show()
        self.ocrBtn.show()
        
        # 取消鼠标跟踪
        self.setMouseTracking(False)
        self.setCursor(QCursor(Qt.ArrowCursor))
        
    def paintEvent(self, event):
        # 绘制矩形框
        if not self.startPoint.isNull() and not self.endPoint.isNull():
            painter = QPainter(self)
            painter.setPen(Qt.red)
            painter.drawRect(QRect(self.startPoint, self.endPoint))
            painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScreenShot()
    window.show()
    sys.exit(app.exec_())
