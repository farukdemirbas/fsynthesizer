from note import Note
from config import DURATION_MULTIPLIER

class Track:
	""" A Track object is an ordered container for unprocessed Note objects.
	A Track does not care about actually processing its Notes.

	** But it is its job to initialize them (if needed),
	and set them up for future processing.

	** General usage:
		1) Add the Notes
		2) Give the Track an Envelope, and override other settings as you like.
		3) call applySettingsToNotes()
		
		X) If desired, Notewise customization can be done AFTER above steps.

	A Track can either take an already initialized Note and add it to itself,
	or it can take the arguments needed to initialize a Note, initialize it,
	and add it to itself.

	Notes on a particular Track share the same effects and a common Envelope.
	The Track object sets the Envelope and FX settings for its Notes.
	
	---
	DETAILS:
	
	The reason why we are not holding processed Notes is simply because they
	are massive, and we don't want to store them in memory.
	The Notes, however, *will* get processed one day, but Track does not care
	about that. The processing of the note is done by other classes right
	before being written to the final SongBuffer, (one by one), and then
	deleted. This way, we only ever store 1 Note in memory at a time.

	Way, way in the future, when I further optimize the Note objects' memory
	costs, this methodology will be revised. Because ideally we'd like all of
	our Notes to be kept in memory for dynamic and real-time modification and
	other such benefits.
	---
	"""
	
	def __init__(self):
		self.name = ""  # example: BASSLINE!!! (I'M ALREADY EXCITED)
		self.notes = []
		self.volume = 0.5
		self.envelope = None
		self.harmonics = [0.85, 0.10, 0.05]
		self.echo = False
		self.echo_delay = 100
		self.echo_volume = 0.35

	def addNoteObject(self, note):
		self.notes.append(note)

	def addNoteFromParams(self, *args):
		try:
			self.addNoteObject(Note(*args))
		except:
			raise Exception("\nInvalid input file."
				"\n(Check for typos in your notes file.)")

	def applySettingsToNotes(self):
		for note in self.notes:
			note.volume = self.volume
			note.envelope = self.envelope
			note.echo = self.echo
			note.echo_delay = self.echo_delay
			note.echo_volume = self.echo_volume


def convert_to_track(track):
	t = Track()
	for element in track:
		if isinstance(element, Note):
			t.addNoteObject(element)
		else:
			t.addNoteFromParams(*element)

	return t
