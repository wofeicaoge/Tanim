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


from corelib.constants import *

from extention.animation.animation_group import *
from extention.animation.creation import *
from extention.animation.transform import *
from extention.animation.specialized import *

from corelib.animation.fading import *
from corelib.animation.growing import *
from corelib.animation.indication import *
from corelib.animation.movement import *
from corelib.animation.numbers import *
from corelib.animation.rotation import *
from corelib.animation.update import *

from corelib.camera.camera import *
from corelib.camera.mapping_camera import *
from corelib.camera.moving_camera import *
from corelib.camera.three_d_camera import *

from corelib.mobject.coordinate_systems import *
from corelib.mobject.changing import *
from corelib.mobject.frame import *
from corelib.mobject.functions import *
from corelib.mobject.geometry import *
from corelib.mobject.matrix import *
from corelib.mobject.mobject import *
from corelib.mobject.number_line import *
from corelib.mobject.numbers import *
from corelib.mobject.probability import *
from corelib.mobject.shape_matchers import *
from corelib.mobject.svg.brace import *
from corelib.mobject.svg.drawings import *
from corelib.mobject.svg.svg_mobject import *
from corelib.mobject.svg.tex_mobject import *
from corelib.mobject.svg.text_mobject import *
from corelib.mobject.three_d_utils import *
from corelib.mobject.three_dimensions import *
from corelib.mobject.types.image_mobject import *
from corelib.mobject.types.point_cloud_mobject import *
from corelib.mobject.types.vectorized_mobject import *
from corelib.mobject.mobject_update_utils import *
from corelib.mobject.value_tracker import *
from corelib.mobject.vector_field import *

from corelib.scene.graph_scene import *
from corelib.scene.moving_camera_scene import *
from corelib.scene.reconfigurable_scene import *
from corelib.scene.scene import *
from corelib.scene.sample_space_scene import *
from corelib.scene.graph_scene import *
from corelib.scene.scene_from_video import *
from corelib.scene.three_d_scene import *
from corelib.scene.vector_space_scene import *
from corelib.scene.zoomed_scene import *

from corelib.utils.bezier import *
from corelib.utils.color import *
from corelib.utils.config_ops import *
from corelib.utils.debug import *
from corelib.utils.images import *
from corelib.utils.iterables import *
from corelib.utils.file_ops import *
from corelib.utils.paths import *
from corelib.utils.rate_functions import *
from corelib.utils.simple_functions import *
from corelib.utils.sounds import *
from corelib.utils.space_ops import *
from corelib.utils.strings import *

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

from PIL import Image
from colour import Color
