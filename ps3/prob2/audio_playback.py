#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Audio Playback
# Generated: Fri Mar  4 17:55:46 2016
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

from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx


class audio_playback(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Audio Playback")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48e3
        self.playback_rate = playback_rate = 1

        ##################################################
        # Blocks
        ##################################################
        _playback_rate_sizer = wx.BoxSizer(wx.VERTICAL)
        self._playback_rate_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_playback_rate_sizer,
        	value=self.playback_rate,
        	callback=self.set_playback_rate,
        	label='playback_rate',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._playback_rate_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_playback_rate_sizer,
        	value=self.playback_rate,
        	callback=self.set_playback_rate,
        	minimum=.25,
        	maximum=10,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_playback_rate_sizer)
        self.fractional_interpolator_xx_0 = filter.fractional_interpolator_ff(0, playback_rate)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink("radio_recording_2.wav", 1, int(samp_rate), 8)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_float*1, "radio_samples", False)
        (self.blocks_file_source_0).set_min_output_buffer(1000)
        (self.blocks_file_source_0).set_max_output_buffer(10000)
        self.audio_sink_0 = audio.sink(48000, "", False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.fractional_interpolator_xx_0, 0))    
        self.connect((self.fractional_interpolator_xx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.fractional_interpolator_xx_0, 0), (self.blocks_wavfile_sink_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_playback_rate(self):
        return self.playback_rate

    def set_playback_rate(self, playback_rate):
        self.playback_rate = playback_rate
        self._playback_rate_slider.set_value(self.playback_rate)
        self._playback_rate_text_box.set_value(self.playback_rate)
        self.fractional_interpolator_xx_0.set_interp_ratio(self.playback_rate)


def main(top_block_cls=audio_playback, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
