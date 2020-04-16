import tanim.utils.constants as consts
from tanim.utils.simple_functions import fdiv

from tanim.core.mobject.image_mobject import ImageMobjectFromCamera

from tanim.extention.scene.moving_camera_scene import MovingCameraScene
from tanim.extention.camera.moving_camera import MovingCamera
from tanim.extention.camera.multi_camera import MultiCamera
from tanim.extention.animation.transform import ApplyMethod

# Note, any scenes from old videos using ZoomedScene will almost certainly
# break, as it was restructured.


class ZoomedScene(MovingCameraScene):
    camera_class = MultiCamera
    zoomed_display_height = 3
    zoomed_display_width = 3
    zoomed_display_center = None
    zoomed_display_corner = consts.UP + consts.RIGHT
    zoomed_display_corner_buff = consts.DEFAULT_MOBJECT_TO_EDGE_BUFFER
    zoomed_camera_config = {
            "default_frame_stroke_width": 2,
            "background_opacity": 1
    }
    zoomed_camera_image_mobject_config = {}
    zoomed_camera_frame_starting_position = consts.ORIGIN
    zoom_factor = 0.15
    image_frame_stroke_width = 3
    zoom_activated = False

    def setup(self):
        MovingCameraScene.setup(self)
        # Initialize camera and display
        zoomed_camera = MovingCamera(**self.zoomed_camera_config)
        zoomed_display = ImageMobjectFromCamera(
            zoomed_camera, **self.zoomed_camera_image_mobject_config
        )
        zoomed_display.add_display_frame()
        for mob in zoomed_camera.frame, zoomed_display:
            mob.stretch_to_fit_height(self.zoomed_display_height)
            mob.stretch_to_fit_width(self.zoomed_display_width)
        zoomed_camera.frame.scale(self.zoom_factor)

        # Position camera and display
        zoomed_camera.frame.move_to(self.zoomed_camera_frame_starting_position)
        if self.zoomed_display_center is not None:
            zoomed_display.move_to(self.zoomed_display_center)
        else:
            zoomed_display.to_corner(
                self.zoomed_display_corner,
                buff=self.zoomed_display_corner_buff
            )

        self.zoomed_camera = zoomed_camera
        self.zoomed_display = zoomed_display

    def activate_zooming(self, animate=False):
        self.zoom_activated = True
        self.camera.add_image_mobject_from_camera(self.zoomed_display)
        if animate:
            self.play(self.get_zoom_in_animation())
            self.play(self.get_zoomed_display_pop_out_animation())
        self.add(
            self.zoomed_camera.frame,
            self.zoomed_display,
        )

    def get_zoom_in_animation(self, run_time=2, **kwargs):
        frame = self.zoomed_camera.frame
        full_frame_height = self.camera.get_frame_height()
        full_frame_width = self.camera.get_frame_width()
        frame.save_state()
        frame.stretch_to_fit_width(full_frame_width)
        frame.stretch_to_fit_height(full_frame_height)
        frame.center()
        frame.set_stroke(width=0)
        return ApplyMethod(frame.restore, run_time=run_time, **kwargs)

    def get_zoomed_display_pop_out_animation(self, **kwargs):
        display = self.zoomed_display
        display.save_state(use_deepcopy=True)
        display.replace(self.zoomed_camera.frame, stretch=True)
        return ApplyMethod(display.restore)

    def get_zoom_factor(self):
        return fdiv(
            self.zoomed_camera.frame.get_height(),
            self.zoomed_display.get_height()
        )
