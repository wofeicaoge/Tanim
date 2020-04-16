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


from tanim.utils.constants import *

from tanim.utils.config import *

from tanim.core.animation.animation import *
from tanim.core.animation.creation import *
from tanim.core.animation.transform import *
from tanim.core.animation.movement import *
from tanim.core.animation.rotation import *
from tanim.core.animation.update import *
from tanim.extention.animation.animation_group import *
from tanim.extention.animation.creation import *
from tanim.extention.animation.transform import *
from tanim.extention.animation.specialized import *
from tanim.extention.animation.fading import *
from tanim.extention.animation.growing import *
from tanim.extention.animation.indication import *
from tanim.extention.animation.numbers import *
from tanim.extention.animation.movement import *

from tanim.core.camera.camera import *
from tanim.extention.camera.mapping_camera import *
from tanim.extention.camera.moving_camera import *
from tanim.extention.camera.three_d_camera import *

from tanim.core.mobject.mobject import *
from tanim.core.mobject.image_mobject import *
from tanim.core.mobject.point_cloud_mobject import *
from tanim.core.mobject.vectorized_mobject import *
from tanim.extention.mobject.coordinate_systems import *
from tanim.extention.mobject.changing import *
from tanim.extention.mobject.frame import *
from tanim.extention.mobject.functions import *
from tanim.extention.mobject.geometry import *
from tanim.extention.mobject.matrix import *
from tanim.extention.mobject.number_line import *
from tanim.extention.mobject.numbers import *
from tanim.extention.mobject.probability import *
from tanim.extention.mobject.shape_matchers import *
from tanim.extention.mobject.svg.brace import *
from tanim.extention.mobject.svg.drawings import *
from tanim.extention.mobject.svg.svg_mobject import *
from tanim.extention.mobject.svg.tex_mobject import *
from tanim.extention.mobject.svg.text_mobject import *
from tanim.extention.mobject.three_dimensions import *
from tanim.extention.mobject.value_tracker import *
from tanim.extention.mobject.vector_field import *

from tanim.core.scene.scene import *
from tanim.extention.scene.graph_scene import *
from tanim.extention.scene.moving_camera_scene import *
from tanim.extention.scene.reconfigurable_scene import *
from tanim.extention.scene.sample_space_scene import *
from tanim.extention.scene.graph_scene import *
from tanim.extention.scene.three_d_scene import *
from tanim.extention.scene.vector_space_scene import *
from tanim.extention.scene.zoomed_scene import *

from tanim.utils.bezier import *
from tanim.utils.color import *
from tanim.utils.config_ops import *
from tanim.utils.debug import *
from tanim.utils.images import *
from tanim.utils.iterables import *
from tanim.utils.file_ops import *
from tanim.utils.paths import *
from tanim.utils.rate_functions import *
from tanim.utils.simple_functions import *
from tanim.utils.sounds import *
from tanim.utils.space_ops import *
from tanim.utils.strings import *
from tanim.utils.three_d_utils import *
from tanim.utils.mobject_update_utils import *


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
from tanim.utils.color import Color