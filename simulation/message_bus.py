class MessageBus:
    def __init__(self):
        self.messages = []

    def send_message(self, sender, receiver, content):
        self.messages.append((sender, receiver, content))

    def get_message_count(self):
        return len(self.messages)
