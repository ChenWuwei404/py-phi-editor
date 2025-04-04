from typing import Callable
from pygame import Event

class Trigger:
    def __init__(self):
        self.slots: list[Callable[[Event], None]] = []

    def connect(self, slot: Callable[[Event], None]):
        self.slots.append(slot)

    def disconnect(self, slot: Callable[[Event], None]):
        self.slots.remove(slot)

    def __call__(self, event: Event):
        [slot(event) for slot in self.slots]