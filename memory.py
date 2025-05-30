import time
import uuid

class SharedMemory:
    def __init__(self):
        self.memory = []

    def log(self, source, type_, extracted, thread_id=None):
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "source": source,
            "type": type_,
            "extracted": extracted,
            "thread_id": thread_id or str(uuid.uuid4())
        }
        self.memory.append(entry)
        return entry

    def get_all(self):
        return self.memory
