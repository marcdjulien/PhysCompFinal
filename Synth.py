import threading
import random
import time
from Constants import *

class Synth(threading.Thread):
	def __init__(self, md):
		super(Synth, self).__init__()
		# Synth board of notes
		self.board = self.new_board()
		self.board_mutex = threading.Lock()
		# Current step being played		
		self.cur_step = 0
		# True/False if the synth should be playing
		self.play = True
		self.play_mutex = threading.Lock()
		# Amount of time to play each note
		self.note_time = NOTE_PERIOD
		# Speed of the synthesizer
		self.seq_time = SEQ_PERIOD
		# Midi Device Object used to play notes
		self.md = md

	# Called when the thread is started
	def run(self):
		print "Starting Synth"
		while self.play:
			# Get the board matrix
			board = self.get_board()
			# Grab the current row
			row = board[self.cur_step]

			# Go through each section in the row and check which note should be played
			for i in xrange(len(row)):
				# The intensity of the note to play
				velocity = 100

				# Get the current value at that spot
				style = row[i]
				
				# Decide which type of note to play
				channel = i
				if style == SQUARE:
					note = 69 + i
					self.md.play_note(channel, note, velocity, self.note_time)
				elif style == CIRCLE:
					note = 45 + i
					self.md.play_note(channel, note, velocity, self.note_time)

			# Wait for a certain amount of time before playing the next row
			time.sleep(self.seq_time)
			# Increment step counter
			self.cur_step = (self.cur_step + 1) % STEPS

	def quit(self):
		print "Closing Synth"
		self.pause()
		self.md.stop()

	"""
	play/pause:
	Thread safe ways to change the play variable
	"""
	def play(self):
		self.play_mutex.acquire()
		self.play = True
		self.play_mutex.release()

	def pause(self):
		self.play_mutex.acquire()
		self.play = False
		self.play_mutex.release()

	"""
	clear_board/set_board/get_board:
	Thread safe ways to clear, get, and set the board
	"""
	def clear_board(self):
		self.board_mutex.acquire()
		board = self.new_board()
		self.set_board(board)
		self.board_mutex.release()

	def get_board(self):
		self.board_mutex.acquire()
		b = self.board
		self.board_mutex.release()
		return b

	def set_board(self, board):
		self.board_mutex.acquire()
		self.board = board
		self.board_mutex.release()

	"""
	Creates a new clear board and returns it
	"""
	def new_board(self):
		board = []
		for i in xrange(STEPS):
			board.append([])
			for j in xrange(12):
				board[i].append(BLANK)
		return board

	"""
	shape2board:
	Sets the board appropriately based on the shapes

	params:
	shapes: the list of shapes that were found
	"""
	def shape2board(self, shapes):
		board = self.new_board()
		Xi = 1.0/STEPS
		Yi = 1.0/NOTES
		for s in shapes:
			if s[0] == CIRCLE:
				x = int(s[2]/Xi) - 1
				y = int(s[3]/Yi) - 1
				if(0 <= x and x < STEPS and 0 <= y and y <= NOTES):
					board[x][y] = CIRCLE

			elif s[0] in [SQUARE, TRIANGLE, STAR]:
				m = np.mean(s[2], 0)
				x = int(m[0]/Xi) - 1
				y = int(m[1]/Yi) - 1
				if(0 <= x and x < STEPS and 0 <= y and y <= NOTES):
					board[x][y] = s[0]

		self.set_board(board)


