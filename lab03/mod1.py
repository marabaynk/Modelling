import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QTabWidget, QHBoxLayout, QFormLayout, QDoubleSpinBox, QWidget, QSpinBox, QMessageBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from math import exp, factorial, gamma
import random
import scipy
from scipy.integrate import quad

def uniform_density(a, b, x):
    if (x >= a) and (x <= b):
        return 1 / (b - a)
    else:
        return 0

def uniform_function(a, b, x):
    if x < a:
        return 0
    elif x >= b:
        return 1
    else:
        return (x - a)/(b - a)

def Exponential_density(lmbd, k):
    return lmbd * exp(-lmbd * k)

def Exponential_function(lmbd, k):
    return quad(Exponential_density, 0, k, args=(lmbd))

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setGeometry(75,75,1800,900)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.figure2 = plt.figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.toolbar2 = NavigationToolbar(self.canvas2, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        hlayout = QHBoxLayout()

        vlayout1 = QVBoxLayout()
        vlayout1.addWidget(self.toolbar)
        vlayout1.addWidget(self.canvas)

        vlayout2 = QVBoxLayout()
        vlayout2.addWidget(self.toolbar2)
        vlayout2.addWidget(self.canvas2)


        hlayout.addLayout(vlayout1)
        hlayout.addLayout(vlayout2)


        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab1.setObjectName("1")
        self.tab2.setObjectName("2")

        self.tabs = QTabWidget()


        mainlayout = QVBoxLayout()
        mainlayout.addLayout(hlayout)
        self.tab1UI()
        self.tab2UI()
        self.tabs.addTab(self.tab1,"Равномерное распределение")
        self.tabs.addTab(self.tab2,"Экспоненциальное распределение")


        mainlayout.addWidget(self.tabs)
        mainlayout.addWidget(self.button)
        self.setLayout(mainlayout)
        self.is_show = False

    def tab1UI(self):
          layout = QFormLayout()
          self.a = QDoubleSpinBox()
          self.b = QDoubleSpinBox()
          self.start_x = QDoubleSpinBox()
          self.stop_x = QDoubleSpinBox()

          self.a.setRange(-1e6, 1e6)
          self.b.setRange(-1e6, 1e6)
          self.start_x.setRange(-1e6, 1e6)
          self.stop_x.setRange(-1e6, 1e6)

          self.a.setValue(3)
          self.b.setValue(6)
          self.start_x.setValue(1)
          self.stop_x.setValue(10)


          layout.addRow("a",self.a)
          layout.addRow("b",self.b)

          layout.addRow("x start",self.start_x)
          layout.addRow("x end",self.stop_x)
          self.tab1.setLayout(layout)

    def tab2UI(self):
          layout = QFormLayout()
          self.lmbd = QDoubleSpinBox()
          self.k_start = QSpinBox()
          self.k_stop = QSpinBox()
          self.lmbd.setRange(0, 1e6)

          self.k_start.setRange(0, 1e6)
          self.k_stop.setRange(0, 1e6)

          self.lmbd.setValue(10)
          self.k_start.setValue(1)
          self.k_stop.setValue(20)

          layout.addRow("alpha",self.lmbd)
          layout.addRow("x start",self.k_start)
          layout.addRow("x end",self.k_stop)
          self.tab2.setLayout(layout)


    def show_warning(self):
        msg = QMessageBox(parent = self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Некорректные данные")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()


    def getdata_uniform(self, foo):
        start = self.start_x.value()
        end = self.stop_x.value()
        N = self.N = 100

        a = self.a.value()
        b = self.b.value()

        if (a >= b) or (start >= end):
            self.show_warning()
            return None, None

        h = (end - start) / N
        X = [start + h * i for i in range(N)]
        Y = [foo(a, b, x) for x in X]
        return X, Y


    def getdata_Exponential(self, foo):
        k_start = self.k_start.value()
        k_stop = self.k_stop.value()
        lmbd = self.lmbd.value()

        if (k_start >= k_stop) or (k_start < 0):
            self.show_warning()
            return None, None

        X = [i for i in range(k_start, k_stop + 1)]
        Y = [foo(lmbd, k) for k in X]

        return X, Y


    def get_status(self, type):
        tabname = self.tabs.currentWidget().objectName()
        type.append(tabname)
        X_d, Y_d = None, None
        X_f, Y_f = None, None

        if tabname == "1":
            X_d, Y_d = self.getdata_uniform(uniform_density)
            if X_d is None:
                return (None, None, None, None)
            X_f, Y_f = self.getdata_uniform(uniform_function)
        else:
            X_d, Y_d = self.getdata_Exponential(Exponential_density)
            if X_d is None:
                return (None, None, None, None)
            X_f, Y_f = self.getdata_Exponential(Exponential_function)
        return (X_f, Y_f, X_d, Y_d)


    def plot(self):
        type = []
        X_f, Y_f, X_d, Y_d = self.get_status(type)

        if X_f is None:
            return

        self.figure.clear()
        self.figure2.clear()

        ax = self.figure.add_subplot(111)
        ax2 = self.figure2.add_subplot(111)


        ax.grid(True)
        ax2.grid(True)

        if type[0] == '1':
            ax.plot(X_d,Y_d)
            ax2.plot(X_f,Y_f)
        else:
            ax.plot(X_d,Y_d)
            ax2.plot(X_f,Y_f)

        ax.legend(['Пл-ть распр.'])
        ax2.legend(['Ф-ция распр.'])

        self.canvas.draw()
        self.canvas2.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()
    app.exec()
    #sys.exit()
