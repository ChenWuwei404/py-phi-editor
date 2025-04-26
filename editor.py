from pygame import Surface, draw, Color

from widgets import *

from i18n import gettext as _

class EditorMenuBar(MenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_padding(Padding(0, 8, 0, 8))
        self.background_color_normal = Color(24, 24, 24)

class EditorCard(Card):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.set_padding(Padding(0))
        self.set_layout(VBoxLayout())

        self.menu_bar = EditorMenuBar()
        self.add_child(self.menu_bar)

class TimeLineEditor(EditorCard):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.menu_bar.add_child(Label(_("Timeline")))
        self.menu_bar.add_child(MenuBarButton(_("View")))

class Editor(Widget):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.set_padding(Padding(0))
        self.set_spacing(2)
        self.set_size(-1, -1)

        self.outline_area = EditorCard()
        self.player_area = EditorCard()
        self.attributes_area = EditorCard()
        self.timeline_area = TimeLineEditor()
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

