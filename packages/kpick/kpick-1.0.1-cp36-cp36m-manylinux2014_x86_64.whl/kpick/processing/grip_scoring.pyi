from ttcv.import_basic_utils import *
from ttdet.cifar_classfication.classification_v2 import BasCifarClassfier
from typing import Any

class GripScorer(BasCifarClassfier):
    def predict_point(self, rgbd: Any, pt: Any): ...
    def predict_point_crop(self, rgbd: Any, pt: Any): ...
