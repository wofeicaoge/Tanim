#!/usr/bin/env python
import code
import os
import subprocess

import corelib.config
import corelib.extract_scene
from corelib.scene.scene import Scene


def main():
    args = corelib.config.parse_cli()
    conf = corelib.config.get_configuration(args)
    corelib.constants.initialize_directories(conf)
    if not args.livestream:
        corelib.extract_scene.main(conf)
    else:
        if not args.to_twitch:
            fnull = open(os.devnull, 'w')
            subprocess.Popen(
                [corelib.constants.STREAMING_CLIENT, corelib.constants.STREAMING_URL],
                stdout=fnull,
                stderr=fnull)

        variables = globals().copy()
        variables.update(locals())
        shell = code.InteractiveConsole(variables)
        shell.push(f"tanim = Scene(**conf)")
        shell.push("from imports import *")
        shell.interact(banner=corelib.constants.STREAMING_CONSOLE_BANNER)
