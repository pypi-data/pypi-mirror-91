import uuid


class Handler:
    def __init__(self, callback):
        self.callback = callback
        self.uuid = str(uuid.uuid4())

    def to_js(self):
        return f"hotairHandle(this, {self.uuid!r})"
