import math
from globals import SAMPLE_RATE, SAMPLE_WIDTH


class AudioBuffer(list):

	sample_rate = SAMPLE_RATE

	def __init__(self, *args, **kwargs):
		super(AudioBuffer, self).__init__(*args, **kwargs)

	def add(self, other):
		# adding a scalar is not supported as it shouldn't ever be needed.
		if not isinstance(other, list):
			return

		if len(other) == 0:
			return self

		# we need to know which one is the longer one and vice versa.
		longer = None
		shorter = None

		if len(self) > len(other):
			longer = self
			shorter = other
		else:
			longer = other
			shorter = self

		# first, deepcopy the longer one onto the resulting buffer
		result = AudioBuffer([val for val in longer])

		# iterate over the shorter one, to add its elements to result
		for i in range(len(shorter)):
			result[i] += shorter[i]

		return result

	def multiply(self, other):
		""" the multiplication behavior you'd expect
		when applying an envelope
		"""

		result = AudioBuffer()

		# if "other" is an iterable object,
		if isinstance(other, list):
			if len(other) == 0:
				return self
			# find the overlap length
			# and multiply each index as normal
			overlap = min(len(self), len(other))
			for i in range(overlap):
				result.append(self[i] * other[i])

		# if "other" is a scalar number, just do scalar multiplication
		else:
			for el in self:
				result.append(el * other)

		return result


class SongBuffer(AudioBuffer):

	def __init__(self, *args, **kwargs):
		super(SongBuffer, self).__init__(*args, **kwargs)

		# list of Track objects
		self.tracks = []

	def addTrack(self, track):
		self.tracks.append(track)

	def makeSong(self, tracks):
		pass

	def writeToWav(self):
		# return path to wav file
		pass
