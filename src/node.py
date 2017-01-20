class Node:
    left, right, up, down, chead = None, None, None, None, None
    v = None

    def __str__(self):
        return "{}:{}^, {}v, {}<, {}>, {}h".format(str(self.v),
                                                   str(self.up),
                                                   str(self.down),
                                                   str(self.left),
                                                   str(self.right),
                                                   str(self.chead))
