"""custom exceptions."""


class Missing(Exception):
    def __init__(self, msg):
        self.msg = msg


class Duplicate(Exception):
    def __init__(self, msg):
        self.msg = msg
