import pygame

pygame.init()


from i18n import set_language, gettext as _
set_language('zh')

from widgets import *

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


screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("PyPhiEditor")
pygame.display.set_icon(pygame.image.load(r'./resource/phi.png'))

main_page = Page(screen)
main_page.set_layout(VBoxLayout())
main_page.add_child(editor_menu_bar)

def add_right_click_menu_test(event: pygame.Event):
    right_test = RightClickMenu(event.pos)
    right_test.add_child(Lable(_("Tap")))
    right_test.add_child(OneTimeRightClickButton(_("Delete")))
    right_test.add_child(MenuSeparator())
    right_test.add_child(RightClickButton(_("Copy")))
    right_test.add_child(RightClickButton(_("Paste")))
    right_test.add_child(MenuSeparator())
    right_test.add_child(RightClickButton(_("Undo")))
    right_test.add_child(RightClickButton(_("Redo")))
    main_page.add_pinned_child(right_test)

main_page.right_pressed.connect(add_right_click_menu_test)

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
    

    clock.tick(61)
    pygame.display.update()
    print(clock.get_fps())