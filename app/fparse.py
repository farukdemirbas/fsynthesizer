def parse_notes(song_file):
	tracks = []

	with open(song_file, 'r') as f:
		lines = f.readlines()
		track = []
		for line in lines[:-1]:
			if line == '+\n':
				tracks.append(track)
				track.clear()
			else:
				track.append(line.split())
		tracks.append(track)

	return tracks
