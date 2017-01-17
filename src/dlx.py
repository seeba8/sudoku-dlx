class Node:
    left, right, up, down, chead = None, None, None, None, None
    v = None

    def __str__(self):
        return str(self.v)

    def info(self):
        return "{}:{}^, {}v, {}<, {}>, {}h".format(str(self),
                                                   str(self.up),
                                                   str(self.down),
                                                   str(self.left),
                                                   str(self.right),
                                                   str(self.chead))


class Header(Node):
    size, name = 0, ""

    def __init__(self):
        self.chead = self

    def __str__(self):
        return str(self.v)


def main(matrix):
    """
    http://lanl.arxiv.org/pdf/cs/0011047
    :param matrix:
    :return:
    """
    A = fill_matrix(matrix)
    # for row in A:
    #     for cell in row:
    #         print(cell.info())
    search(0)


def print_solution():
    for key, val in o.items():
        print(val.chead.name, end="")
        r = val.right
        while r != val:
            print(r.chead.name, end="")
            r = r.right
        print()


def choose_column():
    s = float("inf")
    j = A[0][-1].right
    c = None
    while j != A[0][-1]:
        if j.size < s:
            c = j
            s = j.size
        j = j.right
    return c.chead


def cover_column(c):
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


def uncover_column(c):
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


def search(k):
    h = A[0][-1]
    if h.right == h:
        print_solution()
        return
    else:
        c = choose_column()
        cover_column(c)
        r = c.down
        while r != c:
            o[k] = r
            j = r.right
            while j != r:
                cover_column(j.chead)
                j = j.right
            search(k + 1)
            r = o[k]
            c = r.chead
            j = r.left
            while j != r:
                uncover_column(j.chead)
                j = j.left
            r = r.down
        uncover_column(c)
        return


def fill_matrix(matrix):
    names = matrix[0]
    matrix = matrix[1:]
    headerrow = []
    left, leftmost = None, None
    h = None
    for i in range(len(matrix[0])):
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
    extra = Header()
    extra.v = "masterheader"
    headerrow.append(extra)
    extra.left = h
    extra.right = leftmost
    leftmost.left = extra
    h.right = extra
    A.append(headerrow)
    up, upmost = headerrow[:], headerrow[:]
    last = headerrow[:]

    for j in range(len(matrix)):
        row = matrix[j]
        left, leftmost = None, None
        A.append([])
        x = A[-1]
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
                x.append(c)
                left = c
                up[i] = c
                last[i] = c
        left.right = leftmost
        leftmost.left = left
    for i in range(len(matrix[0])):
        last[i].down = headerrow[i]
        headerrow[i].up = last[i]
    return A


if __name__ == "__main__":
    example = [["A", "B", "C", "D", "E", "F", "G"],
               [0, 0, 1, 0, 1, 1, 0],
               [1, 0, 0, 1, 0, 0, 1],
               [0, 1, 1, 0, 0, 1, 0],
               [1, 0, 0, 1, 0, 0, 0],
               [0, 1, 0, 0, 0, 0, 1],
               [0, 0, 0, 1, 1, 0, 1]]

    A = []
    o = {}
    main(example)
