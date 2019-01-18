from envelope import example_envelopes

def song_settings(tracks):
	""" Take note of how many tracks you have in your composition.
	En example case is portrayed below.

	# I have 3 tracks, I name them for convenience.
-->	pad = tracks[0]
-->	bass = tracks[1]
-->	lead = tracks[2]
	
	# I use a pre-defined envelope for my pad track.
-->	pad.envelope = example_envelopes["pulse"]
	
	# I use another pre-defined envelope for my bass track.
-->	bass.envelope = example_envelopes["longrelease"]
	# I want my bass to be slighlty louder. (0.5 is the default volume)
-->	bass.volume = 0.65

	# I make a custom envelope for my lead.
	# See "envelope.py" for details.
-->	lead.envelope = Envelope(1, 10, 0.8, 40, 200)
-->	lead.volume = 0.65
	# I set custom harmonics for my lead.
	# 1st harmonic has 0.65 relative volume.
	# 2nd harmonic has 0.25 relative volume.
	# 3rd harmonic has 0.10 relative volume. ...
	# (They don't have to add up to 1)
-->	lead.harmonics = [0.65, 0.25, 0.10, 0.005]
	"""

	################# YOUR CODE HERE ###################

	for i in range(len(tracks)):
		tracks[i].envelope = example_envelopes["drawnout"]
		tracks[i].harmonics = [0.85, 0.15]

	tracks[-1].envelope = example_envelopes["longrelease"]
	tracks[-1].volume = 0.15

	tracks[-2].envelope = example_envelopes["pulse"]

	####################################################

	for i in range(len(tracks)):
		tracks[i].applySettingsToNotes()
