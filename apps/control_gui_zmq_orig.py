#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Control Gui Zmq Orig
# GNU Radio version: 3.8.4.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx

from gnuradio import qtgui

class control_gui_zmq_orig(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Control Gui Zmq Orig")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Control Gui Zmq Orig")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "control_gui_zmq_orig")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.up = up = 0
        self.takeoff = takeoff = 0
        self.samp_rate = samp_rate = 32000
        self.right = right = 0
        self.overridevalue = overridevalue = 1500
        self.mode = mode = 'STABILIZE'
        self.left = left = 0
        self.land = land = 0
        self.forward = forward = 0
        self.down = down = 0
        self.back = back = 0

        ##################################################
        # Blocks
        ##################################################
        _up_push_button = Qt.QPushButton('Up')
        _up_push_button = Qt.QPushButton('Up')
        self._up_choices = {'Pressed': 1, 'Released': 0}
        _up_push_button.pressed.connect(lambda: self.set_up(self._up_choices['Pressed']))
        _up_push_button.released.connect(lambda: self.set_up(self._up_choices['Released']))
        self.top_grid_layout.addWidget(_up_push_button, 1, 3, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        _takeoff_push_button = Qt.QPushButton('Take Off')
        _takeoff_push_button = Qt.QPushButton('Take Off')
        self._takeoff_choices = {'Pressed': 1, 'Released': 0}
        _takeoff_push_button.pressed.connect(lambda: self.set_takeoff(self._takeoff_choices['Pressed']))
        _takeoff_push_button.released.connect(lambda: self.set_takeoff(self._takeoff_choices['Released']))
        self.top_grid_layout.addWidget(_takeoff_push_button, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        _right_push_button = Qt.QPushButton('Right')
        _right_push_button = Qt.QPushButton('Right')
        self._right_choices = {'Pressed': 1, 'Released': 0}
        _right_push_button.pressed.connect(lambda: self.set_right(self._right_choices['Pressed']))
        _right_push_button.released.connect(lambda: self.set_right(self._right_choices['Released']))
        self.top_grid_layout.addWidget(_right_push_button, 2, 6, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._overridevalue_tool_bar = Qt.QToolBar(self)
        self._overridevalue_tool_bar.addWidget(Qt.QLabel('Override Value' + ": "))
        self._overridevalue_line_edit = Qt.QLineEdit(str(self.overridevalue))
        self._overridevalue_tool_bar.addWidget(self._overridevalue_line_edit)
        self._overridevalue_line_edit.returnPressed.connect(
            lambda: self.set_overridevalue(int(str(self._overridevalue_line_edit.text()))))
        self.top_grid_layout.addWidget(self._overridevalue_tool_bar, 2, 2, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._mode_options = ['STABILIZE', 'ALT_HOLD']
        # Create the labels list
        self._mode_labels = ['STABILIZE', 'ALT_HOLD']
        # Create the combo box
        self._mode_tool_bar = Qt.QToolBar(self)
        self._mode_tool_bar.addWidget(Qt.QLabel('Mode' + ": "))
        self._mode_combo_box = Qt.QComboBox()
        self._mode_tool_bar.addWidget(self._mode_combo_box)
        for _label in self._mode_labels: self._mode_combo_box.addItem(_label)
        self._mode_callback = lambda i: Qt.QMetaObject.invokeMethod(self._mode_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._mode_options.index(i)))
        self._mode_callback(self.mode)
        self._mode_combo_box.currentIndexChanged.connect(
            lambda i: self.set_mode(self._mode_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._mode_tool_bar, 3, 2, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        _left_push_button = Qt.QPushButton('Left')
        _left_push_button = Qt.QPushButton('Left')
        self._left_choices = {'Pressed': 1, 'Released': 0}
        _left_push_button.pressed.connect(lambda: self.set_left(self._left_choices['Pressed']))
        _left_push_button.released.connect(lambda: self.set_left(self._left_choices['Released']))
        self.top_grid_layout.addWidget(_left_push_button, 2, 4, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        _land_push_button = Qt.QPushButton('Land')
        _land_push_button = Qt.QPushButton('Land')
        self._land_choices = {'Pressed': 1, 'Released': 0}
        _land_push_button.pressed.connect(lambda: self.set_land(self._land_choices['Pressed']))
        _land_push_button.released.connect(lambda: self.set_land(self._land_choices['Released']))
        self.top_grid_layout.addWidget(_land_push_button, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        _forward_push_button = Qt.QPushButton('Forward')
        _forward_push_button = Qt.QPushButton('Forward')
        self._forward_choices = {'Pressed': 1, 'Released': 0}
        _forward_push_button.pressed.connect(lambda: self.set_forward(self._forward_choices['Pressed']))
        _forward_push_button.released.connect(lambda: self.set_forward(self._forward_choices['Released']))
        self.top_grid_layout.addWidget(_forward_push_button, 1, 5, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        _down_push_button = Qt.QPushButton('Down')
        _down_push_button = Qt.QPushButton('Down')
        self._down_choices = {'Pressed': 1, 'Released': 0}
        _down_push_button.pressed.connect(lambda: self.set_down(self._down_choices['Pressed']))
        _down_push_button.released.connect(lambda: self.set_down(self._down_choices['Released']))
        self.top_grid_layout.addWidget(_down_push_button, 2, 3, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        _back_push_button = Qt.QPushButton('Back')
        _back_push_button = Qt.QPushButton('Back')
        self._back_choices = {'Pressed': 1, 'Released': 0}
        _back_push_button.pressed.connect(lambda: self.set_back(self._back_choices['Pressed']))
        _back_push_button.released.connect(lambda: self.set_back(self._back_choices['Released']))
        self.top_grid_layout.addWidget(_back_push_button, 3, 5, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 6):
            self.top_grid_layout.setColumnStretch(c, 1)



    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "control_gui_zmq_orig")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_up(self):
        return self.up

    def set_up(self, up):
        self.up = up

    def get_takeoff(self):
        return self.takeoff

    def set_takeoff(self, takeoff):
        self.takeoff = takeoff

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_right(self):
        return self.right

    def set_right(self, right):
        self.right = right

    def get_overridevalue(self):
        return self.overridevalue

    def set_overridevalue(self, overridevalue):
        self.overridevalue = overridevalue
        Qt.QMetaObject.invokeMethod(self._overridevalue_line_edit, "setText", Qt.Q_ARG("QString", str(self.overridevalue)))

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode
        self._mode_callback(self.mode)

    def get_left(self):
        return self.left

    def set_left(self, left):
        self.left = left

    def get_land(self):
        return self.land

    def set_land(self, land):
        self.land = land

    def get_forward(self):
        return self.forward

    def set_forward(self, forward):
        self.forward = forward

    def get_down(self):
        return self.down

    def set_down(self, down):
        self.down = down

    def get_back(self):
        return self.back

    def set_back(self, back):
        self.back = back





def main(top_block_cls=control_gui_zmq_orig, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
