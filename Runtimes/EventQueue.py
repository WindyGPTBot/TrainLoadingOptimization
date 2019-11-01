class EventQueue():
    """
    Eventqueue, queue of events currently queued up for execution
    """

    def __init__(self):
        self.events = []

    def get_next(self):
        self.events.sort(key=lambda e: e.timestamp)
        return self.events.pop(0)