from pygame import Surface, draw, Color, image, Event, transform, surfarray

from numpy import max as np_max

from widgets import *

from i18n import gettext as _
from widgets.widget import Widget

class EditorMenuBar(MenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_padding(Padding(0, 8, 0, 8))
        self.background_color_normal = Color(24, 24, 24)

class PlayerArea(Card):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.border_width = 0
        self.set_padding(Padding(0))
        self.set_background_image(Surface((1600, 900)))
        self.background_color_normal = Color(0, 0, 0, 0)

    def set_background_image(self, image: Surface):
        self.background_image = transform.smoothscale(image, (1600, 900))
        self.background_image_blurred = transform.gaussian_blur(self.background_image, 100)
        array = surfarray.pixels3d(self.background_image_blurred)
        array[:, :, :] = array[:, :, :] * 0.5

    def draw_background(self, canvas: Surface):
        super().draw_background(canvas)
        canvas.blit(transform.scale(self.background_image_blurred, self.get_size()), self.get_pos())
        

class EditorCard(Card):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.set_padding(Padding(1))
        self.set_layout(VBoxLayout())
        self.set_spacing(0)

        self.menu_bar = EditorMenuBar()
        self.add_child(self.menu_bar)


class OutlineEditor(EditorCard):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.menu_bar.add_child(Icon(image.load_sized_svg(r'./resource/icon/layer.svg', (20, 20))))

        self.menu_add_button = MenuBarButton(_("Add"))
        self.menu_bar.add_child(self.menu_add_button)
        def add_button_menu(event: Event):
            x, y = self.menu_add_button.absolute_rect.topleft
            menu = RightClickMenu((x, y + self.menu_bar.height))

            menu.add_child(RightClickButton(_("Judge-line")))
            menu.add_child(MenuSeparator())
            menu.add_child(RightClickButton(_("Point")))
            menu.add_child(RightClickButton(_("Intersection")))
            menu.add_child(RightClickButton(_("Parametric Curves")))
            menu.add_child(MenuSeparator())
            menu.add_child(RightClickButton(_("Folder")))

            self.get_root().add_pinned_child(menu)
        self.menu_add_button.left_pressed.connect(add_button_menu)



class Timeline(Widget):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.set_size(-1, -1)
        self.set_padding(Padding(0))
        self.set_layout(HBoxLayout())

        self.tracks_column = BackgroundBase()
        self.tracks_column.background_color_normal = Color(20, 20, 20)
        self.tracks_column.set_size(200, -1)
        self.add_child(self.tracks_column)

class TimelineEditor(EditorCard):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.menu_bar.add_child(Icon(image.load_sized_svg(r'./resource/icon/timeline.svg', (20, 20))))

        self.menu_add_button = MenuBarButton(_("Add"))
        self.menu_bar.add_child(self.menu_add_button)
        def add_button_menu(event: Event):
            x, y = self.menu_add_button.absolute_rect.topleft
            menu = RightClickMenu((x, y + self.menu_bar.height))

            menu.add_child(RightClickButton(_("Note Clip")))
            menu.add_child(MenuSeparator())
            menu.add_child(RightClickButton(_("Position Clip")))
            menu.add_child(RightClickButton(_("Rotation Clip")))
            menu.add_child(RightClickButton(_("Alpha Clip")))
            menu.add_child(RightClickButton(_("Velocity Clip")))

            self.get_root().add_pinned_child(menu)
        self.menu_add_button.left_pressed.connect(add_button_menu)

        self.timeline = Timeline()
        self.add_child(self.timeline)

class Editor(Widget):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.set_padding(Padding(0))
        self.set_spacing(2)
        self.set_size(-1, -1)

        self.outline_area = OutlineEditor()
        self.player_area = PlayerArea()
        self.attributes_area = EditorCard()
        self.timeline_area = TimelineEditor()
        self.editor_area = EditorCard()

        self.outline_area.set_parent(self)
        self.player_area.set_parent(self)
        self.attributes_area.set_parent(self)
        self.timeline_area.set_parent(self)
        self.editor_area.set_parent(self)

        self.set_layout(EditorGrid(self))

    def get_children(self) -> list[Widget]:
        return super().get_children() + [
            self.outline_area,
            self.player_area,
            self.attributes_area,
            self.timeline_area,
            self.editor_area,
        ]

class EditorGrid(Layout):
    """
    +---+------+-----+
    | o | plyr | att |
    +---+------+-----+
    | timeline | edt |
    +----------+-----+
    outline_area, player_area, attributes_area, timeline_area, editor_area
    """
    def get_parent(self) -> Editor:
        if isinstance(self.parent, Editor):
            return self.parent
        else:
            raise ValueError("Parent of EditorGrid must be Editor")
        
    def __init__(self, parent: Editor) -> None:
        super().__init__()

        self.player_width_percent = 0.4
        self.timeline_width_percent = 0.7
    
    @property
    def player_width(self) -> int:
        return int(self.get_parent().content_width * self.player_width_percent)
    
    @property
    def player_height(self) -> int:
        return self.player_width*9//16

    @property
    def timeline_width(self) -> int:
        return int(self.get_parent().content_width * self.timeline_width_percent)
    
    @property
    def timeline_height(self) -> int:
        return self.get_parent().content_height - self.player_height
    
    @property
    def outline_height(self) -> int:
        return self.player_height
    
    @property
    def outline_width(self) -> int:
        return self.timeline_width - self.player_width
    
    @property
    def attributes_height(self) -> int:
        return self.player_height
    
    @property
    def attributes_width(self) -> int:
        return self.get_parent().content_width - self.timeline_width
    
    @property
    def editor_height(self) -> int:
        return self.timeline_height
    
    @property
    def editor_width(self) -> int:
        return self.get_parent().content_width - self.timeline_width
    
    def update(self) -> None:
        outline_area = self.get_parent().outline_area
        outline_area.set_size(self.outline_width, self.outline_height)
        outline_area.set_pos(0, 0)

        player_area = self.get_parent().player_area
        player_area.set_size(self.player_width, self.player_height)
        player_area.set_pos(self.outline_width, 0)

        attributes_area = self.get_parent().attributes_area
        attributes_area.set_size(self.attributes_width, self.attributes_height)
        attributes_area.set_pos(self.outline_width + self.player_width, 0)

        timeline_area = self.get_parent().timeline_area
        timeline_area.set_size(self.timeline_width, self.timeline_height)
        timeline_area.set_pos(0, self.player_height)

        editor_area = self.get_parent().editor_area
        editor_area.set_size(self.editor_width, self.editor_height)
        editor_area.set_pos(self.timeline_width, self.player_height)

