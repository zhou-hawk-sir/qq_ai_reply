from collections import deque

class ChatMemory:
    def __init__(self, max_turns=6):
        self.max_turns = max_turns
        self.buffer = deque(maxlen=max_turns * 2)

    def add_user(self, text):
        self.buffer.append({"role": "user", "content": text})

    def add_ai(self, text):
        self.buffer.append({"role": "assistant", "content": text})

    def messages(self):
        return list(self.buffer)

    def clear(self):
        self.buffer.clear()
