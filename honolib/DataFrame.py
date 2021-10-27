import csv
from os import sep 
import re
import math 
from honolib.Series import Series

class DataFrame:
    def __init__(self):
        self.__columns = []
    
    def count_na(self):
        """
        Hàm in ra số lượng phần tử rỗng trên từng cột và lấy tổng
        """
        
        sum_count = 0
        counter = {col.label: col.count_na() for col in self.__columns}
        
        # Độ rộng lớn nhất của các label (để format cho đẹp)
        max_label_width = max([len(label) for label in counter])

        for label, null_count in counter.items():
            if null_count > 0:
                print(label.ljust(max_label_width), '\t', null_count)
        
        print('\nTotal null values:', sum(counter.values()))
    
    def shape(self):
        """
        Kích thước của dataframe
        """
        if len(self.__columns) == 0:
            return 0,
        return len(self.__columns[0].rows), len(self.__columns)

    def get_row(self, index):
        """
        Lấy ra data của hàng từ index
        """
        row_data = []
        for c in self.__columns:
            row_data.append(c.rows[index])
        return row_data

    def set_row(self, index, obj):
        """
        Gán data của hàng từ index
        """
        shape = self.shape()
        assert len(obj) == shape[1], 'Input array length and dataframe width does not match'
        assert index < shape[1], 'Index out of bound'

        for col_index, col in enumerate(self.__columns):
            col.rows[index] = obj[col_index]
    
    def get_column(self, label) -> Series:
        """
        Lấy ra tham chiếu tới một cột từ tên cột
        """
        for col in self.__columns:
            if col.label == label:
                return col 
        raise AttributeError('Column not found')
    
    def set_column(self, label: str, obj: Series):
        """
        Gán cột
        """
        assert len(obj) == self.shape()[0], 'Length mismatch'

        for col in self.__columns:
            if col.label == label:
                col.rows = obj
                return 
        raise AttributeError('Column not found')
    
    def append_column(self, label: str, obj: Series):
        """
        Chèn thêm cột
        """
        assert type(obj) == Series
        assert len(obj) == self.shape()[0]
        self.__columns.append(obj)

    def delete_row(self, index):
        for col in self.__columns:
            del col.rows[index]
    
    def iterrows(self):
        """
        Iterator để duyệt qua từng hàng 
        Phần tử đầu luôn là index của hàng
        """
        shape = self.shape()
        for r in range(shape[0]):
            row_data = [r] + self.get_row(r)
            yield row_data
        
    def get_column_labels(self):
        """
        Lấy ra danh sách các cột của dataframe
        """
        return [col.label for col in self.__columns]
    
    def count_na_rows(self):
        """
        Hàm đếm số lượng hàng bị thiếu dữ liệu (hàng mà có ít nhất 1 cột bị thiếu)
        """
        count = 0
        for row in self.iterrows():
            for cell in row:
                if cell is None:
                    count += 1 
                    continue
        return count

    def __auto_drop_row(self, threshold):
        pass 

    def __auto_drop_col(self, threshold):
        """
        Private: hàm drop các cột với tỉ lệ null cho trước
        """

        i = 0 
        while i < len(self.__columns):
            col = self.__columns[i]
            # Tính tỉ lệ null
            null_perc = col.count_na() / len(col)
            if null_perc > threshold:
                print('Deleted "', col.label, '"; Null = ', null_perc, '%', sep='')
                del self.__columns[i]
            else: 
                i += 1

    
    def auto_drop(self, axis=0, threshold=0.5):
        """
        Xóa các cột hoặc hàng bị thiếu dữ liệu với ngưỡng cho trước
        n = 
        """
        assert threshold <= 1 and threshold >= 0
        if axis == 0:
            self.__auto_drop_row(self, threshold)
        elif axis == 1: 
            self.__auto_drop_col(self, threshold)
        else: 
            raise AttributeError('Invalid axis. Only accept 0 or 1')
    

    def read_csv(self, filename):
            """
            Hàm đọc CSV từ file
            """
            # columns: dataframe thô dưới dạng transpose
            columns = {}
            with open(filename, 'rt', newline='') as f:
                reader = csv.DictReader(f)
                # Lặp qua từng hàng của CSV
                for row in reader:
                    for key in row:
                        if key not in columns:
                            columns[key] = [row[key]]
                        else:
                            columns[key].append(row[key])
            
            # Từ data thô, construct các series tương ứng
            for col in columns:
                series = Series(columns[col], col)
                self.__columns.append(series)

def read_csv(filename):
    df = DataFrame()
    df.read_csv(filename)
    return df