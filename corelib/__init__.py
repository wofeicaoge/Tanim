#!/usr/bin/env python
import corelib.config
import corelib.constants
import corelib.extract_scene
from time import sleep
import code
import os
import subprocess

from corelib.scene.scene import Scene
import corelib.constants


def main():
    args = corelib.config.parse_cli()
    conf = corelib.config.get_configuration(args)
    corelib.constants.initialize_directories(conf)
    if not args.livestream:
        corelib.extract_scene.main(conf)
    else:
        if not args.to_twitch:
            FNULL = open(os.devnull, 'w')
            subprocess.Popen(
                [corelib.constants.STREAMING_CLIENT, corelib.constants.STREAMING_URL],
                stdout=FNULL,
                stderr=FNULL)

        variables = globals().copy()
        variables.update(locals())
        shell = code.InteractiveConsole(variables)
        shell.push(f"tanim = Scene(**conf)")
        shell.push("from corelib.imports import *")
        shell.interact(banner=corelib.constants.STREAMING_CONSOLE_BANNER)
