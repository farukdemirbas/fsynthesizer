---
fsynthesizer [v0.01]
---

HOW TO USE:
Write your compositions in a text file inside the "compositions" folder.
(Check the readme.txt in there for a quick guide on composition formatting).
Then, if you want custom effects on your tracks, see "songsettings.py".
To run the program, execute "python -m main mysong.txt mysong"
The program will look for "mysong.txt" in the compositions folder, and create a "mysong.wav" in the songs folder.
So your resulting .wav file will be be found in the "songs" folder.

Check out the "songs" folder for sample songs.
Check the "compositions" folder for sample compositions.

--------

fsynthesizer is a learning project that uses no external dependencies.
The next update will feature MIDI support.

**In the short term, fysnthesizer will be a Python console application that takes in a custom-format music file, applies rudimentary sound processing and generates a WAV file.**

------

Version 1.0 planned to be implemented **by the start of Summer 2019**, and will be like described below.

**fsynthesizer is (going to become) a program that functions quite like a typical synthesizer.**
It will be a GUI application that allows real-time recording (via a normal or MIDI keyboard) and sound processing. MIDI import will be supported. The user will create their own envelopes, signal shapes, harmonics, sound effects and so on. They will then also be able to save their custom effects. Most widely used music file extensions will be supported in generating an output file.
