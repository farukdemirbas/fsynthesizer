import math
from fglobals import FREQ, ENVELOPE, SAMPLE_RATE
from faudiobuffer import AudioBuffer, Sinusoid


class Note():

	def __init__(self, note, duration_ms, envelope,
				volume=0.5, echo=False, echo_intensity=1):
		self.main_buffer = AudioBuffer()  # to hold the final buffer
		self.raw_buffer = None  # to hold unprocessed note signal
		self.note = note
		self.duration_ms = duration_ms  # in milliseconds
		self.frequency = FREQ[self.note]
		self.volume = volume
		self.envelope = envelope

		# "harmonics" is a list such as [0.5, 0, 0, 0.25, 0.25], where
		# harmonic[0] is the 1st harmonic, harmonic[1] is the 2nd harmonic...
		# and the value of each index is the harmonic's volume ratio.
		# You don't have to have them add up to 1, but it is advised.
		self.harmonics = [0.8, 0.15, 0.05]

		self.echo = echo
		self.echo_intensity = echo_intensity
		self.tail_length = 0  # residual sound caused by Release and other FX
		self.process()  # completely process and get the note ready for writing

	def process(self):
		self.generateRawNote()
		self.applyHarmonics()
		self.applyEnvelope()
		self.applyEcho()
		self.tail_length = self.calcTailLength()

	def generateRawNote(self):
		self.raw_buffer = Sinusoid(self.frequency,
									self.duration_ms, self.volume)

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
				# looks complicated but it's not. see comments on "harmonic"
				harm = Sinusoid(self.frequency * (i+1),
								self.duration_ms, harmonics[i])
				self.main_buffer = self.main_buffer.add(harm)


	def applyEnvelope(self, envelope=None):
		if envelope == None:
			envelope = self.envelope

	def applyEcho(self):
		pass

	def calcTailLength(self):
		# returns the number of samples that compose the tail.
		return 0

	def addToAudioBuffer(self, buffer):
		pass
