from src.node import Node


class Header(Node):
    size, name = 0, ""

    def __init__(self):
        self.chead = self

    def __str__(self):
        return str(self.name)
