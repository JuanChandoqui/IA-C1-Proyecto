import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtGui, QtCore
import Models.AG as sudoku

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Views/menu.ui', self)   
        self.setWindowIcon(QtGui.QIcon('./Resources/Images/sudoku_logo.png'))
        self.setWindowTitle("SUDOKU")
        self.pushButton_ResolverSudoku.clicked.connect(self.pushButtonSolveSudoku)

    def pushButtonSolveSudoku(self):
        list_Grid = sudoku.main()
        print(list_Grid)

        self.fillSudoku(list_Grid)


    def fillSudoku(self, list_Grid:list):
        Palette= QtGui.QPalette()

        for i in range(81):              
            getattr(self, "line_"+str(i)).setText(f'{list_Grid[i]}')
            getattr(self, "line_"+str(i)).setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
            Palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
            getattr(self, "line_"+str(i)).setPalette(Palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()

    try: 
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')