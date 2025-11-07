from typing import TextIO, List, Union, Tuple, Set, Callable
import sys
import itertools

class Cell:
    EMPTY = 0
    COUNT = 0
    MAX_COUNT = 81
    def __init__(self):
        self.value = self.EMPTY # 0 means that value is not set
        self.candidates = set(range(1,10))
        self.my_row = []
        self.my_col = []
        self.my_sq = []
        self.i = 0
        self.j = 0
        Cell.COUNT += 1
        if Cell.COUNT > Cell.MAX_COUNT:
            raise Exception("Too much calls to Cell constructor !!!")
    def __str__(self, empty_char='_'):
        return str(self.value) if self.value != 0 else empty_char
    
    def __repr__(self):
        return self.__str__()

    def is_empty(self):
        return self.value == self.EMPTY

    def is_solved(self):
        return self.value != self.EMPTY

    def str_candidates(self, dlm: str):
        return dlm.join(list(map(str, self.candidates)))

    # should be used only during the load and not durig the solve
    def load_value(self, i:int, j:int, value: int):
        self.i = i
        self.j = j
        if value != self.EMPTY:
            self.candidates = {value}
        print(f'load value {value} into cell {self.dump()}')

    # if there is only one candidate and cell is empty, set the value
    def apply_single(self):
        if self.is_empty() and len(self.candidates) == 1:
            value = list(self.candidates)[0]
            print(f'value {value} applied to cell {self.dump()}')
            self.value = list(self.candidates)[0]
            return True
        else:
            return False

    def remove_candidate(self, value: int):
        if value in self.candidates:
            print(f'value {value} removed as candidate from cell {self.dump()}')
            self.candidates.remove(value)
            return True
        else:
            return False

    def remove_candidates(self, values: Set[int]):
        if values & self.candidates:
            print(f'removing values {values} as candidate from cell {self.dump()}')
            self.candidates.difference_update(values)
            #print(f"- new state: {self.dump()}")
            return True
        else:
            return False

    def remove_candidates_except(self, value: int):
        if value in self.candidates and len(self.candidates) > 1:
            if value not in range(1,10):
                raise Exception(f"Value {value} not acceptible for a Cell !!!")
            self.candidates = { value }
            return True
        else:
            return False

    def dump(self):
        return f"{self.value} ({self.i},{self.j}) {self.candidates}"


