#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test Pymavlink Source
# Description: SImple test of pymavlink source.  Requires SITL runing for the UDP
# GNU Radio version: 3.8.4.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import uaslink


class test_pymavlink_source(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Test Pymavlink Source")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.uaslink_pymavlink_source_p_1 = uaslink.pymavlink_source_p('udp:127.0.0.1:14550', 57600)
        self.blocks_message_debug_0 = blocks.message_debug()


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.uaslink_pymavlink_source_p_1, 'MAVLink'), (self.blocks_message_debug_0, 'print'))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate





def main(top_block_cls=test_pymavlink_source, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
