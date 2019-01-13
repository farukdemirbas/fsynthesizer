import wave
import struct
from audiobuffer import AudioBuffer
from config import MAX_AMPLITUDE, SAMPLE_WIDTH

class SongBuffer():
	""" Responsible to put the tracks together and create the final
	song buffer, and then write out to a wav file.
	As it is, this class is highly inefficient, and will be revisited.
	"""

	def __init__(self, *args, **kwargs):
		# list of Track objects
		self.tracks = []

		self.buffer = AudioBuffer()

		# cursor determines where the next writing operation will occur
		self.cursor = 0

	def addTrack(self, track):
		self.tracks.append(track)

	def makeSong(self):
		for track in self.tracks:
			for note in track.notes:
				note.process()
				
				# print(len(note.envelope.release), 3000 * self.buffer.sample_rate / 1000, note.tail_duration)
				# print(len(note.main_buffer), (note.duration + note.tail_duration) * self.buffer.sample_rate / 1000)

				self.writeToSelf(note)
				note.main_buffer.clear()
				note.raw_buffer.clear()
			self.cursor = 0
		self.scaleVolume()
	
	# ---------------------!!!!!!!!!!!!!-------------------------- #
	# ----------------------- WARNING ---------------------------- #
	# ----------------- MENTAL SAFETY HAZARD --------------------- #
	# ----------------- HORRIBLE CODE BELOW ---------------------- #
	# VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV #
	# ---------------------!!!!!!!!!!!!!-------------------------- #
	def writeToSelf(self, note):
		"""DO NOT LOOK INSIDE. DISASTER.
		(Temporary solution to a design conflict.)

		Readability? 10/10.
		Efficiency? World class.

		This method is as efficient as recycling a book by licking its papers
		until it disintegrates into nature.
		And it is as readable as that book after it's been disintegrated.
		"""

		# newportion will replace the part of self.buffer that's after cursor
		self.buffer[self.cursor:] = self.buffer[self.cursor:].add(note.main_buffer)
		self.cursor += int(self.buffer.sample_rate * note.duration / 1000)

	def scaleVolume(self):
		# the song is completely ready, and sitting on the buffer
		# except its amplitude ranges between [0, 1].
		# so we scale it up according to our sample width
		# minus a bit of a safety margin.
		# (because audio FX may have raised the amplitude to a value above 1)
		self.buffer = self.buffer.multiply(0.25 * MAX_AMPLITUDE)
		


		for track in self.tracks:
			for note in track.notes:
				pass



	def writeToWav(self):
		from config import TARGETFOLDER, TARGETNAME
		sr = self.buffer.sample_rate

		data = bytes()
		for val in self.buffer:
			temp = int(val)
			data += struct.pack('<h', temp)

		with wave.open("{}{}.wav".format(TARGETFOLDER, TARGETNAME), "wb") as f:
			f.setsampwidth(SAMPLE_WIDTH)
			f.setnchannels(1)
			f.setframerate(sr)

			f.writeframesraw(data)
			f.writeframes(b'')

		return 

