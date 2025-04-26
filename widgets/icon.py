from .foreground_base import ForegroundBase, DynamicForegroundBase
from .widget import Widget

from pygame import surfarray, Surface, SRCALPHA

from typing import Literal

class Icon(ForegroundBase):
    def __init__(self, mask: Surface, mask_type: Literal['alpha', 'brightness'] = 'alpha', parent: Widget | None = None):
        super().__init__(parent)
        self.mask = surfarray.array_alpha(mask) if mask_type == 'alpha' else surfarray.array_green(mask)
        self.set_size(*mask.get_size())

    def draw_foreground(self, canvas: Surface):
        icon = Surface(self.get_size(), SRCALPHA)
        icon.fill(self.foreground_color)
        surfarray.pixels_alpha(icon)[:] = self.mask
        canvas.blit(icon, self.get_pos())

class DynamicIcon(Icon, DynamicForegroundBase):
    pass