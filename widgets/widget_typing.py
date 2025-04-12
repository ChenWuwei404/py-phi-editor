__all__ = [
    'ColorLike'
]

from pygame import Color
from typing import Union

ColorLike = Union[Color, tuple[int, int, int], tuple[int, int, int, int]]