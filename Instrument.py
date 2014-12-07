
class Instrument(Object):
	def __init(self):
		super(Instrument, self).__init__()
		self.on = False
		self.style = 0
		self.pattern = 0
		self.variation = 0

	def set_on(self, on):
		self.on = on

	def set_style(self, style):
		self.style = style

	def set_pattern(self, pattern):
		self.pattern = pattern

	def set_variation(self, variation):
		set_variation = variation

	def get_on(self):
		return self.on

	def get_style(self):
		return self.style

	def get_pattern(self):
		return self.pattern

	def get_variation(self):
		return self.variation