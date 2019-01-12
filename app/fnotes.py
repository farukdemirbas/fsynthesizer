from fglobals import FREQ
from faudiobuffer import AudioBuffer, Sinusoid


class Note():
	"""Creates an AudioBuffer that holds a note.
	When process()'d, its main_buffer becomes an AudioBuffer with all desired
	effects applied, and whose total length	is the original length of the node
	+ the tail length. The tail is the residual sound tacked onto the note as
	a result of various Sound FX like echo and the envelope's release.
	"""

	def __init__(self, note, duration, envelope=None,
				volume=0.5, echo=False, echo_delay=50, echo_intensity=0.5):
		self.main_buffer = AudioBuffer()  # to hold the final sound of note
		self.raw_buffer = None  # to hold unprocessed note signal
		self.note = note
		
		# all duration data is in milliseconds
		self.duration = duration
		# residual sound caused by Release and other FX
		# TOTAL DURATION of the note == duration + tail_duration
		self.tail_duration = 0

		self.frequency = FREQ[self.note]
		self.volume = volume
		self.envelope = envelope

		# "harmonics" is a list such as [0.5, 0, 0, 0.25, 0.25], where
		# harmonic[0] is the 1st harmonic, harmonic[1] is the 2nd harmonic...
		# and the value of each index is the harmonic's volume ratio. We don't
		# have to have them add up to 1, but a value close to 1 is advised.
		self.harmonics = [0.8, 0.15, 0.05]

		self.echo = echo
		self.echo_delay = echo_delay
		self.echo_intensity = echo_intensity

	def process(self):
		# completely process and get the note ready for writing
		self.calcTailLength()
		self.generateRawNote()
		self.applyHarmonics()
		if self.envelope:
			self.applyEnvelope()
		if self.echo:
			self.applyEcho()

	def calcTailLength(self):
		self.tail_duration = 0
		if self.envelope:
			self.tail_duration += self.envelope.release_time
		if self.echo:
			self.tail_duration += self.echo_delay

	def generateRawNote(self):
		self.raw_buffer = Sinusoid(self.frequency, self.duration
									+ self.tail_duration, self.volume)

	def applyHarmonics(self, harmonics=None):
		if harmonics == None:
			harmonics = self.harmonics
		
		# apply the volume to the 1st harmonic, which is our raw_buffer atm.
		self.raw_buffer = self.raw_buffer.multiply(self.harmonics[0])

		# place a copy of the raw buffer onto the master buffer
		self.master_buffer = [val for val in self.raw_buffer]

		# generate the signals for the other harmonics
		# and add them all onto the main buffer
		for i in range(len(harmonics)):
			if harmonics[i] != 0:
				# looks complicated but it's not. see comments on "harmonics"
				harm = Sinusoid(self.frequency * (i+1),
								self.duration, harmonics[i])
				self.main_buffer = self.main_buffer.add(harm)


	def applyEnvelope(self, envelope=None):
		if envelope == None:
			envelope = self.envelope
		envelope.apply(self)

	def applyEcho(self):
		sr = AudioBuffer.sample_rate

		# here, we just make a sequence of zeroes followed by the main buffer
		echo = (
			AudioBuffer([0]) * sr * self.echo_delay / 1000) + self.main_buffer
		
		self.main_buffer = self.main_buffer.add(echo)
