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
        # In các tham số thống kê (mean, std, ...) của cột
        col = self.df.get_column(column)
        col.describe()
    
    def list_null_columns(self):
        # In ra các cột rỗng
        self.df.count_na()
    
    def shape(self):
        # In ra kích thước dataframe
        print(self.df.shape())
    
    def count_null_rows(self):
        # Đếm số hàng rỗng
        print('Number of null rows in dataframe:', self.df.count_na_rows())
    
    def list_columns(self):
        # In ra tất cả các cột
        columns = self.df.get_column_labels()
        col_width = max([len(col) for col in columns]) + 2

        for column in columns:
            dtype = self.df.get_column(column).dtype
            print(column.ljust(col_width), '\t', dtype)
        print('Total:', len(columns), 'columns.')
    
    def fillna(self, method, column):
        # Điền các ô rỗng 
        # Nếu không chỉ rõ cột thì điền trên tất cả các cột
        if column is None: 
            for col in self.df._columns:
                col.fill_na(method=method, verbose=self.verbose)
        else: 
            col = self.df.get_column(column)
            col.fill_na(method=method, verbose=self.verbose)
        self.df.write_csv(self.output_filename)
    
    def dropna(self, axis, threshold):
        # Xóa hàng/cột rỗng theo tỉ lệ
        self.df.drop_na(axis=axis, threshold=threshold)
        self.df.write_csv(self.output_filename)
    
    def drop_duplicate(self):
        # Xoá các hàng trùng nhau =
        new_df = self.df.drop_duplicate()
        new_df.write_csv(self.output_filename)

    def normalize(self, method, column):
        # Chuẩn hóa cột
        col = self.df.get_column(column)
        col.normalize(method=method)
        self.df.write_csv(self.output_filename)
    
    def evaluate(self, expression, label):
        # Tính giá trị biểu thức thuộc tính
        expr = hd.SeriesExpression(expression, self.df)
        result = expr.evaluate()
        if label is None:
            label = 'out'
        result.label = label

        new_df = hd.DataFrame()
        new_df.append_column(result)
        new_df.write_csv(self.output_filename)