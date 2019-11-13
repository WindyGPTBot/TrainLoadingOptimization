from Events.Event import Event


class EventQueue:
    """
    EventQueue, queue of events currently queued up for execution
    """

    def __init__(self):
        self.events = []

    def get_next(self) -> Event:
        self.events.sort(key=lambda e: e.timestamp)
        return self.events.pop(0)
