from typing import overload

class Padding:
    @overload
    def __init__(self, padding: int) -> None:...
    @overload
    def __init__(self, padding_top: int, padding_right: int, padding_bottom: int, padding_left: int) -> None:...
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            self.top = self.right = self.bottom = self.left = args[0]
        elif len(args) == 4:
            self.top, self.right, self.bottom, self.left = args
        else:
            raise ValueError("Invalid number of arguments")