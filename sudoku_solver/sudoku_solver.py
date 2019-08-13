import copy
from typing import List, Dict, Set

# https://leetcode.com/problems/sudoku-solver/

# Use dict / set representation of board to allow
# O(1) time checking of constraints.

ALL_VALS = set(['1','2','3','4','5','6','7','8','9'])

def representRows(board: List[List[str]]) -> Dict:
    """
    Represent rows on board using dict of sets.
    """
    R = {}
    for i in range(9):
        R[i] = set()
        for j in range(9):
            val = board[i][j]
            if val != '.':
                R[i].add(val)
    return R

def neededValues(vals: Dict) -> Dict:
    """
    Get needed values for rows and columns.
    """
    needed = {}
    for i in range(9):
        needed[i] = ALL_VALS - vals[i]
    return needed

def neededValuesSubBoard(vals: Dict) -> Dict:
    """
    Get needed values for sub-board.
    """
    needed = {}
    for i in range(3):
        needed[i] = {}
        for j in range(3):
            needed[i][j] = ALL_VALS - vals[i][j]
    return needed

def representCols(board: List[List[str]]) -> Dict:
    """
    Represent columns on board using dict of sets.
    """
    C = {}
    for j in range(9):
        C[j] = set()
        for i in range(9):
            val = board[i][j]
            if val != '.':
                C[j].add(val)
    return C

def representSubBoards(board: List[List[str]]) -> Dict:
    """
    Represent 3x3 sub-boards using nested dict of sets.
    """
    S = {}
    for i in range(3):
        S[i] = {}
        for j in range(3):
            S[i][j] = set()
            ii = 3 * i
            jj = 3 * j
            for k in range(3):
                for l in range(3):
                    val = board[ii+k][jj+l]
                    if val != '.':
                        S[i][j].add(val)
    return S

def subBoardIndex(k: int) -> List:
    """
    Map row or column index k to a sub-board index 0-2. 
    """
    if k < 3:
        return 0
    elif k < 6:
        return 1
    else:
        return 2

def getEmptyCells(board: List[List[str]]) -> Set:
    """
    Return set of empty cells from board.
    """
    empty = set()
    for i in range(9):
        for j in range(9):
            if board[i][j] == '.':
                empty.add(tuple([i, j]))
    return empty

## TODO: Initialize list of empty cells. Update list when
## number is added. 
## TODO: Member function to make move (add number) on board.
## TODO: Backtracking to find solution. 

class Board:
    """
    Class for Sudoku board.
    """
    def __init__(self, board: List[List[str]], rows: Dict, 
            cols: Dict, sub_boards: Dict, empty: Set, needed_rows: Dict,
            needed_cols: Dict, needed_sub: Dict):
        """
        Constructor.
        """
        self.board = board
        self.rows = rows
        self.cols = cols
        self.sub_boards = sub_boards
        self.empty = empty
        self.empty_list = list(empty)
        self.needed_rows = needed_rows
        self.needed_cols = needed_cols
        self.needed_sub = needed_sub

    @classmethod
    def from_board(cls, board: List[List[str]]):
        """
        Instantiate class from only board values.
        """
        # Represent rows, cols, sub-boards, empty
        rows = representRows(board)
        cols = representCols(board)
        sub_boards = representSubBoards(board)
        empty = getEmptyCells(board)
        needed_rows = neededValues(rows)
        needed_cols = neededValues(cols)
        needed_sub = neededValuesSubBoard(sub_boards)
        return cls(board, rows, cols, sub_boards, empty, needed_rows, needed_cols, needed_sub)

    def validMove(self, i: int, j: int, val: str) -> bool:
        """
        Return True if we can place val at position (i, j), 
        else return False.
        """
        # Row constraint
        if val in self.rows[i]:
            return False
        # Column constraint
        if val in self.cols[j]:
            return False
        # Sub-board constraint
        sub_i = subBoardIndex(i)
        sub_j = subBoardIndex(j)
        if val in self.sub_boards[sub_i][sub_j]:
            return False
        # All constraints satisfied -> return True!
        return True

    @property
    def isFull(self):
        return len(self.empty) == 0

    def makeMove(self, i: int, j: int, val: str):
        """
        Add value val to index (i, j) on board.
        """
        # Update row sets
        rows = copy.deepcopy(self.rows)
        rows[i].add(val)
        # Update column sets
        cols = copy.deepcopy(self.cols)
        cols[j].add(val)
        # Update sub-boards
        sub_i = subBoardIndex(i)
        sub_j = subBoardIndex(j)
        sub_boards = copy.deepcopy(self.sub_boards)
        sub_boards[sub_i][sub_j].add(val)
        # Update empty cells
        empty = self.empty - set([tuple([i, j])])
        # Update board
        board = copy.deepcopy(self.board)
        board[i][j] = val
        # Update needed rows
        needed_rows = copy.deepcopy(self.needed_rows)
        needed_rows[i].remove(val)
        # Update needed columns
        needed_cols = copy.deepcopy(self.needed_cols)
        needed_cols[j].remove(val)
        # Update sub-boards
        needed_sub = copy.deepcopy(self.needed_sub)
        needed_sub[sub_i][sub_j].remove(val)
        # Return new board
        kwargs = {
            'board' : board,
            'rows' : rows,
            'cols' : cols,
            'sub_boards' : sub_boards,
            'empty' : empty,
            'needed_rows' : needed_rows,
            'needed_cols' : needed_cols,
            'needed_sub' : needed_sub,
        }
        return Board(**kwargs)

    def validNumbers(self, i: int, j: int):
        sub_i = subBoardIndex(i)
        sub_j = subBoardIndex(j)
        return self.needed_rows[i] & self.needed_cols[j] & self.needed_sub[sub_i][sub_j]

def findEmpty(board: Board):
    for i in range(9):
        for j in range(9):
            if board.board[i][j] == '.':
                return [i, j]

def solve(board: Board):
    """
    Solve sudoku using backtracking.
    """
    # Finished sudoku board!!
    if board.isFull:
        return board
    # Choose (i, j) to which to add number
    [i, j] = findEmpty(board)
    cand = board.validNumbers(i, j)
    # Consider each possible number to add 
    for val in cand:
        # Move is valid
        if board.validMove(i, j, str(val)):
            # Make move and recursively solve
            board_next = board.makeMove(i, j, str(val))
            board_next = solve(board_next)
            # Valid board return it!
            if board_next is not False:
                return board_next
    # No valid board found - return False
    return False

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        pass 