class Board:
    def __init__(self):
        self.cells = [Cell() for _ in range(81)]
        self.rows: List[List[Cell]] = []
        for k in range(9):
            row = self.cells[k*9 : k*9 + 9]
            self.rows.append(row)
            for cell in row:
                cell.my_row = row
        self.columns: List[List[Cell]] = []
        for k in range(9):
            col = [self.cells[i] for i in range(k, k+72+1, 9)]
            self.columns.append(col)
            for cell in col:
                cell.my_col = col
        self.squares: List[List[Cell]] = []
        for k in range(0,9):
            r_start = (k // 3) * 3
            c_start = (k % 3) * 3
            ind_start = self.coord2ind(r_start, c_start)
            square = [self.cells[i] for i in range(ind_start, ind_start + 3)]
            square.extend([self.cells[i] for i in range(ind_start + 9, ind_start + 3 + 9)])
            square.extend([self.cells[i] for i in range(ind_start + 18, ind_start + 3 + 18)])
            self.squares.append(square)
            for cell in square:
                cell.my_sq = square

    def coord2ind(self, i: int, j: int):
        return i * 9 + j

    def get_at(self, i, j) -> Cell:
        return self.cells[self.coord2ind(i, j)]

    def get_crs_from_cell(self, cell: Cell) -> Tuple[List[Cell], List[Cell], List[Cell]]:
        c = cell.my_col
        r = cell.my_row
        s = cell.my_sq
        return (c, r, s)

    def print(self):
        for i in range(9):
            r = ''.join([ str(self.cells[self.coord2ind(i, j)]) for j in range(9)])
            print(r)
    
    def dump(self):
        i = 1
        for row in self.rows:
            print(f"row: {i}")
            for cell in row:
                print(cell.dump())
            i += 1
        i = 1
        for col in self.columns:
            print(f"column: {i}")
            for cell in col:
                print(cell.dump())
            i += 1
        i = 1
        for sq in self.squares:
            print(f"square: {i}")
            for cell in sq:
                print(cell.dump())
            i += 1
    
    # find column/row/square singles
    # i.e. find cells which are the only cell that hold a candidate in some acompassing set
    @staticmethod
    def find_set_singles(cell_array: List[Cell]) -> Set[Tuple[Cell,int]]:
        candidadate_values = set()
        singles = set()
        # find union of all candidates in array of cells
        for cell in cell_array:
            if candidadate_values == {1,2,3,4,5,6,7,8,9}:
                # no sense to continue if it already covers all possible values
                break
            if not cell.is_solved():
                candidadate_values.update(cell.candidates)
        # for each such value, find how many it appears across the array of cells
        for value in candidadate_values:
            count = 0
            cell_and_value = None
            for cell in cell_array:
                if cell.is_solved():
                    continue
                if value in cell.candidates:
                    count += 1
                    if count > 1:
                        break
                    cell_and_value = (cell, value)
            if count == 1 and cell_and_value:
                singles.add(cell_and_value)

        return singles

    @staticmethod
    def candidate_union( cell_tuple: Union[ Tuple[Cell], List[Cell], Set[Cell] ] ) -> Set[int]:
        union = set()
        for cell in cell_tuple:
            union |= cell.candidates
        return union

    # find tuples (doubles, triples, ...) of same candidates in the given set
    # e.g. {2,3}, {2,3}; {1,5}, {1,6}, {5,6}; etc...
    # the number of same candidate sets must be the same as their cardinality (number of elements)
    #@staticmethod
    def find_set_tuples(self, cell_array: List[Cell]) -> List[Tuple[Set[Cell], Set[int]]]:
        unsolved = [cell for cell in cell_array if not cell.is_solved()]
        tuples = []
        for tuple_size in range(2,len(unsolved)):
            cell_subsets = list(itertools.combinations(unsolved, tuple_size))
            for cell_subset in cell_subsets:
                union = self.candidate_union(cell_subset)
                if len(union) == len(cell_subset):
                    tuples.append((set(cell_subset), union))
        return tuples

    # find a candidate places in one of the sets, that are also all inside one intersecting set
    # e.g. all 6 in a row are in the same square, or all 3 in a square are in the same column/row
    # row / column combination is not possible, so we always look either sqaure vs row/column, or row/column vs square
    def find_intersecting_candidates(self, origin: List[Cell], origin_type) -> List[Tuple[Set[Cell], int]]:
        unsolved = [cell for cell in origin if not cell.is_solved()]
        union = self.candidate_union(unsolved)
        commons = []
        for cand in union:
            # find cells with this candidate
            cand_cells = [cell for cell in unsolved if cand in cell.candidates]
            if origin_type == 'S':
                columns = [cell.my_col for cell in cand_cells]
                if columns.count(columns[0]) == len(columns):
                    commons.append((columns[0], cand))
                rows = [cell.my_row for cell in cand_cells]
                if rows.count(rows[0]) == len(rows):
                    commons.append((rows[0], cand))
            elif origin_type in ('C', 'R'):
                squares = [cell.my_sq for cell in cand_cells]
                if squares.count(squares[0]) == len(squares):
                    commons.append((squares[0], cand))
        # return all found
        return commons


ListenerFunction = Callable[[Cell, str], None]

class SudokuSolver:
    @staticmethod
    def dummy_listener(c: Cell, s: str):
        pass
        #print(c.dump() if c else 'no_cell', ':', s)

    def __init__(self, f: ListenerFunction = None):
        self.board = Board()
        self.start_percent = 0
        self.f_listener: ListenerFunction = f if f else self.dummy_listener

    def solved_percent(self) -> int:
        empty_count = [c.is_empty() for c in self.board.cells].count(True)
        return 100*(81-empty_count) // 81

    def load(self, _f: TextIO):
        i = 0
        for line in _f:
            if i > 8:
                break
            j = 0
            for x in line.rstrip():
                if j > 8:
                    break
                cell = self.board.get_at(i, j)
                cell.load_value(i, j, int(x))
                self.f_listener(cell, 'load')
                j += 1
            i += 1
        self.start_percent = self.solved_percent()

    ###############################################################
    # implementation of various sudoku techniques
    ###############################################################

    # removing candidates in acompassing sets for a solved cell
    def __clear_candidates(self, _cell: Cell):
        if not _cell.is_solved():
            return False
        self.f_listener(_cell, 'clearing candidates for a solved cell')
        success = False
        value = _cell.value
        reason = f'removing {value} as candidate'
        for crs in self.board.get_crs_from_cell(_cell):
            for cell in crs:
                if not cell.is_solved() and cell != _cell:
                    success0 = cell.remove_candidate(value)
                    if success0:
                        self.f_listener(cell, reason)
                else:
                    success0 = False
                success != success0

        return success

    # cell singles - applying the value to the cell
    # also remove that value from candidates of all cells in acompassing sets
    def __apply_cell_singles(self) -> bool:
        success = False
        for cell in self.board.cells:
            # cell.apply_single will return sucess only if cell has only one candidate
            success0 = cell.apply_single()
            if success0:
                self.f_listener(cell, 'cell solved as cell single')
                self.__clear_candidates(cell)
            success |= success0

        return success

    # row/column/square singles
    def __apply_rcs_singles(self) -> bool:
        success = False
        for board_sets in (self.board.columns, self.board.rows, self.board.squares):
            for a_set in board_sets:
                singles = self.board.find_set_singles(a_set)
                if singles:
                    for (cell, value) in singles:
                        success |= cell.remove_candidates_except(value)
                        success != self.__clear_candidates(cell)

        return success

    def __clean_rcs_tuples(self) -> bool:
        success = False
        for board_sets in (self.board.columns, self.board.rows, self.board.squares):
            for a_set in board_sets:
                tuples = self.board.find_set_tuples(a_set)
                if tuples:
                    for cell_tuple in tuples:
                        #print(cell_tuple[0], cell_tuple[1])
                        to_clean = set(a_set) - cell_tuple[0]
                        for cell in to_clean:
                            if cell.is_solved():
                                continue
                            success0 = cell.remove_candidates(cell_tuple[1])
                            success |= success0
                            if success0:
                                self.f_listener(cell, "candidates removed because of a tuple found")

        return success

    def __clean_intersecting_candidates(self) -> bool:
        print("__clean_intersecting_candidates")
        success = False
        for square in self.board.squares:
            commons_list = self.board.find_intersecting_candidates(square, 'S')
            if commons_list:
                for commons in commons_list:
                    row_or_col = commons[0]
                    for cell in row_or_col:
                        if (not cell.is_solved()) and (cell not in square):
                            success0 = cell.remove_candidate(commons[1])
                            success |= success0
                            if success0:
                                print("candidates removed because of a alligned candidates in a square")
                                self.f_listener(cell, "candidates removed because of a alligned candidates in a square")

        for col in self.board.columns:
            commons_list = self.board.find_intersecting_candidates(col, 'C')
            if commons_list:
                for commons in commons_list:
                    square = commons[0]
                    for cell in square:
                        if (not cell.is_solved()) and (cell not in col):
                            success0 = cell.remove_candidate(commons[1])
                            success |= success0
                            if success0:
                                print("candidates removed because of a squared candidates in a column")
                                self.f_listener(cell, "candidates removed because of a squared candidates in a column")

        for row in self.board.rows:
            commons_list = self.board.find_intersecting_candidates(row, 'R')
            if commons_list:
                for commons in commons_list:
                    square = commons[0]
                    for cell in square:
                        if (not cell.is_solved()) and (cell not in row):
                            success0 = cell.remove_candidate(commons[1])
                            success |= success0
                            if success0:
                                print("candidates removed because of a squared candidates in a row")
                                self.f_listener(cell, "candidates removed because of a squared candidates in a row")

        return success

    ###############################################################
    # TWO GENERIC STEPS OF THE ALGORYTHM: fill & clean
    ###############################################################

    # apply cell & set singles and clear candidates from encompassing sets
    def __fill(self):
        success = self.__apply_cell_singles()
        if success:
            return success
        success = self.__apply_rcs_singles()
        return success

    # remove candidates based on various logic
    def __clean(self):
        success = self.__clean_rcs_tuples()
        if success:
            return True
        success = self.__clean_intersecting_candidates()
        return success

    def solve(self):
        clean_success = True
        fill_success = True
        max_iteration = 300
        curr_iteration = 0
        while clean_success or fill_success:
            curr_iteration += 1
            # find cell singles or set singles and set that number as cell solution
            # this will also clean candidates induced but setting the cell's solution
            fill_success = self.__fill()
            if self.is_solved():
                print('Stopping because it is solved')
                break
            # favour simpler algorithms
            if fill_success:
                continue
            # clean the list of possible values in entire matrix
            clean_success = self.__clean()

            if curr_iteration > max_iteration:
                print('Stopping because max iterations reached')
                break

        self.f_listener(None, f'Percent solved: {self.solved_percent()}%')
    
    def is_solved(self):
        return self.solved_percent() == 100

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = "sudoku.txt"
    try:
        f = open(file_name, "r")
    except FileNotFoundError:
        print(f"file {file_name} not found")
        exit(-1)

    print(f"file {file_name} loaded")
    print("strting the solve")
    print("#################")

    ss = SudokuSolver()

    ss.load(f)

    f.close()

    ss.board.print()
    print(f'Start percentage: {ss.start_percent}%')

    ss.solve()

    print('## FINAL STATE ##')
    ss.board.print()
    #if not ss.is_solved():
    #    ss.board.dump()
