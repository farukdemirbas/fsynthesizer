import os
from sys import argv, exit
from generate import generate_audio_file
import config


def main(composition_abs_path):
	config.COMPOSITION_ABS_PATH = os.path.abspath(composition_abs_path)
	generate_audio_file()
	print("\nSuccess.")

if __name__ == "__main__":
	if len(argv) < 2:
		print("\n\tExample: python -m run <absolute_path_to_my_composition.txt>"
			  "\n\tThe song will be created in the 'songs' folder\n")
		exit()	
	main(argv[1])
	
