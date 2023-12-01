from observer import Observer

class ServiceLocator():

    _instance = None
    observer = None

    def __init__(self) -> None:
        raise RuntimeError('Call create instead') 

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

