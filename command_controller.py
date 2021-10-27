"""
Module chứa các hàm để xử lý từng chức năng cho chương trình
"""
import honolib as hd

class Controller:
    def __init__(self, input_filename, output_filename, verbose):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.verbose = verbose
        self.df = hd.read_csv(self.input_filename)

        if verbose:
            print('File read into memory.')
    
    def describe(self, column):
        col = self.df.get_column(column)
        col.describe()
    
    def list_null_columns(self):
        self.df.count_na()
    
    def count_null_rows(self):
        print('Number of null rows in dataframe:', self.df.count_na_rows())
    
    def list_columns(self):
        columns = self.df.get_column_labels()
        col_width = max([len(col) for col in columns]) + 2

        for column in columns:
            dtype = self.df.get_column(column).dtype
            print(column.ljust(col_width), '\t', dtype)
    
    def fillna(self, method, column):
        print('Fillna', method, column)
    
    def dropna(self, axis, threshold):
        print('Drop na', axis, threshold)
    
    def unique_filter(self):
        print('Unique filter')

    def normalize(self, method, column):
        print('Normalize', method, column)
    
    def evaluate(self, expression):
        ...