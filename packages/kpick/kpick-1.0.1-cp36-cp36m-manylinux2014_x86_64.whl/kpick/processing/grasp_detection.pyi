from common.utils.proc_utils import *
from .grip_detection import GripDetector as GripDetector
from .suction_detection import SuctionDetector as SuctionDetector
from typing import Any

def find_grasp_pose(org_im: Any, depth: Any, boxes_list: Any, masks_list: Any, classes: Any): ...
