from config import SAMPLE_RATE
from array import array


class AudioBuffer(array):

	sample_rate = SAMPLE_RATE

	def __new__(cls, *args, **kwargs):
		return super().__new__(cls, 'f')

	def __init__(self, *args):
		if not args:
			return
		self.append(args[0])

	def __getitem__(self, key):
		if isinstance(key, slice):
			return AudioBuffer(super().__getitem__(key))
		return super().__getitem__(key)

	def __mul__(self, val):
		return AudioBuffer(super().__mul__(val))

	def append(self, *args, **kwargs):
		try:
			super().append(*args, **kwargs)
		except:
			self.extend(*args, **kwargs)

	def __add__(self, el):
		""" This is concatenation, not to be confused with 'add'. """
		return AudioBuffer(super().__add__(el))

	def add(self, other):
		""" Return a new AudioBuffer that is the result of
		adding Other onto Self element-wise.
		the original AudioBuffers remain untouched.
		"""

		# adding a scalar is not supported as it shouldn't be needed yet.
		if not isinstance(other, array):
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
		""" Element-wise multiplication.
		"""

		result = AudioBuffer()

		# if "other" is an iterable object,
		if isinstance(other, array): #TODO: iterable, not just array
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
		return len(self) * 1000 / self.sample_rate

	def deepcopy(self):
		return AudioBuffer([val for val in self])
	
	def clear(self):
		del self[:]


if __name__ == "__main__":
	li = []
	test_passed = True
	for i in range(10):
		if not len(AudioBuffer(li))==len(li):
			test_passed = False			
		li.append(i)
	print("Tests passed: {}".format(test_passed))