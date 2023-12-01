from typing import Dict, Tuple, List
from signals import Signal

class Observer:
    
    listeners: Dict[Signal, list] = dict()
    unsubscribe_buffer: List[Tuple[Signal, object]] = list()

    def subscribe(self, signal, listener):
        """ Subscribe a listener to a signal """
        self.listeners.setdefault(signal, list()).append(listener)

    def unsubscribe(self, signal, listener):
        """ Unsubscribe a listener from a signal """
        self.unsubscribe_buffer.append((signal, listener))

    def notify(self, signal: Signal, **kwargs):
        """ Notify all listeners of a signal """

        for listener in self.listeners.get(signal, list()):
            signal.execute(listener, **kwargs)

        # Remove any listeners that have been unsubscribed
        for signal, listener in self.unsubscribe_buffer:
            self.listeners.get(signal, list()).remove(listener)
        self.unsubscribe_buffer.clear()
