#!/usr/bin/env python
import code
import os
import subprocess

import tanim.utils.constants as consts
import tanim.utils.extract_scene
from tanim.utils.file_ops import initialize_directories
from tanim.utils.config import parse_cli


def main():
    args = parse_cli()
    conf = tanim.utils.config.get_configuration(args)
    initialize_directories(conf)
    if not args.livestream:
        tanim.utils.extract_scene.main(conf)
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
