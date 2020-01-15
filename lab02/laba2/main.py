import numpy
from PyQt5.QtWidgets import *
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("MainWindow.ui", self)
        self.applyCount_btn.clicked.connect(self.setStatesCount)
        self.processStates_btn.clicked.connect(self.getMatrix)

    def setStatesCount(self):
        count = int(self.countSpin.text())
        self.matrixTable.setRowCount(count)
        self.matrixTable.setColumnCount(count)
        for i in range(count):
            for j in range(count):
                item = QTableWidgetItem("0")
                self.matrixTable.setItem(i, j, item)

    def solveMatrix(self, matrix, count):
        sv_left = []
        for i in range(count):
            p = []
            sum = 0
            for j in range(count):
                p.append(matrix[j][i])
                sum += matrix[i][j]
            p[i] = -sum
            sv_left.append(p)
        norm = [1.0 for i in range(count)]
        sv_left[count - 1] = norm
        sv_right = [0 for i in range(count)]
        sv_right[count - 1] = 1
        numpy_matrix = numpy.array(sv_left)
        numpy_vector = numpy.array(sv_right)
        # print(sv_left)
        # print(sv_right)

        # решение слау
        array = numpy.linalg.solve(numpy_matrix, numpy_vector)
        self.matrixTable_2.setRowCount(2)
        self.matrixTable_2.setColumnCount(count)
        for i in range(count):
            item = QTableWidgetItem(str(round(array[i] * 100, 3)) + "%")
            self.matrixTable_2.setItem(0, i, item)
        for i in range(count):
            sum = 0
            for j in range(count):
                sum += matrix[j][i]
            item = QTableWidgetItem(str(round(array[i] / sum, 3)) + "ед.")
            self.matrixTable_2.setItem(1, i, item)

    def getMatrix(self):
        matrix = []
        count = int(self.countSpin.text())
        for i in range(count):
            p = []
            for j in range(count):
                val = self.matrixTable.item(i, j).text()
                if val == "-":
                    p.append(0)
                else:
                    p.append(float(val))
            matrix.append(p)

        self.solveMatrix(matrix, count)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())