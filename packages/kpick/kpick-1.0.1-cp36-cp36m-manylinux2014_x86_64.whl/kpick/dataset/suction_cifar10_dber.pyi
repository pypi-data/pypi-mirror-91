from .grasp_cifar10_dber import GraspCifar10 as GraspCifar10
from typing import Any, Optional

class SuctionCifar10(GraspCifar10):
    def __init__(self, root: Optional[Any] = ..., train: bool = ..., transform: Optional[Any] = ..., target_transform: Optional[Any] = ..., download: bool = ..., im_shape: Any = ..., data: Optional[Any] = ..., indexing: bool = ..., base_folder: str = ...) -> None: ...
