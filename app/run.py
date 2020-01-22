import os
from sys import argv, exit
from generate import generate_audio_file
import config



def main(notes_file):
	config.NOTESPATH = os.path.abspath(notes_file)
	generate_audio_file()
	print("\nSuccess.")

if __name__ == "__main__":
	if len(argv) < 1:
		print("\n\tExample: python -m run [absolute_path_to_mysong.txt]"
			  "\n\tThe song will be created in the 'songs' folder\n")
		exit()	
	main(argv[1])
	
