from src.node import Node
from src.header import Header
from src.matrix import Matrix


def main(matrix):
    """
    http://lanl.arxiv.org/pdf/cs/0011047
    :param matrix:
    :return:
    """
    # m, fulfilled_constraints = get_constraint_matrix(matrix)
    m = Matrix()
    for r in range(len(matrix)):
        row = matrix[r]
        for c in range(len(row)):
            if row[c] != 0:
                rownum = m.get_row_number(r, c, row[c] - 1)
                m.names.append("Filled-in Sudoku")
                for y in range(len(m)):
                    m[y].append(1 if y == rownum else 0)
    A = fill_matrix(m)
    # TEST

    # for x in set(fulfilled_constraints):
    #     c = A[0][x].chead
    #     cover_column(c)
    #     print("Get the correct row that fulfills that constraint and cover these columns")
    # # for row in A:
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
    print(sudoku)


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
            raise ValueError("Row {} fulfills no constraint".format(j))
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
