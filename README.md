# fsynthesizer [v0.1]

fsynthesizer is a **console application** that takes in a custom-format musical  
composition, applies rudimentary sound processing and generates a WAV file.  

---
#### HOW TO USE

Write your compositions in a text file inside the `compositions` folder.  
(Check the `README.txt` in there for a quick guide on composition formatting)  

Then, if you want custom effects on your tracks,
see the nice and brief explanation in "songsettings.py". 

To run the program, execute:

`python -m run [absolute_path_to_my_song.txt]`

Your resulting .wav file will be found in the "songs" folder.  

---
Check the `compositions` folder for sample compositions  
(Which have their corresponding outputs in the `songs` folder)  

---

Near future:
- Add MIDI/OSC support

Distant future:
- Introduce real-time functionality
- Introduce a GUI
- Work toward making into a DAW
