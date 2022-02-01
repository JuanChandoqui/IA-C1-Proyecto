import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtGui, QtCore
from threading import Thread
from time import sleep
import Models.AG as sudoku

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Views/menu.ui', self)   
        self.setWindowIcon(QtGui.QIcon('./Resources/Images/sudoku_logo.png'))
        self.setWindowTitle("SUDOKU")
        self.pushButton_ResolverSudoku.clicked.connect(self.pushButtonSolveSudoku)


    def pushButtonSolveSudoku(self):
        sudoku.inicializar()
        list_Grid = sudoku.get_sudoku()
        print(list_Grid)

        # list_Grid = []
        # list_Grid_with_0 = []

        # for i in range(9):
        #     list_aux = []
        #     for j in range(9):
        #         number = getattr(self, "line_" + str(i) + "_" + str(j)).text()
        #         if (number == "" or number == " " or number == "  "):
        #             list_aux.append(0)               
        #         else:
        #             number = int(number)
        #             list_aux.append(number)
            
        #     list_Grid_with_0.append(list_aux) #para mantener los valores en color negro
        #     list_Grid.append(list_aux)
        self.fillSudoku(list_Grid)
        # self.threadSolveSudoku(list_Grid=list_Grid)


    def fillSudoku(self, list_Grid:list):
        Palette= QtGui.QPalette()

        for i in range(81):
                # getattr(self, "line_"+str(i)).setText(f'{1}')
                getattr(self, "line_"+str(i)).setText(f'{list_Grid[i]}')
                getattr(self, "line_"+str(i)).setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
                Palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
                getattr(self, "line_"+str(i)).setPalette(Palette)
                # sleep(0.01)


    # def threadSolveSudoku(self, list_Grid):
    #     thread = Thread(target=self.fillSudoku, args=(list_Grid,))
    #     thread.start() 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()

    try: 
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')