from elementary import Line
from audiobuffer import AudioBuffer


class Envelope():
	""" 
	1) It knows how to apply itself to a Note object of any length.

	2) The Envelope shuold be attached to the Note, BEFORE calling
	the Note's process() method. Which complies with common sense.
	
	---
	DETAILS:

	An Envelope holds several Lines that constitute its envelope structure.
	Each Line has 3 parameters: (starting value, ending value, duration).
	Duration is how much time in milliseconds it takes for it to finish its
	journey from the starting value to the ending value.

	A Line knows the sample rate (because it is an AudioBuffer), and adjusts
	itself. Since a Line is also an AudioBuffer, it can multiply and add itself
	with other AudioBuffers. Which is something we need when applying it.

	The release of an Envelope triggers at the END of the note, like when the
	player releases their finger from the piano key. And this introduces some
	complications into the design.

	I tried to confine most of the complications within the borders of
	this class where we don't have to worry about it ever again. And that is
	kind of why it is messy.
	---
	"""

	def __init__(self, attack_end, attack_time, decay_end,
								decay_time, release_time=40):
		self.attack_end = attack_end
		self.attack_time = attack_time
		self.decay_end = decay_end
		self.decay_time = decay_time
		self.release_time = release_time

		# a Line that starts at 0, ends at attack_end,
		# and takes attack_time amount of time in milliseconds.
		self.attack = Line(0, attack_end, attack_time)

		self.decay = Line(attack_end, decay_end, decay_time)

		self.sustain = None  # this depends on the note's duration.

		# Release's starting value depends on when the Note is released.
		# But most times its starting value will be the decay's ending value.
		# The edge case where a Note ends before our attack+decay is
		# known to our apply() method, and necessary actions are taken there.
		self.release = Line(self.decay_end, 0, self.release_time)

	def apply(self, note):
		sr = Line.sample_rate
		target = note.main_buffer
		tail_duration = note.tail_duration
		tail_start_index = int(sr * note.duration / 1000)
		body = target[:tail_start_index]
		tail = target[tail_start_index:]
		
		# print("note.duration:", note.duration)
		# print("note.duration's len calculated:", note.duration * sr / 1000)
		# print("len(note.main_buffer):", len(note.main_buffer))
		# print("note.dur + note.taildur:", note.duration + note.tail_duration)
		# print("length of ^^:", sr / 1000 * (note.duration + note.tail_duration))
		# print()

		# these two will be the result of the operation
		body_applied = None
		tail_applied = None

		# useful for the calculations that follow
		AD = self.attack + self.decay

		if len(body) <= len(AD):
			# Note is over, before the [attack + decay] sequence is done,
			# so we get the final value of [attack + decay] (last moment's val)
			# and assign it as the starting value of our Release
			self.release = Line(AD[len(body)-1], 0, self.release_time)

			# Make a new AudioBuffer that is the multiplication of
			# [attack + decay] and our note's body.
			# This is basically the body of the Note done.
			body_applied = body.multiply(AD)

		else:
			# If the note still continues after AD is finished,
			# we get how much time exists between AD's end and the note's end
			# and we create a Sustain buffer that is THAT long.
			self.sustain = Line(self.decay.ending_value,
								self.decay.ending_value,
								note.duration - AD.duration)

			# Put the Sustain buffer together with our AD
			# and apply it to our target's body
			ADS = AD + self.sustain
			body_applied = ADS.multiply(body)


		tail_applied = self.release.multiply(tail)

		return body_applied + tail_applied

example_envelopes = {
	"standard": (1, 10, 0.75, 20, 25),
	"mediumrelease": (1, 10, 1, 10, 350),
	"longrelease": (1, 10, 1, 10, 1100),
	"pulse": (1, 10, .45, 25, 25),
	"heavenly": (1, 800, 1, 1, 1200),
	"drawnout": (1, 3000, 0.3, 1000, 2600)
}