import pygame

pygame.init()


from i18n import set_language, gettext as _
set_language('zh')

from widgets import *

from editor import Editor

class EditorMenuBar(MenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.file_button = MenuBarButton(_("File"))
        self.add_child(self.file_button)

        self.edit_button = MenuBarButton(_("Edit"))
        self.add_child(self.edit_button)

        self.view_button = MenuBarButton(_("View"))
        self.add_child(self.view_button)

        self.play_button = MenuBarButton(_("Play"))
        self.add_child(self.play_button)

        self.help_button = MenuBarButton(_("Help"))
        self.add_child(self.help_button)

editor_menu_bar = EditorMenuBar()

class StatueBar(MenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_height(32)
        self.set_padding(Padding(8))

        self.version_label = Label(_("PyPhiEditor 0.0.1"))
        self.add_child(self.version_label)

statue_bar = StatueBar()


screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("PyPhiEditor")
pygame.display.set_icon(pygame.image.load(r'./resource/phi.png'))

main_page = Page(screen)
main_page.set_spacing(0)
main_page.set_layout(VBoxLayout())
main_page.add_child(editor_menu_bar)
editor_area = Editor()
main_page.add_child(editor_area)
main_page.add_child(statue_bar)


def add_right_click_menu_test(event: pygame.Event):
    right_test = RightClickMenu(event.pos)
    right_test.add_child(RightClickMenuTitle(_("Position Clip")))
    right_test.add_child(RightClickButton(_("Copy")))
    right_test.add_child(RightClickButton(_("Cut")))
    delete_button = OnceRightClickButton(_("Delete"))
    delete_button.set_color((255, 64, 64))
    right_test.add_child(delete_button)
    right_test.add_child(MenuSeparator())
    right_test.add_child(RightClickButton(_("Edit Source")))
    right_test.add_child(MenuSeparator())
    right_test.add_child(RightClickButton(_("Add Modifier")))
    right_test.add_child(RightClickButton(_("Multiline Edit")))
    main_page.add_pinned_child(right_test)

editor_area.timeline_area.right_pressed.connect(add_right_click_menu_test)

clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type in UI_EVENTS:
            main_page.process_event(event)


    screen.fill((0, 0, 0))
    main_page.update()
    main_page.draw(screen)
    

    clock.tick(0)
    pygame.display.update()
    print(clock.get_fps())