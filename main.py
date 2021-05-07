import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from interface import interface
import screen_rec


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 生成主框口
    MainWindow = QMainWindow()
    # 定义自己设计的ui
    ui = interface.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    fluid = screen_rec.run()
    # 向槽函数传递ui即可修改textEdit控件
    ui.pushButton.clicked.connect(lambda: fluid.all(ui))
    ui.comboBox.activated.connect(lambda: fluid._comboBox(str(ui.comboBox.currentIndex())))
    ui.checkBox.stateChanged.connect(lambda: fluid._checkBox(ui.checkBox.isChecked()))
    ui.checkBox_2.setChecked(True)
    ui.checkBox_2.stateChanged.connect(lambda: fluid._checkBox_2(ui.checkBox_2.isChecked()))
    sys.exit(app.exec_())
