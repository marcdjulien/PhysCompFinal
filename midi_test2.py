from MidiDevice import MidiDevice
from Constants import *
import time

MIDI_DEVICE_NAME = "LoopBe Internal MIDI"
md = MidiDevice(MIDI_DEVICE_NAME)
md.start()
"""
for note in xrange(65, 100, 3):
	md.play_note(5, note, 100, 0.5)
	time.sleep(0.25)
"""
note = 69 + 4
md.play_note(0, note, 100, 0.5)
time.sleep(1.00)
md.stop()