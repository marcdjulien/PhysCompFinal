from Constants import *
import threading
from pygame import midi
import time

class MidiDevice(threading.Thread):
	def __init__(self, name):
		super(MidiDevice, self).__init__()
		midi.init()
		self.outport = self.get_device(name)
		self.play = True
		self.playing_notes = []
		self.playing_mutex = threading.Lock()

	def run(self):
		print "Starting MIDI"
		while self.play:
			self.playing_mutex.acquire()
			for nvd in self.playing_notes:
				nvd[2] = nvd[2] - MIDI_DEVICE_PERIOD
				if nvd[2] <= 0:
					self.playing_notes.remove(nvd)
					self.release_note(nvd[0], nvd[1])
			self.playing_mutex.release()
			time.sleep(MIDI_DEVICE_PERIOD)

		self.playing_mutex.acquire()
		for nvd in self.playing_notes:
			self.release_note(nvd[0], nvd[1])
		self.outport.close()

	def add_note(self, nvd):
		self.playing_mutex.acquire()
		self.playing_notes.append(nvd)
		self.playing_mutex.release()

	def play_note(self, note, vel, duration):
		self.add_note([note, vel, duration])
		self.outport.write_short(NOTE_ON, note, vel)

	def release_note(self, note, vel):
		self.outport.write_short(NOTE_OFF, note, vel)
		pass
	def stop(self):
		self.play = False

	def get_device(self, dev_name):
		for i in xrange(0, midi.get_count()):
			name = midi.get_device_info(i)[1]
			if name == dev_name:
				if midi.get_device_info(i)[3]:
					return midi.Output(i)