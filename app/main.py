from sys import argv
from fgenerate import generate_audio_file
from fplayback import playback_audio_file


def main(notes_file):
    wave_file_path = generate_audio_file(notes_file)
    playback_audio_file(wave_file_path)


if __name__ == "__main__":
    try:
        main(argv[1])  # argv[1] is the txt file for the notes_file.
    except IndexError:
        print("Please specify the file holding the notes."
              "\nExample: python main.py \"mysong.txt\"")
