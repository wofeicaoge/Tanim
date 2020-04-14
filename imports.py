"""
I won't pretend like this is best practice, by in creating animations for a video,
it can be very nice to simply have all of the Mobjects, Animations, Scenes, etc.
of tanim available without having to worry about what namespace they come from.

Rather than having a large pile of "from <module> import *" at the top of every such
script, the intent of this file is to make it so that one can just include
"from corelib.imports import *".  The effects of adding more modules
or refactoring the library on current or older scene scripts should be entirely
addressible by changing this file.

Note: One should NOT import from this file for main library code, it is meant only
as a convenience for scripts creating scenes for videos.
"""


from utils.constants import *

from utils.config import *

from corelib.animation.animation import *
from corelib.animation.creation import *
from corelib.animation.transform import *
from corelib.animation.movement import *
from corelib.animation.rotation import *
from corelib.animation.update import *
from extention.animation.animation_group import *
from extention.animation.creation import *
from extention.animation.transform import *
from extention.animation.specialized import *
from extention.animation.fading import *
from extention.animation.growing import *
from extention.animation.indication import *
from extention.animation.numbers import *
from extention.animation.movement import *

from corelib.camera.camera import *
from extention.camera.mapping_camera import *
from extention.camera.moving_camera import *
from extention.camera.three_d_camera import *

from corelib.mobject.mobject import *
from corelib.mobject.image_mobject import *
from corelib.mobject.point_cloud_mobject import *
from corelib.mobject.vectorized_mobject import *
from extention.mobject.coordinate_systems import *
from extention.mobject.changing import *
from extention.mobject.frame import *
from extention.mobject.functions import *
from extention.mobject.geometry import *
from extention.mobject.matrix import *
from extention.mobject.number_line import *
from extention.mobject.numbers import *
from extention.mobject.probability import *
from extention.mobject.shape_matchers import *
from extention.mobject.svg.brace import *
from extention.mobject.svg.drawings import *
from extention.mobject.svg.svg_mobject import *
from extention.mobject.svg.tex_mobject import *
from extention.mobject.svg.text_mobject import *
from extention.mobject.three_dimensions import *
from extention.mobject.value_tracker import *
from extention.mobject.vector_field import *

from corelib.scene.scene import *
from extention.scene.graph_scene import *
from extention.scene.moving_camera_scene import *
from extention.scene.reconfigurable_scene import *
from extention.scene.sample_space_scene import *
from extention.scene.graph_scene import *
from extention.scene.three_d_scene import *
from extention.scene.vector_space_scene import *
from extention.scene.zoomed_scene import *

from utils.bezier import *
from utils.color import *
from utils.config_ops import *
from utils.debug import *
from utils.images import *
from utils.iterables import *
from utils.file_ops import *
from utils.paths import *
from utils.rate_functions import *
from utils.simple_functions import *
from utils.sounds import *
from utils.space_ops import *
from utils.strings import *
from utils.three_d_utils import *
from utils.mobject_update_utils import *


# Non tanim libraries that are also nice to have without thinking

import inspect
import itertools as it
import numpy as np
import operator as op
import os
import random
import re
import string
import sys
import math
import sympy as sp
import subprocess

from PIL import Image
from colour import Color