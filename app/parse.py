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
				# convert necessary strings into floats
				temp = line.split()
				for i in range(1, len(temp)):
					temp[i] = float(temp[i])
				track.append(temp)
		tracks.append(track)

	return tracks
