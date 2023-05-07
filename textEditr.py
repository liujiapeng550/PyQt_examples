from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenu, QAction
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # 添加右键菜单
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.show_context_menu)

        # 添加复制操作
        copy_action = QAction('复制', self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.text_edit.copy)
        self.addAction(copy_action)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        copy_action = menu.addAction('复制')
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.text_edit.copy)
        menu.exec_(self.text_edit.viewport().mapToGlobal(pos))


if __name__ == '__main__':
    app = QApplication([])
    main_win = MainWindow()
    main_win.show()
    app.exec_()