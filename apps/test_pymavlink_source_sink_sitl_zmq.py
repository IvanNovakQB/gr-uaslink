#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test Pymavlink Source Sink Sitl Zmq
# GNU Radio version: 3.8.4.0

from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import uaslink


class test_pymavlink_source_sink_sitl_zmq(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Test Pymavlink Source Sink Sitl Zmq")

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source('tcp://127.0.0.1:14000', 100, False, '')
        self.uaslink_pymavlink_source_sink_pp_1 = uaslink.pymavlink_source_sink_pp('tcp:127.0.0.1:5763',57600)
        self.uaslink_mavlink_control_0 = uaslink.mavlink_control('127.0.0.1:14560', 57600)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.uaslink_mavlink_control_0, 'MAVLink_OUT'), (self.uaslink_pymavlink_source_sink_pp_1, 'MAVLink_IN'))
        self.msg_connect((self.uaslink_pymavlink_source_sink_pp_1, 'MAVLink_OUT'), (self.uaslink_mavlink_control_0, 'MAVLink_IN'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.uaslink_mavlink_control_0, 'Command'))






def main(top_block_cls=test_pymavlink_source_sink_sitl_zmq, options=None):
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
