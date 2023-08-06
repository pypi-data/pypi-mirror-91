from ttcv.import_basic_utils import *
from ..utils.grip_utils import GRIP as GRIP, GRIPS as GRIPS
from ttcv.basic.basic_objects import BasObj as BasObj
from typing import Any

def find_grip_pts(args: Any, rgbd_pad: Any, pad_mask: Any, angles: Any, pad_x: Any, pad_y: Any, center: Any): ...
def find_grip_pts_ray(args: Any, rgbd_pad: Any, pad_mask: Any, angles: Any, pad_x: Any, pad_y: Any, center: Any): ...

class EdgePairFinder:
    def find_grip_candidates_from_edges(self, rgbd: Any, args: Any, use_ray: bool = ...): ...
