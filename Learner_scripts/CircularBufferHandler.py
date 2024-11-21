
import logging
from collections import deque

class CircularBufferHandler(logging.Handler):
    def __init__(self, file_name, max_logs=100):
        super().__init__()
        self.file_name = file_name
        self.max_logs = max_logs
        self.buffer = deque(maxlen=max_logs)

    def emit(self, record):
        log_entry = self.format(record)
        self.buffer.append(log_entry)

    def flush_to_file(self):
        with open(self.file_name, 'w') as log_file:
            log_file.write("\n".join(self.buffer))
            log_file.write("\n")
