class Event:
    def __init__(self, type_, payload):
        self.type = type_
        self.payload = payload
    
    def __repr__(self):
        return f"Event(type={self.type!r}, payload={self.payload!r})"
