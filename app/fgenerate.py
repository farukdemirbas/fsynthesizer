"""Functions to generate an actual playable audio file from a
text file storing musical information in our designated format
"""

from faudiobuffer import AudioBuffer
from fparse import parse_notes

buffer = AudioBuffer()  # in memory


def generate_audio_file(song_file):
	# a 'track' is a monophonic sequence of notes
	tracks = parse_notes(song_file)
	for track in tracks:
		record_onto_buffer(track, buffer)
	audio_file_path = write_to_wav_file(buffer)
	return audio_file_path


def record_onto_buffer(notes, buffer):
	pass


def write_to_wav_file(buffer, destination_path=""):
	pass
