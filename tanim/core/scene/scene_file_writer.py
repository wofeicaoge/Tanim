import datetime
import os
import shutil
import subprocess
from time import sleep

from pydub import AudioSegment
import numpy as np

from tanim.utils.config_ops import digest_config
import tanim.utils.constants as consts
from tanim.utils.file_ops import add_extension_if_not_present
from tanim.utils.file_ops import guarantee_existence
from tanim.utils.sounds import get_full_sound_file_path


def print_file_ready_message(file_path):
    print("\nFile ready at {}\n".format(file_path))


class SceneFileWriter(object):
    CONFIG = {
        "write_to_movie": False,
        # TODO, save_pngs is doing nothing
        "save_pngs": False,
        "png_mode": "RGBA",
        "save_last_frame": False,
        "movie_file_extension": ".mp4",
        "gif_file_extension": ".gif",
        "livestreaming": False,
        "to_twitch": False,
        "twitch_key": None,
        # Previous output_file_name
        # TODO, address this in extract_scene et. al.
        "file_name": None,
        "input_file_path": "",  # ??
        "output_directory": None,
    }

    def __init__(self, scene, **kwargs):
        digest_config(self, kwargs)
        self.scene = scene
        self.loop_run = True
        # For livestreaming, if we don't stop idle stream updating,
        # it could conflict with animation to cause flashing
        self.stop_update = False
        self.init_output_directories()
        self.init_audio()

    # Output directories and files
    def init_output_directories(self):
        module_directory = self.output_directory or self.get_default_module_directory()
        scene_name = self.file_name or self.get_default_scene_name()
        if self.save_last_frame:
            if consts.VIDEO_DIR != "":
                image_dir = guarantee_existence(os.path.join(
                    consts.VIDEO_DIR,
                    module_directory,
                    "images",
                ))
            else:
                image_dir = guarantee_existence(os.path.join(
                    consts.VIDEO_OUTPUT_DIR,
                    "images",
                ))
            self.image_file_path = os.path.join(
                image_dir,
                add_extension_if_not_present(scene_name, ".png")
            )
        if self.write_to_movie:
            if consts.VIDEO_DIR != "":
                movie_dir = guarantee_existence(os.path.join(
                    consts.VIDEO_DIR,
                    module_directory,
                    self.get_resolution_directory(),
                ))
            else:
                movie_dir = guarantee_existence(consts.VIDEO_OUTPUT_DIR)
            self.movie_file_path = os.path.join(
                movie_dir,
                add_extension_if_not_present(
                    scene_name, self.movie_file_extension
                )
            )
            self.gif_file_path = os.path.join(
                movie_dir,
                add_extension_if_not_present(
                    scene_name, self.gif_file_extension
                )
            )

    def get_default_module_directory(self):
        filename = os.path.basename(self.input_file_path)
        root, _ = os.path.splitext(filename)
        return root

    def get_default_scene_name(self):
        if self.file_name is None:
            return self.scene.__class__.__name__
        else:
            return self.file_name

    def get_resolution_directory(self):
        pixel_height = self.scene.camera.pixel_height
        frame_rate = self.scene.camera.frame_rate
        return "{}p{}".format(
            pixel_height, frame_rate
        )

    # Directory getters
    def get_image_file_path(self):
        return self.image_file_path

    def get_movie_file_path(self):
        return self.movie_file_path

    # Sound
    def init_audio(self):
        self.includes_sound = False

    def create_audio_segment(self):
        self.audio_segment = AudioSegment.silent()

    def add_audio_segment(self, new_segment,
                          time=None,
                          gain_to_background=None):
        if not self.includes_sound:
            self.includes_sound = True
            self.create_audio_segment()
        segment = self.audio_segment
        curr_end = segment.duration_seconds
        if time is None:
            time = curr_end
        if time < 0:
            raise Exception("Adding sound at timestamp < 0")

        new_end = time + new_segment.duration_seconds
        diff = new_end - curr_end
        if diff > 0:
            segment = segment.append(
                AudioSegment.silent(int(np.ceil(diff * 1000))),
                crossfade=0,
            )
        self.audio_segment = segment.overlay(
            new_segment,
            position=int(1000 * time),
            gain_during_overlay=gain_to_background,
        )

    def add_sound(self, sound_file, time=None, gain=None, **kwargs):
        file_path = get_full_sound_file_path(sound_file)
        new_segment = AudioSegment.from_file(file_path)
        if gain:
            new_segment = new_segment.apply_gain(gain)
        self.add_audio_segment(new_segment, time, **kwargs)

    # Writers
    def pause_idle_update(self):
        self.stop_update = True

    def resume_idle_update(self):
        self.stop_update = False

    def stop_stream_loop(self):
        self.loop_run = False

    def begin_stream(self):
        if self.write_to_movie:
            self.open_movie_pipe()

    def end_stream(self):
        if self.write_to_movie:
            self.close_movie_pipe()

    def stream_loop(self):
        self.begin_stream()
        frame_duration = 1 / self.scene.camera.frame_rate
        while self.loop_run:
            a = datetime.datetime.now()
            if self.scene.has_frame():
                frame = self.scene.fetch_frame()
                self.write_frame(frame)
            # We only keep animation in non livestream
            # and record every changes in livestream
            elif self.livestreaming and not self.stop_update:
                self.scene.update_frame()
                frame = self.scene.get_latest_frame()
                self.scene.add_frames(frame)
            b = datetime.datetime.now()
            time_diff = (b - a).total_seconds()
            if time_diff < frame_duration:
                sleep(frame_duration - time_diff)

        while self.scene.has_frame():
            frame = self.scene.fetch_frame()
            self.write_frame(frame)

        self.end_stream()

    def write_frame(self, frame):
        if self.write_to_movie:
            self.writing_process.stdin.write(frame.tostring())

    def save_final_image(self, image):
        file_path = self.get_image_file_path()
        image.save(file_path)
        print_file_ready_message(file_path)

    def finish(self):
        if self.livestreaming:
            return
        self.loop_run = False
        if self.write_to_movie and self.includes_sound:
            self.combine_sound()
        if self.save_last_frame:
            self.scene.update_frame(ignore_skipping=True)
            self.save_final_image(self.scene.get_image())

    def open_movie_pipe(self):
        fps = self.scene.camera.frame_rate
        height = self.scene.camera.get_pixel_height()
        width = self.scene.camera.get_pixel_width()

        command = [
            consts.FFMPEG_BIN,
            '-y',  # overwrite output file if it exists
            '-f', 'rawvideo',
            '-s', '%dx%d' % (width, height),  # size of one frame
            '-pix_fmt', 'rgba',
            '-r', str(fps),  # frames per second
            '-i', '-',  # The imput comes from a pipe
            '-an',  # Tells FFMPEG not to expect any audio
            '-loglevel', 'error',
        ]
        # TODO, the test for a transparent background should not be based on
        # the file extension.
        if self.movie_file_extension == ".mov":
            # This is if the background of the exported
            # video should be transparent.
            command += [
                '-vcodec', 'qtrle',
            ]
        else:
            command += [
                '-vcodec', 'libx264',
                '-pix_fmt', 'yuv420p',
            ]
        if self.livestreaming:
            if self.to_twitch:
                command += ['-f', 'flv']
                command += ['rtmp://live.twitch.tv/app/' + self.twitch_key]
            else:
                command += ['-f', 'mpegts']
                command += [consts.STREAMING_PROTOCOL + '://' + consts.STREAMING_IP + ':' + consts.STREAMING_PORT]
        else:
            command += [self.movie_file_path]
        self.writing_process = subprocess.Popen(command, stdin=subprocess.PIPE)

    def close_movie_pipe(self):
        self.writing_process.stdin.close()
        self.writing_process.wait()

    def combine_sound(self):
        movie_file_path = self.get_movie_file_path()
        sound_file_path = movie_file_path.replace(
            self.movie_file_extension, ".wav"
        )
        # Makes sure sound file length will match video file
        self.add_audio_segment(AudioSegment.silent(0))
        self.audio_segment.export(
            sound_file_path,
            bitrate='312k',
        )
        temp_file_path = movie_file_path.replace(".", "_temp.")
        commands = [
            "ffmpeg",
            "-i", movie_file_path,
            "-i", sound_file_path,
            '-y',  # overwrite output file if it exists
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "320k",
            # select video stream from first file
            "-map", "0:v:0",
            # select audio stream from second file
            "-map", "1:a:0",
            '-loglevel', 'error',
            # "-shortest",
            temp_file_path,
        ]
        subprocess.call(commands)
        shutil.move(temp_file_path, movie_file_path)
        os.remove(sound_file_path)

        print_file_ready_message(movie_file_path)
