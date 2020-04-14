#!/usr/bin/env python
import code
import os
import subprocess

import extention.utils.config
import extention.utils.extract_scene
import extention.utils.constants as consts
from corelib.scene.scene import Scene


def main():
    args = extention.utils.config.parse_cli()
    conf = extention.utils.config.get_configuration(args)
    consts.initialize_directories(conf)
    if not args.livestream:
        extention.utils.extract_scene.main(conf)
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
