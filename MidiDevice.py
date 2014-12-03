from Constants import *
import threading
from pygame import midi
import time

class MidiDevice(threading.Thread):
	def __init__(self, name):
		super(MidiDevice, self).__init__()
		# Initialize the python midi module 
		midi.init()
		# Get the Midi device that we want to control
		self.outport = self.get_device(name)
		# True/False whether to play or now
		self.play = True
		# List of notes currently being played
		self.playing_notes = [] #Each element is of the form: [note, velocity, duration]
		self.playing_mutex = threading.Lock()

	def run(self):
		print "Starting MIDI"
		while self.play:
			self.playing_mutex.acquire()
			# Go through each note being played and decrement the time
			# Remove any notes that are done playing
			for cnvd in self.playing_notes:
				# Subtract from the amount of time left to play
				cnvd[3] = cnvd[3] - MIDI_DEVICE_PERIOD
				# If done playing remove from list, and send message to stop note
				if cnvd[3] <= 0:
					self.playing_notes.remove(cnvd)
					self.release_note(cnvd[0], cnvd[1], cnvd[2])

			self.playing_mutex.release()
			# Wait for a certain amount of time
			time.sleep(MIDI_DEVICE_PERIOD)

		# When done playing or quiting
		# Remove and stop playing all notes
		self.playing_mutex.acquire()
		for cnvd in self.playing_notes:
			self.release_note(cnvd[0], cnvd[1], cnvd[2])
		self.outport.close()

	"""
	Thread safe way to add notes to list
	"""
	def add_note(self, cnvd):
		self.playing_mutex.acquire()
		self.playing_notes.append(cnvd)
		self.playing_mutex.release()
	"""
	play_note:
	Sends a message to the midi device to play a certain note
	and adds the note to the list of currently playing notes

	params:
	note: the MIDI note value to play
	vel: the velocity/intensity of the note to play
	duration: how long to play each note
	"""
	def play_note(self, channel, note, vel, duration):
		self.add_note( [channel, note, vel, duration] )
		self.outport.write_short(channel+NOTE_OFF, note, vel)
		self.outport.write_short(channel+NOTE_ON, note, vel)

	"""
	release
	"""
	def release_note(self, channel, note, vel):
		self.outport.write_short(channel+NOTE_OFF, note, vel)

	def stop(self):
		self.play = False

	def get_device(self, dev_name):
		for i in xrange(0, midi.get_count()):
			name = midi.get_device_info(i)[1]
			print midi.get_device_info(i)
			if name == dev_name:
				if midi.get_device_info(i)[3]: #Checking if output device
					return midi.Output(i)