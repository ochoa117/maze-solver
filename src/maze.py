from cell import Cell
import random
import time

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        if seed:
            random.seed(seed)
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0,0)
        self.__reset_cells_visited()
    
    def __create_cells(self):
        for i in range(self.__num_cols):
            col_cells = []
            for j in range(self.__num_rows):
                col_cells.append(Cell(self.__win))
            self.__cells.append(col_cells)
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)
    
    def __draw_cell(self, i, j):
        x1 = self.__cell_size_x * i + self.__x1
        x2 = self.__cell_size_x + x1
        y1 = self.__cell_size_y * j + self.__y1
        y2 = self.__cell_size_y + y1
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()
    
    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.05)
    
    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)
    
    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            will_visit = []
            # determine which cell(s) to visit next
            # right
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                will_visit.append((i + 1, j))
            # left
            if i > 0 and not self.__cells[i - 1][j].visited:
                will_visit.append((i - 1, j))
            # down
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                will_visit.append((i, j + 1))
            # up
            if j > 0 and not self.__cells[i][j - 1].visited:
                will_visit.append((i, j - 1))
            # break out if there is nowhere to go
            if len(will_visit) == 0:
                self.__draw_cell(i, j)
                return
            # randomly choose which direction to go
            next_visit = will_visit[random.randrange(len(will_visit))]

            # knock out walls between this cell and next cell
            #right
            if next_visit[0] == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[i + 1][j].has_left_wall = False
            # left
            if next_visit[0] == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[i - 1][j].has_right_wall = False
            # down
            if next_visit[1] == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[i][j + 1].has_top_wall = False
            # up
            if next_visit[1] == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[i][j - 1].has_bottom_wall = False
            
            # recursively visit next cell
            self.__break_walls_r(next_visit[0], next_visit[1])
    
    def __reset_cells_visited(self):
        for i in range(0, self.__num_cols):
            for j in range(0, self.__num_rows):
                if self.__cells[i][j].visited:
                    self.__cells[i][j].visited = False
    
    def solve(self, i=0, j=0):
        return self.__solve_r(i, j)
    
    def __solve_r(self, i, j):
        self.__animate()
        self.__cells[i][j].visited = True
        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True
        # move up
        if j - 1 >= 0 and not self.__cells[i][j].has_top_wall and not self.__cells[i][j - 1].visited:
            self.__cells[i][j].draw_move(self.__cells[i][j - 1])
            if self.__solve_r(i, j - 1):
                return True
            else:
                self.__cells[i][j - 1].draw_move(self.__cells[i][j], True)
        # move down
        if j + 1 < self.__num_rows and not self.__cells[i][j].has_bottom_wall and not self.__cells[i][j + 1].visited:
            self.__cells[i][j].draw_move(self.__cells[i][j + 1])
            if self.__solve_r(i, j + 1):
                return True
            else:
                self.__cells[i][j + 1].draw_move(self.__cells[i][j], True)
        # move left
        if i - 1 >= 0 and not self.__cells[i][j].has_left_wall and not self.__cells[i - 1][j].visited:
            self.__cells[i][j].draw_move(self.__cells[i - 1][j])
            if self.__solve_r(i - 1, j):
                return True
            else:
                self.__cells[i - 1][j].draw_move(self.__cells[i][j], True)
        # move right
        if i + 1 >= 0 and not self.__cells[i][j].has_right_wall and not self.__cells[i + 1][j].visited:
            self.__cells[i][j].draw_move(self.__cells[i + 1][j])
            if self.__solve_r(i + 1, j):
                return True
            else:
                self.__cells[i + 1][j].draw_move(self.__cells[i][j], True)
        return False