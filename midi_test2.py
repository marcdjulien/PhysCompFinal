from MidiDevice import MidiDevice
from Constants import *
import time

MIDI_DEVICE_NAME = "LoopBe Internal MIDI"
md = MidiDevice(MIDI_DEVICE_NAME)
md.start()

for note in xrange(65, 100, 3):
	md.play_note(note, 100, 0.5)
	time.sleep(0.25)

time.sleep(3)
md.stop()