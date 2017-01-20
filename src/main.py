from src.dlx import DLX
from src.matrix import Matrix


def main(sudoku):
    """
    http://lanl.arxiv.org/pdf/cs/0011047
    :param sudoku:
    :return:
    """
    # m = Matrix("sudoku", 9, 3, sudoku)
    m = Matrix(sudoku)

    dlx = DLX(m)
    dlx.search(0)

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
    main(example)
