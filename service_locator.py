from observer import Observer
from soundManager import SoundManager

class ServiceLocator():

    _instance = None
    observer = None
    sound_manager = None

    def __init__(self) -> None:
        raise RuntimeError('Call create instead') 

    def get_sound_manager(self):
        """
            Creates singleton for sound manager
        """
        if self.sound_manager is None:
            self.sound_manager = SoundManager()
        return self.sound_manager

    def get_observer(self) -> Observer:
        """
            Creates singleton for observer
        """
        if self.observer is None:
            self.observer = Observer()
        return self.observer

    @classmethod
    def create(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

