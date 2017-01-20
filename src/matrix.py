class Matrix(list):
    def __init__(self, constraints, puzzle="sudoku9x9", size=9, blocksize=3):
        """
        see: http://www.stolaf.edu/people/hansonr/sudoku/exactcovermatrix.htm
         81+81+81+81=324 columns:
         1) Some number in cell x (only one value)
            r1c1, r1c2, ..., r2c1, r2c2, ..., r9c8, r9c9
         2) Number n must appear in row r
            r1#1, r1#2, ..., r2#1, r2#2, ..., r9#8, r9#9
         3) Number n must appear in column c
            c1#1, c1#2, ..., c2#1, c2#2, ..., c9#8, c9#9
         4) Number n must appear in block b
            b1#1, b1#2, ..., b2#1, b2#2, ..., b9#8, b9#9
            with b1=r1c1-r3c3, b2=r1c4-r3c6, ...

         9*9*9=729 rows:
         Number n at position (x,y): Possibilities to set a number
         (r,c):n -->
         r1c1#1
         r1c2#2
         ...
         r1c2#1
         r1c2#2
         ...
         r9c9#8
         r9c9#9
         """
        self.puzzle = puzzle
        self.size = size
        self.blocksize = blocksize
        list.__init__(self, [x[:] for x in [[0] * (81 * 4)] * 9 ** 3])

        self.names = list()
        nameformats = ["rc{}{}","r{}#{}", "c{}#{}", "b{}#{}"]
        for nameformat in nameformats:
            self.names += [nameformat.format(r, c) for r in range(self.size) for c in range(self.size)]

        for r in range(self.size):
            for c in range(self.size):
                for n in range(self.size):
                    # every row has four 1s, one for row, one for column, one for cell, one for existance
                    y = self.get_row_number(r, c, n)
                    # print(y)
                    for i in self.get_corresponding_constraints(r, c, n):
                        self[y][i] = 1  # block constraint

        for r in range(len(constraints)):
            row = constraints[r]
            for c in range(len(row)):
                if row[c] != 0:
                    rownum = self.get_row_number(r, c, row[c] - 1)
                    self.names.append("Filled-in Sudoku")
                    for y in range(len(self)):
                        self[y].append(1 if y == rownum else 0)

    def get_corresponding_constraints(self, r, c, n):
        yield 0 * self.size * self.size + r * self.size + c  # cell constraint
        yield 1 * self.size * self.size + r * self.size + n  # row constraint
        yield 2 * self.size * self.size + c * 9 + n  # column constraint
        yield 3 * self.size * self.size + self.size * self.blocksize * (r // self.blocksize) + self.size * (
        c // self.blocksize) + n  # block constraint

    def get_row_number(self, r, c, n):
        return self.size * self.size * r + self.size * c + n
