###################################
# 
# Reflection for Jupyter Notebooks
#
# Charles Varley, 2391564v
#
###################################


from IPython.core.getipython import get_ipython
from IPython.display import display, Javascript


class Cell():
    ''' A class to abstract a Jupyter Notebook cell. '''
    def __init__(self, ctype, content, index='-', prompt='-', auto_execute=False):
        self._ctype   = ctype
        self._content = content
        self._index   = index
        self._prompt  = prompt
        self._auto_execute = auto_execute

    @property 
    def ctype(self):
        return self._ctype

    @ctype.setter
    def ctype(self, t):
        if type(t) is str:
            t_lower = t.lower()
            if t_lower in ["code", "markdown"]:
                self._ctype = t_lower
                if self.auto_execute:
                    self.execute("ctype")
            else: 
                raise ValueError("Invalid cell type value. Values accepted: 'code', 'markdown'")
        else:
            raise TypeError("Ctype requires a string")

    @property 
    def content(self):
        return self._content

    @content.setter
    def content(self, c):
        if type(c) is str:
            self._content = c
            if self.auto_execute:
                self.execute("content")
        else: 
            raise TypeError("Content requires a string")

    @property 
    def index(self):
        return self._index

    @index.setter
    def index(self, i):
        if type(i) is not int:
            raise TypeError(f"Index argument must be an int, got: {type(i)}")
        self._index = i

    @property 
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, p):
        if (type(p) is not int) and (p != '-'):
            raise TypeError(f"Prompt argument must be an int or \'-\', got: {type(p)}")
        self._prompt = p

    @property
    def auto_execute(self):
        return self._auto_execute

    @auto_execute.setter
    def auto_execute(self, b):
        if type(b) is not bool:
            raise TypeError(f"Auto_execute argument must be a boolean, got: {type(b)}")
        elif b:
            self._check_auto_execute()
        self._auto_execute = b


    def __str__(self): 
        return f"Cell object: {{ ctype: {self.ctype}, content: {self.content}, index: {self.index}, prompt: {self.prompt}, auto: {self.auto_execute} }}"

    def _check_auto_execute(self):
         if self.index == "-":
            raise NotImplementedError("Cannot auto_execute a cell that isn't set in the notebook.")

    def execute(self, option="all"):
        # Check cell's auto_execute validity
        self._check_auto_execute()
        # Apply optional changes
        if option == "ctype" or option == "all":
            display(Javascript(f"set_cell_type({self.index}, \"{self.ctype}\", false);"))
        if option == "content" or option == "all":
            display(Javascript(f"set_cell_content({self.index}, \"{self.content}\", false);"))
        display(Javascript(f"Jupyter.notebook.execute_cells([{self.index}]);"))
        # Update cell prompt
        if self.ctype == "markdown":
            self.prompt = '-'
        else:
            self.prompt = get_ipython().execution_count + 1

    def append(self, s):
        self.content += "\n" + s

    
