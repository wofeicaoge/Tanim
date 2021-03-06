from tanim.utils.iterables import list_update

from tanim.core.mobject.mobject import Mobject
from tanim.core.scene.scene import Scene

from tanim.extention.camera.moving_camera import MovingCamera


class MovingCameraScene(Scene):
    CONFIG = {
        "camera_class": MovingCamera
    }

    def setup(self):
        Scene.setup(self)
        assert(isinstance(self.camera, MovingCamera))
        self.camera_frame = self.camera.frame
        # Hmm, this currently relies on the fact that MovingCamera
        # willd default to a full-sized frame.  Is that okay?
        return self

    def get_moving_mobjects(self, *animations):
        moving_mobjects = Scene.get_moving_mobjects(self, *animations)
        all_moving_mobjects = Mobject.extract_mobject_family_members(
            moving_mobjects
        )
        movement_indicators = self.camera.get_mobjects_indicating_movement()
        for movement_indicator in movement_indicators:
            if movement_indicator in all_moving_mobjects:
                # When one of these is moving, the camera should
                # consider all mobjects to be moving
                return list_update(self.submobjects, moving_mobjects)
        return moving_mobjects
