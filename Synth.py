import threading
import random
import time
from Constants import *

class Synth(threading.Thread):
	def __init__(self, md):
		super(Synth, self).__init__()
		self.board = self.new_board()
		self.board_mutex = threading.Lock()
		self.playing = []
		self.cur_step = 0
		self.play = True
		self.play_mutex = threading.Lock()
		self.note_time = NOTE_PERIOD
		self.seq_time = SEQ_PERIOD
		self.md = md

	def run(self):
		print "Starting Synth"
		while self.play:

			board = self.get_board()
			row = board[self.cur_step]

			for i in xrange(len(row)):
				style = row[i]

				if style == SQUARE:
					self.md.play_note(69 + i, 100, self.note_time)
				elif style == CIRCLE:
					self.md.play_note(45 + i, 100, self.note_time)


			time.sleep(self.seq_time)
			self.cur_step = (self.cur_step + 1) % STEPS

	def quit(self):
		print "Closing Synth"
		self.pause()
		self.md.stop()

	def play(self):
		self.play_mutex.acquire()
		self.play = True
		self.play_mutex.release()

	def pause(self):
		self.play_mutex.acquire()
		self.play = False
		self.play_mutex.release()

	def clear_board(self):
		board = self.new_board()
		self.set_board(board)

	def get_board(self):
		self.board_mutex.acquire()
		b = self.board
		self.board_mutex.release()
		return b

	def set_board(self, board):
		self.board_mutex.acquire()
		self.board = board
		self.board_mutex.release()

	def new_board(self):
		board = []
		for i in xrange(STEPS):
			board.append([])
			for j in xrange(12):
				board[i].append(BLANK)
		return board

	def shape2board(self, shapes):
		board = self.new_board()
		Xi = 1.0/STEPS
		Yi = 1.0/NOTES
		for s in shapes:
			if s[0] == CIRCLE:
				x = STEPS-int(s[2]/Xi) - 1
				y = int(s[3]/Yi) - 1
				board[x][y] = CIRCLE
			elif s[0] == SQUARE:
				x = STEPS-int(s[2]/Xi) - 1
				y = int(s[3]/Yi) - 1
				board[x][y] = SQUARE
		self.set_board(board)


