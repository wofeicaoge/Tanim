import os
from tanim.utils.file_ops import seek_full_path_from_defaults
import tanim.utils.constants as consts


def play_chord(*nums):
    commands = [
        "play",
        "-n",
        "-c1",
        "--no-show-progress",
        "synth",
    ] + [
        "sin %-" + str(num)
        for num in nums
    ] + [
        "fade h 0.5 1 0.5",
        ">",
        os.devnull
    ]
    try:
        os.system(" ".join(commands))
    except BaseException:
        pass


def play_error_sound():
    play_chord(11, 8, 6, 1)


def play_finish_sound():
    play_chord(12, 9, 5, 2)


def get_full_sound_file_path(sound_file_name):
    return seek_full_path_from_defaults(
        sound_file_name,
        default_dir=os.path.join(consts.ASSETS_DIR, "sounds"),
        extensions=[".wav", ".mp3"]
    )
