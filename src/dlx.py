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
        return str(self.name)


class Matrix(list):
    def __init__(self, prefill=True):
        # see: http://www.stolaf.edu/people/hansonr/sudoku/exactcovermatrix.htm
        # 81+81+81+81=324 columns:
        # 1) Some number in cell x (only one value)
        #    r1c1, r1c2, ..., r2c1, r2c2, ..., r9c8, r9c9
        # 2) Number n must appear in row r
        #    r1#1, r1#2, ..., r2#1, r2#2, ..., r9#8, r9#9
        # 3) Number n must appear in column c
        #    c1#1, c1#2, ..., c2#1, c2#2, ..., c9#8, c9#9
        # 4) Number n must appear in block b
        #    b1#1, b1#2, ..., b2#1, b2#2, ..., b9#8, b9#9
        #    with b1=r1c1-r3c3, b2=r1c4-r3c6, ...
        #
        # 9*9*9=729 rows:
        # Number n at position (x,y): Possibilities to set a number
        # (r,c):n -->
        # r1c1#1
        # r1c2#2
        # ...
        # r1c2#1
        # r1c2#2
        # ...
        # r9c9#8
        # r9c9#9
        self.names = ["rc{}{}".format(r, c) for r in range(9) for c in range(9)]
        self.names += ["r{}#{}".format(r, c) for r in range(9) for c in range(9)]
        self.names += ["c{}#{}".format(r, c) for r in range(9) for c in range(9)]
        self.names += ["b{}#{}".format(r, c) for r in range(9) for c in range(9)]

        if not prefill:
            list.__init__(self)
            return

        list.__init__(self, [x[:] for x in [[0] * (81 * 4)] * 9 ** 3])
        # list.__init__(self, [[0] * (81 + 81 + 81 + 81)] * (9 * 9 * 9))

        for r in range(9):
            for c in range(9):
                for n in range(9):
                    # every row has four 1s, one for row, one for column, one for cell, one for existance
                    y = self.get_row_number(r, c, n)
                    # print(y)
                    for i in self.get_corresponding_constraints(r, c, n):
                        self[y][i] = 1  # block constraint
                        # print(sum(self[y]))
                        # self.names = [str(i) for i in range(9)] * 9 * 4

                        # input(self.names)
                        # print(self[1])

    def get_row_number(self, r, c, n):
        return 9 * 9 * r + 9 * c + n

    def set_number_in_constraint(self, r, c, n, i = 0):
        """
        We can remove one row per set number, as well as 4 columns (one for each type of constraint, that is,
        one for each 1 in the row
        Remove them or set them to zero. Set to zero causes problems maybe?
        even the number is zero-based (sudoku from 0 to 8)
        :param x:
        :param y:
        :param cell:
        :return:
        """
        fulfilled_constraints = []
        print("\nr{}c{}#{}: ".format(r,c,n+1), end="")
        rownum = self.get_row_number(r, c, n) - i
        print("rownumber: {}, affected columns: ".format(rownum + i), end="")
        for i in range(len(self[rownum])):
            if self[rownum][i] == 1:
                fulfilled_constraints.append(i)
                print("{}, ".format(i%81), end="")
                # for y in range(len(self)):
                #    self[y][i] = -1
        del self[rownum]
        return fulfilled_constraints

    def get_corresponding_constraints(self, r, c, n):
        yield 0 * 81 + r * 9 + c  # cell constraint
        yield 1 * 81 + r * 9 + n  # row constraint
        yield 2 * 81 + c * 9 + n  # column constraint
        yield 3 * 81 + 27 * (r // 3) + 9 * (c // 3) + n  # block constraint


def main(matrix):
    """
    http://lanl.arxiv.org/pdf/cs/0011047
    :param matrix:
    :return:
    """
    m, fulfilled_constraints = get_constraint_matrix(matrix)
    # m = Matrix()
    A = fill_matrix(m)
    # TEST
    h = A[0][-1]
    for x in set(fulfilled_constraints):
        c = A[0][x].chead
        cover_column(c)
        r = c.down
        while r != c:
            r = r.down
    # for row in A:
    #     for cell in row:
    #         print(cell.info())
    search(0)


def get_constraint_matrix(sudoku):
    matrix = Matrix()
    fulfilled_constraints = []
    i = 0
    for r in range(len(sudoku)):
        row = sudoku[r]
        for c in range(len(row)):
            n = row[c]
            if n != 0:
                fulfilled_constraints += matrix.set_number_in_constraint(r, c, n - 1, i)
                i += 1
    # i = 0
    # while i < len(matrix) - 1:
    #     if sum(matrix[i]) == 0:
    #         del matrix[i]
    #     i += 1
    # i = 0
    # while i < len(matrix[0]) - 1:
    #     if sum(matrix[j][i] for j in range(len(matrix))) == 0:
    #         print("del constraint")
    #         for row in matrix:
    #             del row[i]
    #     i += 1
    return (matrix, fulfilled_constraints)


def print_solution():
    print(o)
    sudoku = [x[:] for x in [[-1] * 9] * 9]
    for key, val in o.items():
        r, c, v = 0, 0, 0
        # print(val.chead.name, end="")
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
            # print(r.chead.name, end="")
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
        sudoku[r][c] = v
    print("asd")
    print(sudoku)
    assert(False)

def choose_column():
    s = float("inf")
    j = A[0][-1].right
    c = None
    while j != A[0][-1]:
        if j.size < s:
            c = j
            s = j.size
        j = j.right
    if c == None:
        assert (False)
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
        # print(k)
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
    names = matrix.names
    # matrix = matrix[1:]
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
        if all(x == 0 for x in row):
            print("SUMZERO")
            #continue
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
    # example = [["A", "B", "C", "D", "E", "F", "G"],
    #            [0, 0, 1, 0, 1, 1, 0],
    #            [1, 0, 0, 1, 0, 0, 1],
    #            [0, 1, 1, 0, 0, 1, 0],
    #            [1, 0, 0, 1, 0, 0, 0],
    #            [0, 1, 0, 0, 0, 0, 1],
    #            [0, 0, 0, 1, 1, 0, 1]]
    e = ["500080049",
         "000500030",
         "067300001",
         "150000000",
         "000208000",
         "000000018",
         "700004150",
         "030002000",
         "490050003"]
    example = [[int(r[y]) for y in range(9)] for r in e]
    # print(example)

    A = []
    o = {}
    main(example)
