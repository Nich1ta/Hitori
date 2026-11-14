from boardgame import BoardGame

class Hitori0(BoardGame):
    def __init__(self, file):
        self._list = []
        self._numbers = []
        with open(file, "r") as f:
            self._rows = 0
            for lines in f:
                self._rows += 1
                for el in lines.split(","):
                    self._list.append(el)
                    self._numbers.append(int(el))

        self._w = len(self._list) // self._rows
        self._h = self._rows
        self._annots = [0] * (self._h * self._w)  
        

    def play(self, x, y, action):

        index = x + y * self._w

        if action == "flag":
            
            if self._annots[index] == 0:  
                self._annots[index] = 3  
                self.check_highlight_validity(x, y)
            
            elif self._annots[index] == 3:
                self._annots[index] = 1  # Flag
                self.check_flag_validity(x, y)
            
            elif self._annots[index] == 1:
                self._annots[index] = 0  # Reset to normal
            
            elif self._annots[index] == 2:
                self._annots[index] = 0  # Reset to normal
                self.reset_adjacent_flags(x, y)  
            
            elif self._annots[index] == 4:
                self._annots[index] = 1  # Flag
                self.reset_highlight(x, y)
    def reset_highlight(self, x, y):
        
        # Reset in the same row
        for i in range(self._w):
            if self._annots[i + y * self._w] == 4 and self._numbers[i + y * self._w] == self._numbers[x + y * self._w]:
                self._annots[i + y * self._w] = 3  

        # Reset in the same column
        for i in range(self._h):
            if self._annots[x + i * self._w] == 4 and self._numbers[x + i * self._w] == self._numbers[x + y * self._w]:
                self._annots[x + i * self._w] = 3  


    def check_highlight_validity(self, x, y):
        
        index = x + y * self._w
        valid = True

        # Check for duplicates in the row
        for i in range(self._w):
            if i != x and self._annots[i + y * self._w] == 3 and self._numbers[i + y * self._w] == self._numbers[x + y * self._w]:
                valid = False

        # Check for duplicates in the column
        for i in range(self._h):
            if i != y and self._annots[x + i * self._w] == 3 and self._numbers[x + i * self._w] == self._numbers[x + y * self._w]:
                valid = False

        
        if not valid:
            self._annots[x + y * self._w] = 4
            
            for i in range(self._w):
                if self._numbers[i + y * self._w] == self._numbers[x + y * self._w] and self._annots[i + y * self._w] == 3:
                    self._annots[i + y * self._w] = 4
            for i in range(self._h):
                if self._numbers[x + i * self._w] == self._numbers[x + y * self._w] and self._annots[x + i * self._w] == 3:
                    self._annots[x + i * self._w] = 4

    def reset_adjacent_flags(self, x, y):
        
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self._w and 0 <= ny < self._h:  
                neighbor_index = nx + ny * self._w
                
                if self._annots[neighbor_index] == 2:
                    self._annots[neighbor_index] = 1  

        
    def check_flag_validity(self, x, y):
        
        index = x + y * self._w
        if self._annots[index] == 1:  
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self._w and 0 <= ny < self._h:
                    neighbor_index = nx + ny * self._w
                    if self._annots[neighbor_index] == 1 or self._annots[neighbor_index] == 2:  
                        self._annots[index] = 2  
                        self._annots[neighbor_index] = 2  
    
    

    def read(self, x, y):
        
        index = x + y * self._w
        txt = str(self._numbers[index])
        annot = self._annots[index]

        if annot == 1:  # Flag
            txt += "#"
        elif annot == 2:  # Wrong flag
            txt += "R"
        elif annot == 3:  # Highlight
            txt += "!"
        elif annot == 4:  # Wrong highlight
            txt += "H"
        
        return txt

    def fill(self, x, y):
        """Fill the board with flags, recursively filling connected empty cells."""
        bd, w, h = self._annots, self._w, self._h
        if 0 <= x < w and 0 <= y < h and bd[x + y * w] == 0:
            bd[x + y * w] = 1  # Flag the current cell
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                self.fill(x + dx, y + dy)

    def no_repeats(self):
        
        for y in range(self._h):
            row = [self._numbers[x + y * self._w] for x in range(self._w) if self._annots[x + y * self._w] != 1]
            if len(row) != len(set(row)):
                return False

        for x in range(self._w):
            col = [self._numbers[x + y * self._w] for y in range(self._h) if self._annots[x + y * self._w] != 1]
            if len(col) != len(set(col)):
                return False

        return True

    def no_adjacent_black(self):
       
        for y in range(self._h):
            for x in range(self._w):
                if self._annots[x + y * self._w] == 1:  
                    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self._w and 0 <= ny < self._h:
                            if self._annots[nx + ny * self._w] == 1: 
                                return False
        return True

    def connected_white_cells(self):
        def is_white(i):
            return self._annots[i] in (0, 3)   # unmarked or circled

        visited = [False] * (self._h * self._w)
        start = next((i for i in range(len(self._annots)) if is_white(i)), None)
        if start is None:
            return True

        stack = [start]
        while stack:
            idx = stack.pop()
            if visited[idx]:
                continue
            visited[idx] = True
            x, y = idx % self._w, idx // self._w
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                n_idx = nx + ny * self._w
                if 0 <= nx < self._w and 0 <= ny < self._h and not visited[n_idx]:
                    if is_white(n_idx):
                        stack.append(n_idx)

        return all(visited[i] for i in range(len(self._annots)) if is_white(i))

    def finished(self): 
        
        no_wrong_highlights = all(annot != 4 for annot in self._annots)
        return no_wrong_highlights and self.no_repeats() and self.no_adjacent_black() and self.connected_white_cells()

    def status(self): 
        
        if not self.no_repeats():
            return "Playing!"
        if not self.no_adjacent_black():
            return "Error: Adjacent black cells!"
        if not self.connected_white_cells():
            return "Error: White cells not connected!"
        return "Finished!"

    def cols(self): 
        
        return self._w

    def rows(self): 
        
        return self._h



def load_level(level_name):
    """Load the specific level and return an instance of Hitori0."""
    level_files = {
        "lvl1": "5-easy.csv",
        "lvl2": "6-medium.csv",
        "lvl3": "8-hard.csv",
        "lvl4": "9-veryhard.csv",
        "lvl5": "12-superhard.csv",
        "lvl6": "15-impossible.csv"
    }

    if level_name in level_files:
        return Hitori0(level_files[level_name])  # Load the selected level
    else:
        raise ValueError(f"Unknown level: {level_name}")
