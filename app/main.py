from sys import argv
from generate import generate_audio_file


def main(notes_file):
	wave_file_path = generate_audio_file(notes_file)

	print(
		"Success. \nHere is the path to your song: \n{}".format(wave_file_path)
	)


if __name__ == "__main__":
	try:
		main(argv[1])  # argv[1] is the txt file for the notes_file.
	except IndexError:
		print("Please specify the file containing the notes."
			  "\nExample: python main.py \"mysong.txt\""
			  "\nThe song file should be in the \"compositions\" folder.\n")
