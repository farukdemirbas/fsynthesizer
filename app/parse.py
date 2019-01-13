
def parse_notes():
	tracks = []

	from config import NOTESFOLDER, NOTESNAME
	with open(NOTESFOLDER + NOTESNAME, 'r') as f:
		lines = f.readlines()
		track = []
		for line in lines[:-1]:
			if line == '+\n':
				tracks.append([val for val in track])
				track.clear()
			else:
				# convert necessary strings into floats
				temp = line.split()
				for i in range(1, len(temp)):
					temp[i] = float(temp[i])
				track.append(temp)
		tracks.append([val for val in track])

	return tracks
