from MidiDevice import MidiDevice
from Synth import Synth
from Viewer import Viewer
from VideoAnalyzer import VideoAnalyzer
from Constants import *
import time, pygame

md = MidiDevice(MIDI_DEVICE_NAME)
sy = Synth(md)
va = VideoAnalyzer(sy)
vw = Viewer(sy)

md.start()
sy.start()
vw.start()
va.start()
