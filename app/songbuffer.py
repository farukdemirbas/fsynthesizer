import wave
import os
from array import array
from audiobuffer import AudioBuffer
from config import MAX_AMPLITUDE, SAMPLE_WIDTH

	# ---------------------!!!!!!!!!!!!!-------------------------- #
	# ----------------------- WARNING ---------------------------- #
	# ----------------- MENTAL SAFETY HAZARD --------------------- #
	# ----------------- HORRIBLE CODE BELOW ---------------------- #
	# VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV #
	# ---------------------!!!!!!!!!!!!!-------------------------- #
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
		i = 1
		for track in self.tracks:
			print("Processing track {}/{}...".format(i, len(self.tracks)))
			i += 1
			for note in track.notes:
				note.process()
				self.writeToSelf(note)
				note.clearBuffers()
			self.cursor = 0
		self.scaleVolume()
	
	def writeToSelf(self, note):
		self.buffer[self.cursor:] = self.buffer[self.cursor:].add(note.main_buffer)
		self.cursor += int(self.buffer.sample_rate * note.duration / 1000) #TODO: wtf?

	def scaleVolume(self):
		# the song is completely ready, and sitting on the buffer
		# except its amplitude ranges between [-1, 1].
		# so we scale it up according to our sample width
		# minus a bit of a safety margin.
		# (because audio FX may have raised the amplitude to a value above 1)
		self.buffer = self.buffer.multiply(.25 * MAX_AMPLITUDE)

	def writeToWav(self):
		from config import TARGET_FOLDER_NAME, COMPOSITION_ABS_PATH
		sr = self.buffer.sample_rate

		print("Packing python objects into primitive types.")
		# Convert our [-1, 1] float array into an integer array
		data = array('i', [0] * len(self.buffer))
		for i in range(len(self.buffer)):
			data[i] = int(self.buffer[i])

		print("Writing out to wav...")

		target_name = os.path.splitext(os.path.basename(COMPOSITION_ABS_PATH))[0] + ".wav"
		# ^ target_name == <name_of_song>.wav

		with wave.open(os.path.join(os.path.dirname(__file__), "..", TARGET_FOLDER_NAME, target_name), "wb") as f:
			f.setsampwidth(SAMPLE_WIDTH)
			f.setnchannels(1)
			f.setframerate(sr)

			f.writeframesraw(data)
			f.writeframes(b'')
