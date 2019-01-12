"""Functions to generate an actual playable audio file from a
text file storing musical information in our designated musical notation format
"""

from songbuffer import SongBuffer
from parse import parse_notes
from track import convert_to_track
from envelope import example_envelopes

master = SongBuffer()  # in memory

def generate_audio_file(song_file):
	# a 'track' is a monophonic sequence of notes
	# tracks is a list of individual tracks.
	tracks = parse_notes(song_file)

	# Turn it into a list of Track objects, which allow customization
	# such as applying different envelopes or effects for each track
	# (i.e. maybe we want our bass track to have high attack and be pulse-like)
	# And add our Track objects to the master SongBuffer
	for track in tracks:
		t = convert_to_track(track)
		t.envelope = example_envelopes["0"]
		t.echo = True
		t.applySettingsToNotes()
		master.addTrack(t)

	# Combine the tracks to create the final song.
	master.makeSong()

	# Write out the final song as a .wav file and store the file's path
	audio_file_path = master.writeToWav()

	return audio_file_path
