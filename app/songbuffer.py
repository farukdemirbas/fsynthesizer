import wave
import struct
from audiobuffer import AudioBuffer
from config import MAX_AMPLITUDE, SAMPLE_WIDTH

class SongBuffer(AudioBuffer):

	def __init__(self, *args, **kwargs):
		super(SongBuffer, self).__init__(*args, **kwargs)

		# list of Track objects
		self.tracks = []

		# determines where the next writing operation will occur
		self.cursor = 0

	def addTrack(self, track):
		self.tracks.append(track)

	def makeSong(self):
		for track in self.tracks:
			for note in track.notes:
				note.process()
				self.writeToSelf(note)
				del note
			self.cursor = 0
		self.scaleVolume()
	
	def writeToSelf(self, note):
		self[self.cursor:].add(note.main_buffer)
		self.cursor += len(self.sample_rate * note.duration / 1000)

	def scaleVolume(self):
		# the song completely ready, and sitting on the buffer
		# except its amplitude is between [0, 1]
		# so we scale it up according to our sample width
		# minus a bit of a safety margin.
		self.multiply(0.85 * MAX_AMPLITUDE)

	def writeToWav(self):
		sr = self.sample_rate

		data = struct.pack("<h" * len(self), *self)

		with open("../songs/test.wav", "wb") as f:
			f.setsampwidth(SAMPLE_WIDTH)
			f.setnchannels(1)
			f.setframerate(sr)

			f.writeframesraw(data)

