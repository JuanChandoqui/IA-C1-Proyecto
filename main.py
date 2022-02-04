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
        self.label_analizando.setVisible(False)
        self.pushButton_ResolverSudoku.clicked.connect(self.pushButtonSolveSudoku)
        self.pushButton_limpiarSudoku.clicked.connect(self.clearSudoku)

    def pushButtonSolveSudoku(self):
        self.label_analizando.setVisible(True)
        list_Grid = sudoku.main()
        print(list_Grid)
        self.fillSudoku(list_Grid)

    def fillSudoku(self, list_Grid:list):
        for i in range(81):              
            getattr(self, "line_"+str(i)).setText(f'{list_Grid[i]}')
    

    def clearSudoku(self):
        self.label_analizando.setVisible(False)
        for i in range(81):              
            getattr(self, "line_"+str(i)).clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()

    try: 
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')