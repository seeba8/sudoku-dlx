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

    def set_number_in_constraint(self, r, c, n, i=0):
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
        print("\nr{}c{}#{}: ".format(r, c, n + 1), end="")
        rownum = self.get_row_number(r, c, n)  # - i
        print("rownumber: {}, affected columns: ".format(rownum), end="")
        for i in range(len(self[rownum])):
            if self[rownum][i] == 1:
                fulfilled_constraints.append(i)
                print("{}, ".format(i % 81), end="")
                # for y in range(len(self)):
                #    self[y][i] = -1
        # del self[rownum]
        return fulfilled_constraints

    def get_corresponding_constraints(self, r, c, n):
        yield 0 * 81 + r * 9 + c  # cell constraint
        yield 1 * 81 + r * 9 + n  # row constraint
        yield 2 * 81 + c * 9 + n  # column constraint
        yield 3 * 81 + 27 * (r // 3) + 9 * (c // 3) + n  # block constraint
