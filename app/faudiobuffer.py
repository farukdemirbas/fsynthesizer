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

	def __init__(self, frequency, duration_ms, amplitude=0.5, *args, **kwargs):
		super(Sinusoid, self).__init__(*args, **kwargs)

		self.frequency = frequency
		self.duration_ms = duration_ms
		self.amplitude = amplitude

		self._becomeSinusoid(self.frequency, self.duration_ms, self.amplitude)

	def _becomeSinusoid(self):
		self.clear()
		# Acos(2pi.f.t) for each sample.
		for i in range(int(self.sample_rate * self.duration_ms / 1000)):
			val = self.amplitude * math.cos(
					2 * math.pi * self.frequency * i / self.sample_rate)
			self.append(val)


class Line(AudioBuffer):
	"""
	The line of reasoning here is to have each line line up to align as an
	envelope when requested further down the line.
	Knows the project's properties and composes itself in line.
	
	---
	Eight days out of nine, you want a cosine
	You'll think all is well, life is cake and wine
	Another class, oh never, will you need to define
	Back in your chair, content, you will recline
	
	Come that day, no escape, no warnings, no means to confine
	You will view your model to perhaps some parts refine
	The idea terrifies you, to lack a crucial thing in design
	Day will yield the night, you'll ponder in moonshine

	Then, a flash of brilliance, you will recombine
	The memories of yonder, of your past deeds divine!
	Your eyes will shine, bathed in all emotions benign

	In immense relief, you'll be sighin':

	This class is mine
	it operates fine
	Say otherwise
	and you'll be lyin'.
	---

	"""

	def __init__(self, starting_value, ending_value,
					duration_ms, *args, **kwargs):
		super(Line, self).__init__(*args, **kwargs)

		self.starting_value = starting_value
		self.ending_value = ending_value
		self.duration_ms = duration_ms

		self.constructLine()

	def constructLine(self):
		self.clear()
		for i in range(int(self.sample_rate * self.duration_ms / 1000)):
			val = self.starting_value + (
						(self.ending_value - self.starting_value)
						* i / (self.sample_rate * self.duration_ms / 1000))
			self.append(val)
