"""
Module chứa các hàm để xử lý từng chức năng cho chương trình
"""
import honolib as hd

class Controller:
    def __init__(self, input_filename, output_filename, verbose):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.verbose = verbose
        self.df: hd.DataFrame = hd.read_csv(self.input_filename)

        if verbose:
            print('File read into memory.')
    
    def describe(self, column):
        col = self.df.get_column(column)
        col.describe()
    
    def list_null_columns(self):
        self.df.count_na()
    
    def shape(self):
        print(self.df.shape())
    
    def count_null_rows(self):
        print('Number of null rows in dataframe:', self.df.count_na_rows())
    
    def list_columns(self):
        columns = self.df.get_column_labels()
        col_width = max([len(col) for col in columns]) + 2

        for column in columns:
            dtype = self.df.get_column(column).dtype
            print(column.ljust(col_width), '\t', dtype)
    
    def fillna(self, method, column):
        if column is None: 
            for col in self.df._columns:
                col.fill_na(method=method)
        else: 
            col = self.df.get_column(column)
            col.fill_na(method=method)
        self.df.write_csv(self.output_filename)
    
    def dropna(self, axis, threshold):
        self.df.drop_na(axis=axis, threshold=threshold)
        self.df.write_csv(self.output_filename)
    
    def drop_duplicate(self):
        new_df = self.df.drop_duplicate()
        new_df.write_csv(self.output_filename)

    def normalize(self, method, column):
        col = self.df.get_column(column)
        col.normalize(method=method)
        self.df.write_csv(self.output_filename)
    
    def evaluate(self, expression):
        ...