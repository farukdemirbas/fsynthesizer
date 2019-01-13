from sys import argv
from generate import generate_audio_file
import config



def main(notes_file, targetname):
	config.TARGETNAME = targetname
	config.NOTESNAME = notes_file
	generate_audio_file()
	print("\nSuccess")

if __name__ == "__main__":
	try:
		main(argv[1], argv[2])
	except IndexError:
		print("\nExample: python main.py mysong.txt songname"
			  "\nThe notes file should be in the \"compositions\" folder.\n"
			  "\nThe song will be written to songname.wav in the songs folder")
