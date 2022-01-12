#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Packet Loopback Hier
# Description: Complete Loopback of packet based mavlink messages
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

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from gnuradio.qtgui import Range, RangeWidget
from packet_rx import packet_rx  # grc-generated hier_block
from packet_tx import packet_tx  # grc-generated hier_block
import uaslink

from gnuradio import qtgui

class packet_loopback_hier(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Packet Loopback Hier")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Packet Loopback Hier")
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

        self.settings = Qt.QSettings("GNU Radio", "packet_loopback_hier")

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
        self.Const_PLD = Const_PLD = digital.constellation_calcdist(digital.psk_4()[0], digital.psk_4()[1],
        4, 1).base()
        self.Const_PLD.gen_soft_dec_lut(8)
        self.sps = sps = 2
        self.rep = rep = 3
        self.rate = rate = 2
        self.polys = polys = [109, 79]
        self.nfilts = nfilts = 32
        self.k = k = 7
        self.hdr_format = hdr_format = digital.header_format_counter(digital.packet_utils.default_access_code, 3, Const_PLD.bits_per_symbol())
        self.eb = eb = 0.22
        self.tx_rrc_taps = tx_rrc_taps = firdes.root_raised_cosine(nfilts, nfilts,1.0, eb, 5*sps*nfilts)
        self.time_offset = time_offset = 1.0
        self.rx_rrc_taps = rx_rrc_taps = firdes.root_raised_cosine(nfilts, nfilts*sps,1.0, eb, 11*sps*nfilts)
        self.noise = noise = 0.0
        self.freq_offset = freq_offset = 0
        self.enc_hdr = enc_hdr = fec.repetition_encoder_make(8000, rep)
        self.enc = enc = fec.cc_encoder_make(8000,k, rate, polys, 0, fec.CC_TERMINATED, False)
        self.dec_hdr = dec_hdr = fec.repetition_decoder.make(hdr_format.header_nbits(),rep, 0.5)
        self.dec = dec = fec.cc_decoder.make(8000,k, rate, polys, 0, -1, fec.CC_TERMINATED, False)
        self.amp = amp = 1.0
        self.Const_HDR = Const_HDR = digital.constellation_calcdist(digital.psk_2()[0], digital.psk_2()[1],
        2, 1).base()
        self.Const_HDR.gen_soft_dec_lut(8)

        ##################################################
        # Blocks
        ##################################################
        self._time_offset_range = Range(0.99, 1.01, 0.00001, 1.0, 200)
        self._time_offset_win = RangeWidget(self._time_offset_range, self.set_time_offset, 'Time Offset', "counter_slider", float)
        self.top_grid_layout.addWidget(self._time_offset_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noise_range = Range(0, 5, 0.01, 0.0, 200)
        self._noise_win = RangeWidget(self._noise_range, self.set_noise, 'Noise Amp', "counter_slider", float)
        self.top_grid_layout.addWidget(self._noise_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_offset_range = Range(-0.5, 0.5, 0.0001, 0, 200)
        self._freq_offset_win = RangeWidget(self._freq_offset_range, self.set_freq_offset, 'Freq. Offset', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_offset_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._amp_range = Range(0, 2, 0.01, 1.0, 200)
        self._amp_win = RangeWidget(self._amp_range, self.set_amp, 'Amplitude', "counter_slider", float)
        self.top_layout.addWidget(self._amp_win)
        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source('tcp://127.0.0.1:14000', 100, False, '')
        self.uaslink_pymavlink_source_sink_pp_0 = uaslink.pymavlink_source_sink_pp('/dev/ttyUSB0',57600)
        self.uaslink_mavlink_control_0 = uaslink.mavlink_control('127.0.0.1:14560', 57600)
        self.tab1 = Qt.QTabWidget()
        self.tab1_widget_0 = Qt.QWidget()
        self.tab1_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab1_widget_0)
        self.tab1_grid_layout_0 = Qt.QGridLayout()
        self.tab1_layout_0.addLayout(self.tab1_grid_layout_0)
        self.tab1.addTab(self.tab1_widget_0, 'Time')
        self.tab1_widget_1 = Qt.QWidget()
        self.tab1_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab1_widget_1)
        self.tab1_grid_layout_1 = Qt.QGridLayout()
        self.tab1_layout_1.addLayout(self.tab1_grid_layout_1)
        self.tab1.addTab(self.tab1_widget_1, 'Freq.')
        self.tab1_widget_2 = Qt.QWidget()
        self.tab1_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab1_widget_2)
        self.tab1_grid_layout_2 = Qt.QGridLayout()
        self.tab1_layout_2.addLayout(self.tab1_grid_layout_2)
        self.tab1.addTab(self.tab1_widget_2, 'Const.')
        self.top_grid_layout.addWidget(self.tab1, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.tab0 = Qt.QTabWidget()
        self.tab0_widget_0 = Qt.QWidget()
        self.tab0_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab0_widget_0)
        self.tab0_grid_layout_0 = Qt.QGridLayout()
        self.tab0_layout_0.addLayout(self.tab0_grid_layout_0)
        self.tab0.addTab(self.tab0_widget_0, 'Time')
        self.tab0_widget_1 = Qt.QWidget()
        self.tab0_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab0_widget_1)
        self.tab0_grid_layout_1 = Qt.QGridLayout()
        self.tab0_layout_1.addLayout(self.tab0_grid_layout_1)
        self.tab0.addTab(self.tab0_widget_1, 'Freq.')
        self.tab0_widget_2 = Qt.QWidget()
        self.tab0_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab0_widget_2)
        self.tab0_grid_layout_2 = Qt.QGridLayout()
        self.tab0_layout_2.addLayout(self.tab0_grid_layout_2)
        self.tab0.addTab(self.tab0_widget_2, 'Const.')
        self.top_grid_layout.addWidget(self.tab0, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.packet_tx_0_0 = packet_tx(
            hdr_const=Const_HDR,
            hdr_enc=enc_hdr,
            hdr_format=hdr_format,
            pld_const=Const_PLD,
            pld_enc=enc,
            psf_taps=tx_rrc_taps,
            sps=sps,
        )
        self.packet_tx_0 = packet_tx(
            hdr_const=Const_HDR,
            hdr_enc=enc_hdr,
            hdr_format=hdr_format,
            pld_const=Const_PLD,
            pld_enc=enc,
            psf_taps=tx_rrc_taps,
            sps=sps,
        )
        self.packet_rx_0_0 = packet_rx(
            eb=eb,
            hdr_const=Const_HDR,
            hdr_dec=dec_hdr,
            hdr_format=hdr_format,
            pld_const=Const_PLD,
            pld_dec=dec,
            psf_taps=rx_rrc_taps,
            sps=sps,
        )
        self.packet_rx_0 = packet_rx(
            eb=eb,
            hdr_const=Const_HDR,
            hdr_dec=dec_hdr,
            hdr_format=hdr_format,
            pld_const=Const_PLD,
            pld_dec=dec,
            psf_taps=rx_rrc_taps,
            sps=sps,
        )
        self.channels_channel_model_0_0 = channels.channel_model(
            noise_voltage=noise,
            frequency_offset=freq_offset,
            epsilon=time_offset,
            taps=[1.0],
            noise_seed=0,
            block_tags=True)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise,
            frequency_offset=freq_offset,
            epsilon=time_offset,
            taps=[1.0],
            noise_seed=0,
            block_tags=True)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(amp)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(amp)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.packet_rx_0, 'pkt out'), (self.uaslink_mavlink_control_0, 'MAVLink_IN'))
        self.msg_connect((self.packet_rx_0_0, 'pkt out'), (self.uaslink_pymavlink_source_sink_pp_0, 'MAVLink_IN'))
        self.msg_connect((self.uaslink_mavlink_control_0, 'MAVLink_OUT'), (self.packet_tx_0_0, 'in'))
        self.msg_connect((self.uaslink_pymavlink_source_sink_pp_0, 'MAVLink_OUT'), (self.packet_tx_0, 'in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.uaslink_mavlink_control_0, 'Command'))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.packet_rx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.packet_rx_0_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.channels_channel_model_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.packet_tx_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.packet_tx_0_0, 0), (self.channels_channel_model_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "packet_loopback_hier")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_Const_PLD(self):
        return self.Const_PLD

    def set_Const_PLD(self, Const_PLD):
        self.Const_PLD = Const_PLD
        self.packet_rx_0.set_pld_const(self.Const_PLD)
        self.packet_rx_0_0.set_pld_const(self.Const_PLD)
        self.packet_tx_0.set_pld_const(self.Const_PLD)
        self.packet_tx_0_0.set_pld_const(self.Const_PLD)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rx_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.sps, 1.0, self.eb, 11*self.sps*self.nfilts))
        self.set_tx_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0, self.eb, 5*self.sps*self.nfilts))
        self.packet_rx_0.set_sps(self.sps)
        self.packet_rx_0_0.set_sps(self.sps)
        self.packet_tx_0.set_sps(self.sps)
        self.packet_tx_0_0.set_sps(self.sps)

    def get_rep(self):
        return self.rep

    def set_rep(self, rep):
        self.rep = rep

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate

    def get_polys(self):
        return self.polys

    def set_polys(self, polys):
        self.polys = polys

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rx_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.sps, 1.0, self.eb, 11*self.sps*self.nfilts))
        self.set_tx_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0, self.eb, 5*self.sps*self.nfilts))

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format
        self.packet_rx_0.set_hdr_format(self.hdr_format)
        self.packet_rx_0_0.set_hdr_format(self.hdr_format)
        self.packet_tx_0.set_hdr_format(self.hdr_format)
        self.packet_tx_0_0.set_hdr_format(self.hdr_format)

    def get_eb(self):
        return self.eb

    def set_eb(self, eb):
        self.eb = eb
        self.set_rx_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.sps, 1.0, self.eb, 11*self.sps*self.nfilts))
        self.set_tx_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0, self.eb, 5*self.sps*self.nfilts))
        self.packet_rx_0.set_eb(self.eb)
        self.packet_rx_0_0.set_eb(self.eb)

    def get_tx_rrc_taps(self):
        return self.tx_rrc_taps

    def set_tx_rrc_taps(self, tx_rrc_taps):
        self.tx_rrc_taps = tx_rrc_taps
        self.packet_tx_0.set_psf_taps(self.tx_rrc_taps)
        self.packet_tx_0_0.set_psf_taps(self.tx_rrc_taps)

    def get_time_offset(self):
        return self.time_offset

    def set_time_offset(self, time_offset):
        self.time_offset = time_offset
        self.channels_channel_model_0.set_timing_offset(self.time_offset)
        self.channels_channel_model_0_0.set_timing_offset(self.time_offset)

    def get_rx_rrc_taps(self):
        return self.rx_rrc_taps

    def set_rx_rrc_taps(self, rx_rrc_taps):
        self.rx_rrc_taps = rx_rrc_taps
        self.packet_rx_0.set_psf_taps(self.rx_rrc_taps)
        self.packet_rx_0_0.set_psf_taps(self.rx_rrc_taps)

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self.channels_channel_model_0.set_noise_voltage(self.noise)
        self.channels_channel_model_0_0.set_noise_voltage(self.noise)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.channels_channel_model_0.set_frequency_offset(self.freq_offset)
        self.channels_channel_model_0_0.set_frequency_offset(self.freq_offset)

    def get_enc_hdr(self):
        return self.enc_hdr

    def set_enc_hdr(self, enc_hdr):
        self.enc_hdr = enc_hdr
        self.packet_tx_0.set_hdr_enc(self.enc_hdr)
        self.packet_tx_0_0.set_hdr_enc(self.enc_hdr)

    def get_enc(self):
        return self.enc

    def set_enc(self, enc):
        self.enc = enc
        self.packet_tx_0.set_pld_enc(self.enc)
        self.packet_tx_0_0.set_pld_enc(self.enc)

    def get_dec_hdr(self):
        return self.dec_hdr

    def set_dec_hdr(self, dec_hdr):
        self.dec_hdr = dec_hdr
        self.packet_rx_0.set_hdr_dec(self.dec_hdr)
        self.packet_rx_0_0.set_hdr_dec(self.dec_hdr)

    def get_dec(self):
        return self.dec

    def set_dec(self, dec):
        self.dec = dec
        self.packet_rx_0.set_pld_dec(self.dec)
        self.packet_rx_0_0.set_pld_dec(self.dec)

    def get_amp(self):
        return self.amp

    def set_amp(self, amp):
        self.amp = amp
        self.blocks_multiply_const_vxx_0.set_k(self.amp)
        self.blocks_multiply_const_vxx_0_0.set_k(self.amp)

    def get_Const_HDR(self):
        return self.Const_HDR

    def set_Const_HDR(self, Const_HDR):
        self.Const_HDR = Const_HDR
        self.packet_rx_0.set_hdr_const(self.Const_HDR)
        self.packet_rx_0_0.set_hdr_const(self.Const_HDR)
        self.packet_tx_0.set_hdr_const(self.Const_HDR)
        self.packet_tx_0_0.set_hdr_const(self.Const_HDR)





def main(top_block_cls=packet_loopback_hier, options=None):

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
