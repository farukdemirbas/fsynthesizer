from sys import argv
from fgenerate import generate_wave_file
from fplayback import playback_wave_file


def main(song):
    wave_file = generate_wave_file(song)
    playback_wave_file(wave_file)


if __name__ == "__main__":
    try:
        main(argv[1])  # argv[1] is the txt file for the song.
    except IndexError:
        print("Please specify the song file."
              "\nExample: python main.py \"mysong.txt\"")
