"""Functions to generate an actual playable audio file from a
text file storing musical information in our designated format
"""

from audiobuffer import SongBuffer
from parse import parse_notes

master = SongBuffer()  # in memory

def generate_audio_file(song_file):
	# a 'track' is a monophonic sequence of notes
	# tracks is a list of individual tracks.
	tracks = parse_notes(song_file)

	# Turn it into a list of Track objects, which allow customization
	# such as applying different envelopes or effects for each track
	# (i.e. maybe we want our bass track to have high attack and be pulse-like)
	tracks = make_tracks(tracks)

	# Add our Track objects to the master SongBuffer
	for track in tracks:
		master.addTrack(track)

	# Combine the tracks to create the final song.
	master.makeSong()

	# Write out the final song as a .wav file and store the file's path
	audio_file_path = master.writeToWav()

	return audio_file_path
