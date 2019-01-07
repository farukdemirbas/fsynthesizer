from fglobals import FREQ, ENVELOPE


class Note():

	def __init__(self, note, duration, envelope, amplitude, echo=False):
		self.buffer = []
		self.note = note
		self.duration = duration
		self.frequency = FREQ[note]
		self.amplitude = amplitude
		self.envelope = envelope
		self.harmonics = [65, 30, 5]  # 1st, 2nd and 3rd harmonics
		self.tail_length = 0  # residual sound caused by Release and Echo
		self.process()  # completely process and get the note ready for writing

	def process(self):
		self.generateRawNote()
		self.applyHarmonics()
		self.applyEnvelope()
		self.applyEcho()

	def generateRawNote(self):
		pass

	def applyHarmonics(self, harmonics=self.harmonics):
		pass

	def applyEnvelope(self, envelope=self.envelope):
		pass

	def applyEcho(self, intensity=1):
		pass

	def addToAudioBuffer(self, buffer):
		pass
