from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot

from modeller import Modeller

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("window.ui", self)

        self.setFixedSize(900, 650)
        self.setWindowTitle("Система с очередями")

        self.btn_run.clicked.connect(self.run)

    def run(self):
        uniform_a = self.spin_a.value()
        uniform_b = self.spin_b.value()
        expo_lambd = self.spin_lambd.value()
        req_count = self.spin_req_count.value()
        reenter_prob = self.spin_reenter_prob.value()
        dt = self.spin_dt.value()
        method = self.comboBox_method.currentIndex()

        print(uniform_a, uniform_b, expo_lambd, req_count, reenter_prob, dt)
        modeller = Modeller(uniform_a, uniform_b, expo_lambd, reenter_prob, req_count, dt)
        if method == 0:
            self.show_results(modeller.event_based_modelling())
        else:
            self.show_results(modeller.time_based_modelling())

    def show_results(self, results):
        self.lineEdit_res_request_count.setText(str(results[0]))
        self.lineEdit_res_reentered_count.setText(str(results[1]))
        self.lineEdit_res_max_queue_size.setText(str(results[2]))
        self.lineEdit_res_time.setText('{:.2f}'.format(results[3]))