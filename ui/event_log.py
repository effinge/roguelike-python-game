class EventLog:
    def __init__(self, limit=3):
        self.limit = limit
        self.messages = []

    def add(self, message):
        self.messages.append(message)
        self.messages = self.messages[-self.limit:]

    def get_messages(self):
        return self.messages
