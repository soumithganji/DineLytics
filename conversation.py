from collections import deque


class ConversationBufferWindow:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.buffer = deque(maxlen=window_size)

    def add_message(self, role: str, content: str):
        self.buffer.append((role, content))

    def get_conversation_string(self) -> str:
        return "\n".join([f"{role}: {content}" for role, content in self.buffer])

    def clear(self):
        self.buffer.clear()

    @classmethod
    def from_dict(cls, dictionary: dict) -> "ConversationBufferWindow":
        instance = cls(window_size=dictionary["window_size"])
        instance.buffer = deque(dictionary["buffer"], maxlen=instance.window_size)
        return instance