from torchvision.datasets import *
from .grasp_cifar10_dber import GraspCifar10 as GraspCifar10
from .grip_cifar10_dber import GripCifar10 as GripCifar10
from .suction_cifar10_dber import SuctionCifar10 as SuctionCifar10
from typing import Any

def get_mean_std(name: Any): ...
def Dataset(name: Any, **kwargs: Any): ...