class CellManager():
    ''' 
    A class to store notebook cells as a list of Cell instances, to work around the Shell message block.
    Is updated with notebook's cell state information every time a cell is executed. 
    '''
    def __init__(self):
        self._cells = []

    @property 
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, cells):
        self._cells = cells


    # Update functions, invoked by JS.
    def _update_cells(self, cell_dict):
        for c in cell_dict.keys():
            if int(c)<len(self.cells):
                # Update existing cells
                self.cells.ctype = cell_dict[c]['ctype']
                self.cells.content = cell_dict[c]['content']
                self.cells.index = int(c)
            else:
                # Append new cells
                self.cells.append(Cell(cell_dict[c]['ctype'], cell_dict[c]['content'], index=int(c)))
    
    def _update_cell_prompt(self, i):
        if self.cells[i].ctype == "code":
            self.cells[i].prompt = get_ipython().execution_count - 1


    # Data integrity functions.
    def _check_index(self, i):
        if type(i) is int:
            if i >= len(self.cells):
                raise IndexError(f"Index argument larger than currently stored cell array, got: {i}")
            elif i < 0:
                raise IndexError(f"Index argument is negative, got: {i}")
        elif type(i) is list:
            for j in i:
                self._check_index(j)
        else:
            raise TypeError(f"Index argument is not of type Int or list of Ints, got: {type(i)}")
        
    def _check_cell(self, cell):
        if type(cell) is Cell:
            return 
        elif type(cell) is list:
            for c in cell:
                self._check_cell(c)
        else:   
            raise TypeError(f"Cell argument is not of type Cell or list of Cells, got: {type(cell)}")

    def _update_cell_indices(self):
        for i,c in enumerate(self.cells):
            c.index = i

    def _update_prompts(self, indices):
        i_array = indices if type(indices) is list else [indices]
        ipy_count = get_ipython().execution_count + 1 # +1 to account for initial cell
        for i in i_array:
            if self.cells[i].ctype == "code":
                self.cells[i].prompt = ipy_count
                ipy_count += 1 # only increment counter at code cells
            elif self.cells[i].ctype == 'markdown':
                self.cells[i].prompt = '-'
        

    # Cell manipulation functions.
    def get_cell(self, i):
        self._check_index(i)
        return self.cells[i]

    def get_cells(self, i_list):
        self._check_index(i_list)
        return [self.cells[i] for i in i_list]

    def set_cell(self, cell, i, run):
        self._check_index(i)
        self.cells[i] = cell
        self.cells[i].index = i # Set cell index in case it differs from i
        if run:
            self._update_prompts(i)

    def set_cells(self, cell_list, i_list, run):
        self._check_index(i_list)
        if (type(i_list) is list) and (type(cell_list) is list):
            if len(i_list) == len(cell_list):
                for j in range(len(i_list)):
                    self.cells[i_list[j]] = cell_list[j]
                    self.cells[i_list[j]].index = i_list[j] # Set cell index in case it differs from i[j]
                    if run:
                        self._update_prompts(i_list)
            else:
                raise AttributeError(f"Index and cell lists are not the same length, got: {len(i_list)}, {len(cell_list)}")  
        else:
            raise TypeError(f"Both index and cell arguments are not lists, got: {type(i_list)}, {type(cell_list)}")
        
    def insert_cell(self, cell, i, run):
        self._check_cell(cell)
        if i is not None:
            self._check_index(i)
            self.cells.insert(i, cell)
            # Update indices of cells after cell insertion
            self._update_cell_indices()
        else:
            cell.index = len(self.cells)
            self.cells.append(cell)
        if run:
            self._update_prompts(i)

    def insert_cells(self, cell_list, i_start, run):
        self._check_cell(cell_list)
        if i_start is not None:
            self._check_index(i_start)
            self.cells[i_start:i_start] = cell_list
            # Update indices of cells after cell insertion
            self._update_cell_indices()
        else:
            for c in cell_list:
                c.index = len(self.cells)
                self.cells.append(c)
        if run:
            self._update_prompts([i_start+i for i in range(len(cell_list))])

    def delete_cell(self, i):
        self._check_index(i)
        self._cells.pop(i)
        # Update indices of cells after cell deletion
        self._update_cell_indices()

    def delete_cells(self, i_list):
        self._check_index(i_list)
        self.cells = [c for c in self.cells if c.index not in i_list]
        # Update indices of cells after cell deletion
        self._update_cell_indices()

    def set_cell_type(self, ctype, i, run):
        self._check_index(i)
        if type(i) is list:
            for j in i:
                self.cells[j].ctype = ctype
        else:
            self.cells[i].ctype = ctype
        if run:
            self._update_prompts(i)

    def set_cell_content(self, content, i, run):
        self._check_index(i)
        self.cells[i].content = content 
        if run:
            self._update_prompts(i)

    def append_to_cell(self, content, i):
        self._check_index(i)
        self.cells[i].append(content)


    # Print out all cell data.
    def dump(self):
        for cell in self.cells:
            print(f"Cell {cell.index}:")
            print(f"Execution order: {cell.prompt}")
            print(f"Type: {cell.ctype.capitalize()}")
            print(f"Content: {cell.content}\n")
