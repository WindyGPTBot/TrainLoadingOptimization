from Events import Event


class EventQueue():
    """
    Eventqueue, queue of events currently queued up for execution
    """

    def __init__(self):
        self.events = []

    def get_next(self):
        result = self.events.sort(key=lambda e: e.timestamp)[0]
        self.events.remove(0)
        return result