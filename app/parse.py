def parse_notes():
	
	tracks = []

	from config import COMPOSITION_ABS_PATH
	with open(COMPOSITION_ABS_PATH, 'r') as f:
		lines = f.readlines()
		track = []
		for line in lines:
			if line == "\n":
				continue
			if line.startswith("//"):
				continue
			if line == '+\n':
				tracks.append([val for val in track])
				track.clear()
			else:
				# CONVERTNECESSARYSTRINGSINTOFLOATSSSSSS
				temp = line.split()
				for i in range(1, len(temp)):
					temp[i] = float(temp[i])
				track.append(temp)
		tracks.append([val for val in track])

	return tracks
