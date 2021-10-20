import csv 
import re
import math 

class DataFrame:
    def __init__(self):
        self.column_names = []
        self.rows = []
        self.col_types = {}

    def __detect_type_value(self, val):
        """
        Detect type of a variable (from string representation)
        For example: '1.2' -> float, '1' -> int, 'abc' -> str
        """
        if val is None:
            return None
        elif isinstance(val, int):
            return int 
        elif isinstance(val, float):
            return float
        elif isinstance(val, str):
            if re.match('^[-+]?[0-9]+$', val):
                return int
            elif re.match('^[-+]?([0-9]+\.[0-9]*|[0-9]*\.[0-9]+)$', val):
                # 0.5, -0.5, .5, 5. -> float
                return float
            else:
                return str
        else:
            return type(val)

    @staticmethod
    def from_csv(filename):
        df = DataFrame()
        """
        Read dataframe from csv file
        """
        with open(filename, mode='rt', newline='') as f:
            reader = csv.DictReader(f)
            df.column_names = list(reader.fieldnames)
            df.rows = [row for row in reader]
        # Fill empty cells (empty string) with None
        df.__process_empty_cells()
        # Cast cells to its correct type
        df.__process_column_types()
        return df

    def __process_empty_cells(self):
        """
        Assign all empty cell (length = 0) to None
        """
        for attr in self.column_names:
            for row in self.rows:
                if len(row[attr]) == 0:
                    row[attr] = None

    def __process_column_types(self):
        """
        Cast all columns to their correct type.
        If all values in a column have the same type -> the column is associated with that type.
        Otherwise, the column is associated with 'object' type.
        Also cast the values
        """
        for attr in self.column_names:
            for row in self.rows:
                if row[attr] is None:
                    continue
                t: type = self.__detect_type_value(row[attr])
                # If column has not been assigned -> assign the current cell's type to the column
                if attr not in self.col_types:
                    self.col_types[attr] = t
                # If column has 'object' type -> ignore
                elif self.col_types[attr] is object:
                    pass 
                # If column and current cell has different types -> column's type is 'object'
                elif self.col_types[attr] != t:
                    self.col_types[attr] = object
                # Cast current cell to the its correct type
                row[attr] = t(row[attr])

    def to_csv(self, filename):
        """
        Write dataframe to csv file
        """
        with open(filename, mode='wt', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.column_names)
            writer.writeheader()
            # Convert None values back to empty string
            for row in self.rows:
                for attr in self.column_names:
                    if row[attr] is None:
                        row[attr] = ''
                writer.writerow(row)
    
    def get_column(self, attr):
        """
        Get all values of a given column
        """
        return [row[attr] for row in self.rows]

    def assign_column(self, attr, list):
        """
        Assign a given column with an array
        """
        assert len(list) == len(self.rows), 'Series does not have the same row number as table'
        for index, row in enumerate(self.rows):
            if list[index] is None:
                pass
            # Check for type difference
            elif type(list[index]) != self.col_types[attr]:
                self.col_types[attr] = object
            row[attr] = list[index]

    def sum(self, attr):
        """
        Calculate sum of a column
        Returns: sum, n (n is the number of non-null values)
        """
        assert self.col_types[attr] in [float, int], 'Cannot calculate sum value of non-numeric columns'
        s = 0 # accumulate sum
        n = 0 # number of non-None values
        for row in self.rows:
            if row[attr] is not None:
                n += 1
                s += row[attr]
        return s, n

    def mean(self, attr):
        """
        Calculate mean value of a column
        Returns: mean, n (n is the number of non-null values)
        """
        assert self.col_types[attr] in [float, int], 'Cannot calculate mean value of non-numeric columns'
        s, n = self.sum(attr)
        return s / n, n
    
    def var(self, attr):
        """
        Calculate variance value of a column
        Returns: var, n (n is the number of non-null values)
        """
        assert self.col_types[attr] in [float, int], 'Cannot calculate std value of non-numeric columns'
        
        mean, n = self.mean(attr)
        var = 0

        col = self.get_column(attr)
        for cell in col:
            if cell is not None:
                var += (cell - mean) ** 2
        var /= n
        return var, n

    def std(self, attr):
        """
        Calculate variance value of a column
        Returns: std, n (n is the number of non-null values)
        """
        assert self.col_types[attr] in [float, int], 'Cannot calculate var value of non-numeric columns'
        var, n = self.var(attr)
        return math.sqrt(var), n
        

    def count_na(self):
        """
        Count number of None values in each column
        """
        counter = {}
        for attr in self.column_names:
            for row in self.rows:
                if row[attr] is None:
                    if attr in counter:
                        counter[attr] += 1
                    else:
                        counter[attr] = 1
        return counter

    def describe(self):
        describe = {}

def from_csv(filename):
    return DataFrame.from_csv(filename)