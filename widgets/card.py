from typing import Optional

from pygame import Surface, Rect, draw, surfarray

from .background_base import BackgroundBase, DynamicBackgroundBase
from .border_base import BorderBase

from .widget import Widget

from numpy_renderer import painter
from numpy import ndarray

class Card(BackgroundBase, BorderBase):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.border_radius = 8

        self.corners_cache: tuple[Optional[ndarray], Optional[ndarray], Optional[ndarray], Optional[ndarray]] = (None, None, None, None)

    def draw_background(self, canvas: Surface):
        canvas_rect = canvas.get_rect()

        x, y, width, height = self.visual_rect

        left_top_rect = Rect(x, y, self.border_radius, self.border_radius)
        right_top_rect = Rect(x + width - self.border_radius, y, self.border_radius, self.border_radius)
        left_bottom_rect = Rect(x, y + height - self.border_radius, self.border_radius, self.border_radius)
        right_bottom_rect = Rect(x + width - self.border_radius, y + height - self.border_radius, self.border_radius, self.border_radius)

        left_top = surfarray.array3d(canvas.subsurface(left_top_rect.clip(canvas_rect))) if left_top_rect.colliderect(canvas_rect) else None
        right_top = surfarray.array3d(canvas.subsurface(right_top_rect.clip(canvas_rect))) if right_top_rect.colliderect(canvas_rect) else None
        left_bottom = surfarray.array3d(canvas.subsurface(left_bottom_rect.clip(canvas_rect))) if left_bottom_rect.colliderect(canvas_rect) else None
        right_bottom = surfarray.array3d(canvas.subsurface(right_bottom_rect.clip(canvas_rect))) if right_bottom_rect.colliderect(canvas_rect) else None
        self.corners_cache = (right_bottom, right_top, left_bottom, left_top)
        
        return super().draw_background(canvas)

    def draw_shape(self, canvas: Surface):
        painter.corner_redraw_rect(canvas, self.border_color, self.border_width, self.visual_rect, self.border_radius, self.corners_cache)

class DynamicCard(Card, DynamicBackgroundBase):
    pass

