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

# 问题：在类中用函数修改实例变量，只在函数内部有效，函数外实例变量未被修改？
# 原因：起初以为是作用域问题。但是修改的是实例变量，应该不会出错。后来发现每次触发信号与槽机制后都会执行一次__init__中的代码
# 解决：在__main__入口处实例化对象，在信号与槽中使用对象的属性传送信号

# 问题：在另一个类中定义的函数类型为str？
# 因为在另一个类中实例变量和函数名重复

# 问题：checkBox_2不论是否勾选，输出的结果总是False
# 原因：复制代码的时候忘记把槽函数checkBox改成checkBox_2