class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class EventManager(metaclass=Singleton):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_name, callback):
        """Subscribe a callback function to an event."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)

    def unsubscribe(self, event_name, callback):
        """Unsubscribe a callback function from an event."""
        if event_name in self._subscribers:
            self._subscribers[event_name].remove(callback)

    def trigger(self, event_name, *args, **kwargs):
        """Trigger all callbacks associated with an event."""
        if event_name in self._subscribers:
            for callback in self._subscribers[event_name]:
                callback(*args, **kwargs)
