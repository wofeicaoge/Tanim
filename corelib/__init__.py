#!/usr/bin/env python
import code
import os
import subprocess

import utils.config
import utils.extract_scene
import utils.constants as consts
from utils.file_ops import initialize_directories

from corelib.scene.scene import Scene


def main():
    args = utils.config.parse_cli()
    conf = utils.config.get_configuration(args)
    initialize_directories(conf)
    if not args.livestream:
        utils.extract_scene.main(conf)
    else:
        if not args.to_twitch:
            fnull = open(os.devnull, 'w')
            subprocess.Popen(
                [consts.STREAMING_CLIENT, consts.STREAMING_URL],
                stdout=fnull,
                stderr=fnull)

        variables = globals().copy()
        variables.update(locals())
        shell = code.InteractiveConsole(variables)
        shell.push(f"tanim = Scene(**conf)")
        shell.push("from imports import *")
        shell.interact(banner=consts.STREAMING_CONSOLE_BANNER)
