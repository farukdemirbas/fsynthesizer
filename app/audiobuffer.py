from config import SAMPLE_RATE


class AudioBuffer(list):

	sample_rate = SAMPLE_RATE

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def __getitem__(self, key):
		if isinstance(key, slice):
			return AudioBuffer(super().__getitem__(key))
		return super().__getitem__(key)

	def __mul__(self, val):
		return AudioBuffer(super().__mul__(val))

	def __add__(self, el):
		return AudioBuffer(super().__add__(el))

	def add(self, other):
		""" return a new AudioBuffer that is the result of
		adding Other onto Self element-wise.
		the original AudioBuffers remain untouched.
		"""

		# adding a scalar is not supported as it shouldn't be needed yet.
		if not isinstance(other, list):
			raise Exception("Can not add() a scalar value to an AudioBuffer.")

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
				return result
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

	@property
	def duration(self):
		sr = self.sample_rate
		dur = len(self) * 1000 / sr
		return dur

	def deepcopy(self):
		return AudioBuffer([val for val in self])
