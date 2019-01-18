"""Functions to generate an actual playable audio file from a
text file storing musical information in our designated musical notation format
"""

from songbuffer import SongBuffer
from parse import parse_notes
from track import convert_to_track
from envelope import example_envelopes
from config import DURATION_MULTIPLIER
from songsettings import song_settings

master = SongBuffer()  # in memory

def generate_audio_file():
	# a 'track' is a monophonic sequence of notes
	# tracks is a list of individual tracks.
	print("\nParsing composition...")
	tracks = parse_notes()

	# Turn it into a list of Track objects, which allow customization
	# such as applying different envelopes or effects for each track
	# (i.e. maybe we want our bass track to have high attack and be pulse-like)
	for i in range(len(tracks)):
		tracks[i] = convert_to_track(tracks[i])

	apply_default_settings(tracks)  # start with the default settings
	print("\nApplying user settings onto tracks...")
	apply_user_settings(tracks)   # override the default settings as desired

	apply_duration_multiplier(tracks)

	print("\nAttaching tracks to master buffer...")
	# Add our Track objects to the master SongBuffer
	add_tracks_to_master(tracks, master)

	print("\nActualizing master buffer...")
	# Combine the tracks to create the final song.
	master.makeSong()

	# Write out the final song as a .wav file
	master.writeToWav()

	return True

def apply_default_settings(tracks):
	for i in range(len(tracks)):
		tracks[i].envelope = example_envelopes["standard"]
		tracks[i].echo = False
		tracks[i].echo_delay = 200
		tracks[i].echo_volume = 0.6
		tracks[i].applySettingsToNotes()

def apply_user_settings(tracks):
	try:
		song_settings(tracks)
	except Exception:
		print("\nSong settings invalid. Will be ignored.")
		print("Proceeding with default settings.")

def add_tracks_to_master(tracks, master):
	for i in range(len(tracks)):
		master.addTrack(tracks[i])

def apply_duration_multiplier(tracks):
	for track in tracks:
		for note in track.notes:
			note.duration *= DURATION_MULTIPLIER
