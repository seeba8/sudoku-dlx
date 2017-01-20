from src.header import Header
from src.node import Node


class DLX(list):
    """
    http://lanl.arxiv.org/pdf/cs/0011047
    """

    def __init__(self, constraints):
        self.o = {}
        list.__init__(self)
        names = constraints.names
        headerrow = self.create_header_row(constraints)
        self.append(headerrow)

        self.create_rest_of_matrix(constraints)

    def create_header_row(self, constraints):
        headerrow = []
        names = constraints.names
        left, leftmost = None, None
        h = None
        for i in range(len(constraints[0])):
            h = Header()
            h.name = names[i]
            h.v = (i, -1)
            if left is not None:
                h.left = left
                left.right = h
            if leftmost is None:
                leftmost = h
            left = h
            headerrow.append(h)
        # This is the master header used to check if all constraints are covered (master.right == master)
        # See self.search(k), line 1
        extra = Header()
        extra.v = "masterheader"
        headerrow.append(extra)
        extra.left = h
        extra.right = leftmost
        leftmost.left = extra
        h.right = extra
        return headerrow

    def create_rest_of_matrix(self, constraints):
        headerrow = self[-1]  # there is only the header row inserted, so we can just pick the previous element
        # the following three variables need to be a flat copy of the list,
        # otherwise manipulations would affect all the others
        up, upmost = headerrow[:], headerrow[:]
        last = headerrow[:]

        for j in range(len(constraints)):
            row = constraints[j]
            if all(x == 0 for x in row):
                raise ValueError("Row {} fulfills no constraint".format(j))
            left, leftmost = None, None
            self.append([])
            current_row = self[-1]
            for i in range(len(row)):
                cell = row[i]
                if cell == 1:
                    c = Node()
                    c.chead = headerrow[i]
                    headerrow[i].size += 1
                    c.v = (i, j)
                    if leftmost is None:
                        leftmost = c
                    if left is not None:
                        left.right = c
                        c.left = left
                    up[i].down = c
                    c.up = up[i]
                    current_row.append(c)
                    left = c
                    up[i] = c
                    last[i] = c

            left.right = leftmost
            leftmost.left = left
        # link the last row to the header row
        for i in range(len(constraints[0])):
            last[i].down = headerrow[i]
            headerrow[i].up = last[i]

    def cover_column(self, c):
        c.right.left = c.left
        c.left.right = c.right
        i = c.down
        while i != c:
            j = i.right
            while j != i:
                j.down.up = j.up
                j.up.down = j.down
                j.chead.size -= 1
                j = j.right
            i = i.down

    def uncover_column(self, c):
        i = c.up
        while i != c:
            j = i.left
            while j != i:
                j.chead.size += 1
                j.down.up = j
                j.up.down = j
                j = j.left
            i = i.up
        c.right.left = c
        c.left.right = c

    def search(self, k):
        h = self[0][-1]
        if h.right == h:
            # print(k)
            self.print_solution()
            return
        else:
            c = self.choose_column()
            self.cover_column(c)
            r = c.down
            while r != c:
                self.o[k] = r
                j = r.right
                while j != r:
                    self.cover_column(j.chead)
                    j = j.right
                self.search(k + 1)
                r = self.o[k]
                c = r.chead
                j = r.left
                while j != r:
                    self.uncover_column(j.chead)
                    j = j.left
                r = r.down
            self.uncover_column(c)
            return

    def print_solution(self):
        solution = [x[:] for x in [[-1] * 9] * 9]
        for key, val in self.o.items():
            r, c, v = 0, 0, 0
            if val.chead.name.startswith("rc"):
                r = int(val.chead.name[2])
                c = int(val.chead.name[3])
            elif val.chead.name.startswith("r"):
                r = int(val.chead.name[1])
                v = int(val.chead.name[3]) + 1
            elif val.chead.name.startswith("c"):
                c = int(val.chead.name[1])
                v = int(val.chead.name[3]) + 1
            right = val.right
            while right != val:
                if right.chead.name.startswith("rc"):
                    r = int(right.chead.name[2])
                    c = int(right.chead.name[3])
                elif right.chead.name.startswith("r"):
                    r = int(right.chead.name[1])
                    v = int(right.chead.name[3]) + 1
                elif right.chead.name.startswith("c"):
                    c = int(right.chead.name[1])
                    v = int(right.chead.name[3]) + 1
                right = right.right
            solution[r][c] = v
        print(solution)

    def choose_column(self):
        s = float("inf")
        j = self[0][-1].right
        c = None
        while j != self[0][-1]:
            if j.size < s:
                c = j
                s = j.size
            j = j.right
        if c is None:
            raise ValueError("No constraint available")
        return c.chead
