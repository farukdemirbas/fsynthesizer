import math
from fglobals import SAMPLE_RATE, SAMPLE_WIDTH


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


class Sinusoid(AudioBuffer):
	""" Takes frequency, length (milliseconds!), and amplitude (from 0 to 1),
	and "becomes" an AudioBuffer containing that sinusoid
	using the global SAMPLE_RATE information.
	"""

	def __init__(self, frequency, duration, amplitude=0.5, *args, **kwargs):
		super(Sinusoid, self).__init__(*args, **kwargs)

		self._becomeSinusoid(frequency, duration, amplitude)

	def _becomeSinusoid(self, frequency, duration, amplitude):
		sr = self.sample_rate

		for i in range(int(sr * duration / 1000)):
			val = amplitude * math.cos(2 * math.pi * frequency * i / sr)
			self.append(val)

