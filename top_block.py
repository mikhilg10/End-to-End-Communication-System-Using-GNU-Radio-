#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.7.13.5
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from math import pi
from optparse import OptionParser
import pmt
import sys
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.nfilts = nfilts = 32
        self.ntaps = ntaps = 11*nfilts*sps
        self.excess_bw = excess_bw = 0.4
        self.tx_taps = tx_taps = firdes.root_raised_cosine(nfilts,nfilts,1.0,excess_bw,ntaps)
        self.timing_bw = timing_bw = 2*pi/100
        self.samp_rate = samp_rate = 96e3
        self.rx_taps = rx_taps = firdes.root_raised_cosine(nfilts,nfilts*sps,1.0,excess_bw,ntaps)
        self.interpolator = interpolator = 5
        self.fll_ntaps = fll_ntaps = 55
        self.fc = fc = 120e3
        self.f_cut_0 = f_cut_0 = 20e3
        self.f_cut = f_cut = 24e3
        self.decimator = decimator = 5
        self.const_points = const_points = 2

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decimator,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=interpolator,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
        	  sps,
                  taps=(tx_taps),
        	  flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)

        self.low_pass_filter_0_0_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	2, samp_rate*interpolator, f_cut, 4e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	2, samp_rate*interpolator, f_cut, 4e3, firdes.WIN_HAMMING, 6.76))
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, 2*pi/100, (rx_taps), nfilts, 16, 1.5, 1)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(sps, excess_bw, fll_ntaps, 2*pi/100)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(2*pi/100, 4, False)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((-1, 1), 1)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate*interpolator,True)
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_float*1, 2)
        self.blocks_pack_k_bits_bb_0_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_multiply_xx_1_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_uchar_0 = blocks.float_to_uchar()
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, 'D:\\Work\\GNURadio\\LAB-4\\Original_Text.txt', False)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, 'D:\\Work\\GNURadio\\LAB-4\\Sent.txt', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_sig_source_x_1_0_0_0 = analog.sig_source_f(samp_rate*interpolator, analog.GR_SIN_WAVE, fc, 1, 0)
        self.analog_sig_source_x_1_0_0 = analog.sig_source_f(samp_rate*interpolator, analog.GR_COS_WAVE, fc, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate*interpolator, analog.GR_COS_WAVE, fc, 1, 0)
        self.Tabs = Qt.QTabWidget()
        self.Tabs_widget_0 = Qt.QWidget()
        self.Tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Tabs_widget_0)
        self.Tabs_grid_layout_0 = Qt.QGridLayout()
        self.Tabs_layout_0.addLayout(self.Tabs_grid_layout_0)
        self.Tabs.addTab(self.Tabs_widget_0, 'Message before up-conversion')
        self.Tabs_widget_1 = Qt.QWidget()
        self.Tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Tabs_widget_1)
        self.Tabs_grid_layout_1 = Qt.QGridLayout()
        self.Tabs_layout_1.addLayout(self.Tabs_grid_layout_1)
        self.Tabs.addTab(self.Tabs_widget_1, 'Up-converted Signal')
        self.top_grid_layout.addWidget(self.Tabs)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_1_0_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.analog_sig_source_x_1_0_0_0, 0), (self.blocks_multiply_xx_1_0, 1))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_xx_1_0, 0))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.blocks_skiphead_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_float_to_uchar_0, 0), (self.blocks_pack_k_bits_bb_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.low_pass_filter_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_1_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_skiphead_0, 0), (self.blocks_float_to_uchar_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.digital_fll_band_edge_cc_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rx_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts*self.sps,1.0,self.excess_bw,self.ntaps))
        self.pfb_arb_resampler_xxx_0.set_rate(self.sps)
        self.set_ntaps(11*self.nfilts*self.sps)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_tx_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts,1.0,self.excess_bw,self.ntaps))
        self.set_rx_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts*self.sps,1.0,self.excess_bw,self.ntaps))
        self.set_ntaps(11*self.nfilts*self.sps)

    def get_ntaps(self):
        return self.ntaps

    def set_ntaps(self, ntaps):
        self.ntaps = ntaps
        self.set_tx_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts,1.0,self.excess_bw,self.ntaps))
        self.set_rx_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts*self.sps,1.0,self.excess_bw,self.ntaps))

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.set_tx_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts,1.0,self.excess_bw,self.ntaps))
        self.set_rx_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts*self.sps,1.0,self.excess_bw,self.ntaps))

    def get_tx_taps(self):
        return self.tx_taps

    def set_tx_taps(self, tx_taps):
        self.tx_taps = tx_taps
        self.pfb_arb_resampler_xxx_0.set_taps((self.tx_taps))

    def get_timing_bw(self):
        return self.timing_bw

    def set_timing_bw(self, timing_bw):
        self.timing_bw = timing_bw

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(2, self.samp_rate*self.interpolator, self.f_cut, 4e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(2, self.samp_rate*self.interpolator, self.f_cut, 4e3, firdes.WIN_HAMMING, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate*self.interpolator)
        self.analog_sig_source_x_1_0_0_0.set_sampling_freq(self.samp_rate*self.interpolator)
        self.analog_sig_source_x_1_0_0.set_sampling_freq(self.samp_rate*self.interpolator)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate*self.interpolator)

    def get_rx_taps(self):
        return self.rx_taps

    def set_rx_taps(self, rx_taps):
        self.rx_taps = rx_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps((self.rx_taps))

    def get_interpolator(self):
        return self.interpolator

    def set_interpolator(self, interpolator):
        self.interpolator = interpolator
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(2, self.samp_rate*self.interpolator, self.f_cut, 4e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(2, self.samp_rate*self.interpolator, self.f_cut, 4e3, firdes.WIN_HAMMING, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate*self.interpolator)
        self.analog_sig_source_x_1_0_0_0.set_sampling_freq(self.samp_rate*self.interpolator)
        self.analog_sig_source_x_1_0_0.set_sampling_freq(self.samp_rate*self.interpolator)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate*self.interpolator)

    def get_fll_ntaps(self):
        return self.fll_ntaps

    def set_fll_ntaps(self, fll_ntaps):
        self.fll_ntaps = fll_ntaps

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.analog_sig_source_x_1_0_0_0.set_frequency(self.fc)
        self.analog_sig_source_x_1_0_0.set_frequency(self.fc)
        self.analog_sig_source_x_0.set_frequency(self.fc)

    def get_f_cut_0(self):
        return self.f_cut_0

    def set_f_cut_0(self, f_cut_0):
        self.f_cut_0 = f_cut_0

    def get_f_cut(self):
        return self.f_cut

    def set_f_cut(self, f_cut):
        self.f_cut = f_cut
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(2, self.samp_rate*self.interpolator, self.f_cut, 4e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(2, self.samp_rate*self.interpolator, self.f_cut, 4e3, firdes.WIN_HAMMING, 6.76))

    def get_decimator(self):
        return self.decimator

    def set_decimator(self, decimator):
        self.decimator = decimator

    def get_const_points(self):
        return self.const_points

    def set_const_points(self, const_points):
        self.const_points = const_points


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
