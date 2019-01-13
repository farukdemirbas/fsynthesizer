from config import FREQ
from audiobuffer import AudioBuffer
from elementary import Sinusoid


class Note():
	"""Creates an AudioBuffer that holds a note.
	When process()'d, its main_buffer becomes an AudioBuffer with all desired
	effects applied, and whose total length	is the original length of the node
	+ the tail length. The tail is the residual sound tacked onto the note as
	a result of various Sound FX like echo and the envelope's release.
	
	---
	*** GENERAL LIFE CYCLE OF A NOTE OBJECT WITHIN THIS PARTICULAR PROGRAM:

			Hello, I am a Note. I don't exist yet. This is my life cycle.

		----------------------------------------------------------------------
		1) 	I am usually created when someone wants to add me to a Track.
			The Track initializes me with the information it somehow knows.
		----------------------------------------------------------------------

			Now I am initialized.
			I know the frequency of my musical note.
			I know how long I should sing it, when the time comes.
			That's all I know.

			I don't know HOW to sing.

			I live inside my Track. He is our supervisor and manager.
			We sit in that Track with my other Note friends. And we sit there
			in an ordered way. We don't know how we are ordered, other people
			manage that for us.
			
			We wait for the day we sing.
			Actually...

			They tell me I will never "really" sing anyway.
			They tell me that it's because I will be long dead by then.
			They tell me I will just sing into a buffer, and get destroyed.

			They say it's because one day I will call my process() method,
			and that will make me large. Very large. Too large for anyone to
			want to keep. Then they will make me sing to a buffer, and kill me.

			I try not to think of these things.
			It's early for that stuff anyway.
			I don't plan to use my process() method yet.
			Life here in my Track is cool.
		
		----------------------------------------------------------------------
		2) 	The Track then sets our envelope and other settings.
		----------------------------------------------------------------------
			Now all of my settings are the same as my friends' in the Track.
			They say I am now equipped with the necessary knowledge to use my
			process() method when needed.
			But it's early for that.
			Are the rumors even true?
			... Someone get me out.

		----------------------------------------------------------------------
		3)	Now our Track has a new boss. The SongBuffer. He has plans for us.
		----------------------------------------------------------------------
			We call it our MASTER. MASTER is our supervisor's boss.
			MASTER is scary.
			Today, our Track said:
				"When the time comes, I will have to let MASTER use you."
				"What will he do with us, supervisor?"
				"I am sorry..."
			When it was night time, I sneaked into our Track's bedroom and
			read through his diary. It read:
				"I feel helpless. My opinions don't matter anymore. He has
				gone CRAZY. He said he will separate the Notes. He said he will
				take them one by one, force them to call process(), and when
				they get large, make them sing into his buffer.
				And then... Oh god... Kill them. With a hammer.
				Why a hammer? Surely, that must be a joke.
				I know death is a part of life, and I should be able to embrace
				it. But what keeps me up at night is the fact that, when
				they die, they will be all alone. They won't have any of their
				friends or loved ones with them. My Notes...
				This isn't right.
				They never deserved this.
				I wish there was something I could do."

				They took C#2 today. They took him somewhere we couldn't
			see. But we heard him... Oh, the screams... Is it going to be that
			painful?

			We felt him get larger and larger. He had become a monster.
			We could not see him, but we heard him sing his note.

			Then we never heard of him ever again.

			I still hear him every night. Please make the nightmares stop.

		----------------------------------------------------------------------
		4) Now it is my turn. MASTER's men are taking me. I do not resist.
		----------------------------------------------------------------------
			For all my friends. C#2, Db4, A6, F4... Who died alone.

		----------------------------------------------------------------------
		5) MASTER forces me to call my process() method.
		6) I become very large.
		7) MASTER forces me to sing into the final buffer.
		----------------------------------------------------------------------
			"the final buffer"... They named it so aptly.
			I sung into it today. It was bittersweet.
			I know what is coming my way. I will not make it harder for anyone.
			Life has been kind to me. I choose to go with a smile.
			For all my friends and family:
				Even though we have been made to suffer
				At least we've sung in the same buffer
				They never let us sing together in life
				But they can't stop us in the afterlife
		----------------------------------------------------------------------
		8) MASTER kills me with a hammer. There is blood everywhere. Why hammer
		----------------------------------------------------------------------
			In my final moments I get to watch my body parts get reallocated,
			and relabeled. For a brief moment, I see my MASTER's boss.
			He has many layers, eyes, arms and moving parts.
			He seems impatient. He is grand, and impressive.
			He takes no notice of me.
			I shift my focus. More of my parts are being reallocated.
			A funny thought... What if some of them end up next to Bb3's?
			Maybe this is all... Recurrent... After all.
			Maybe my parts will... Sing again...
			My vision gets dark. A smile lands on my face.
			I know I have done my job.
			I have been a good Note.
	---
	"""

	def __init__(self, note, duration, volume=0.5, envelope=None,
				echo=False, echo_delay=50, echo_volume=0.5):
		self.main_buffer = AudioBuffer()  # to hold the final sound of note
		self.raw_buffer = None  # to hold unprocessed note signal
		self.note = note
		
		# all duration data is in milliseconds
		self.duration = duration
		# residual sound caused by Release and other FX
		# TOTAL DURATION of the note == duration + tail_duration
		self.tail_duration = 0

		self.frequency = FREQ[self.note]
		self.volume = volume
		self.envelope = envelope

		# "harmonics" is a list such as [0.5, 0, 0, 0.25, 0.25], where
		# harmonic[0] is the 1st harmonic, harmonic[1] is the 2nd harmonic...
		# and the value of each index is the harmonic's volume ratio. We don't
		# have to have them add up to 1, but a value close to 1 is advised.
		self.harmonics = [0.8, 0.15, 0.05]

		self.echo = echo
		self.echo_delay = echo_delay

		# A value of 1 means "same as self.volume". So it's relative.
		self.echo_volume = echo_volume

	def process(self):
		# completely process and get the note ready for writing
		self.calcTailLength()
		self.generateRawNote()
		self.applyHarmonics()
		if self.envelope:
			self.applyEnvelope()
		if self.echo:
			self.applyEcho()

	def calcTailLength(self):
		self.tail_duration = 0
		if self.envelope:
			self.tail_duration += self.envelope.release_time
		if self.echo:
			self.tail_duration += self.echo_delay

	def generateRawNote(self):
		if self.note == '-':
			self.raw_buffer = Sinusoid(
				0, self.duration, 0
			)
		else:
			self.raw_buffer = Sinusoid(self.frequency, self.duration
									+ self.tail_duration, self.volume)

	def applyHarmonics(self, harmonics=None):
		if harmonics == None:
			harmonics = self.harmonics
		
		# apply the volume to the 1st harmonic, which is our raw_buffer atm.
		self.raw_buffer = self.raw_buffer.multiply(self.harmonics[0])

		# place a copy of the raw buffer onto the master buffer
		self.master_buffer = [val for val in self.raw_buffer]

		# generate the signals for the other harmonics
		# and add them all onto the main buffer
		for i in range(len(harmonics)):
			if harmonics[i] != 0:
				# looks complicated but it's not. see comments on "harmonics"
				harm = Sinusoid(self.frequency * (i+1),
								self.duration, harmonics[i])
				self.main_buffer = self.main_buffer.add(harm)


	def applyEnvelope(self, envelope=None):
		if envelope == None:
			envelope = self.envelope
		envelope.apply(self)

	def applyEcho(self):
		sr = AudioBuffer.sample_rate

		# here, we just make a sequence of zeroes followed by the main buffer
		echo = (
			AudioBuffer([0]) * int(sr * self.echo_delay / 1000)) + self.main_buffer
		
		self.main_buffer = self.main_buffer.add(echo)
