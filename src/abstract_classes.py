from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass
from PySide6.QtCore import QObject
from typing import *

@dataclass
class MediaStation(ABC):
    name: str
    url: str

class BufferMeta(type(QObject), ABCMeta):
    pass

#class MediaPlayer(ABC, QObject):
class MediaPlayer(object, metaclass=BufferMeta):
    @abstractmethod
    def get_current_station(self) -> MediaStation:
        pass
    
    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def toggle(self):
        pass

    @abstractmethod
    def set_media(self, media: MediaStation):
        pass
