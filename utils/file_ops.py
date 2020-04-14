import os
import numpy as np

import utils.constants as consts


def initialize_directories(config):
    video_path_specified = config["video_dir"] or config["video_output_dir"]

    if not (video_path_specified and config["tex_dir"]):
        if config["media_dir"]:
            consts.MEDIA_DIR = config["media_dir"]
        else:
            consts.MEDIA_DIR = os.path.join(
                os.path.expanduser('~'),
                "media"
            )
        if not os.path.isdir(consts.MEDIA_DIR):
            consts.MEDIA_DIR = "./media"
        print(
            f"Media will be written to {consts.MEDIA_DIR + os.sep}. You can change "
            "this behavior with the --media_dir flag."
        )
    else:
        if config["media_dir"]:
            print(
                "Ignoring --media_dir, since both --tex_dir and a video "
                "directory were both passed"
            )

    consts.TEX_DIR = config["tex_dir"] or os.path.join(consts.MEDIA_DIR, "Tex")
    consts.TEXT_DIR = os.path.join(consts.MEDIA_DIR, "texts")
    if not video_path_specified:
        consts.VIDEO_DIR = os.path.join(consts.MEDIA_DIR, "videos")
        consts.VIDEO_OUTPUT_DIR = os.path.join(consts.MEDIA_DIR, "videos")
    elif config["video_output_dir"]:
        consts.VIDEO_OUTPUT_DIR = config["video_output_dir"]
    else:
        consts.VIDEO_DIR = config["video_dir"]

    for folder in [consts.VIDEO_DIR, consts.VIDEO_OUTPUT_DIR, consts.TEX_DIR, consts.TEXT_DIR]:
        if folder != "" and not os.path.exists(folder):
            os.makedirs(folder)


def add_extension_if_not_present(file_name, extension):
    # This could conceivably be smarter about handling existing differing extensions
    if file_name[-len(extension):] != extension:
        return file_name + extension
    else:
        return file_name


def guarantee_existence(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.abspath(path)


def seek_full_path_from_defaults(file_name, default_dir, extensions):
    possible_paths = [file_name]
    possible_paths += [
        os.path.join(default_dir, file_name + extension)
        for extension in ["", *extensions]
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    raise IOError("File {} not Found".format(file_name))


def get_sorted_integer_files(directory,
                             min_index=0,
                             max_index=np.inf,
                             remove_non_integer_files=False,
                             remove_indices_greater_than=None,
                             extension=None,
                             ):
    indexed_files = []
    for file in os.listdir(directory):
        if '.' in file:
            index_str = file[:file.index('.')]
        else:
            index_str = file

        full_path = os.path.join(directory, file)
        if index_str.isdigit():
            index = int(index_str)
            if remove_indices_greater_than is not None:
                if index > remove_indices_greater_than:
                    os.remove(full_path)
                    continue
            if extension is not None and not file.endswith(extension):
                continue
            if index >= min_index and index < max_index:
                indexed_files.append((index, file))
        elif remove_non_integer_files:
            os.remove(full_path)
    indexed_files.sort(key=lambda p: p[0])
    return list(map(lambda p: os.path.join(directory, p[1]), indexed_files))
