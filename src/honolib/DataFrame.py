import csv
import re
import math 
import copy
from honolib.Series import Series

class DataFrame:
    def __init__(self):
        self._columns = []
    
    def count_na(self):
        """
        Hàm in ra số lượng phần tử rỗng trên từng cột và lấy tổng
        """
        
        sum_count = 0
        counter = {col.label: col.count_na() for col in self._columns}
        
        # Độ rộng lớn nhất của các label (để format cho đẹp)
        max_label_width = max([len(label) for label in counter])

        for label, null_count in counter.items():
            if null_count > 0:
                print(label.ljust(max_label_width), '\t', null_count)
        
        print('\nTotal null values:', sum(counter.values()))
    
    def shape(self) -> tuple:
        """
        Trả về kích thước (hàng, cột) của dataframe
        """
        if len(self._columns) == 0:
            return 0, 0
        return len(self._columns[0].rows), len(self._columns)

    def get_row(self, index: int) -> list:
        """
        Trả về data của hàng từ `index`
        """
        row_data = []
        for c in self._columns:
            row_data.append(c[index])
        return row_data

    def set_row(self, index: int, obj):
        """
        Gán data của hàng tại vị trí `index` bằng mảng `obj`. Mỗi phần tử của `obj` ứng với mỗi cột của hàng.
        """
        shape = self.shape()
        assert len(obj) == shape[1], 'Input array length and dataframe width does not match'
        assert index < shape[1], 'Index out of bound'

        for col_index, col in enumerate(self._columns):
            col[index] = obj[col_index]
    
    def append_row(self, obj):
        """
        Chèn một hàng vào bảng. Mỗi phần tử của `obj` ứng với mỗi cột của hàng.
        """
        shape = self.shape()
        assert len(obj) == shape[1], 'Input array length and dataframe width does not match'

        for index, col in enumerate(self._columns):
            col.rows.append(obj[index])
        
    def get_column(self, label) -> Series:
        """
        Lấy ra tham chiếu tới một cột từ tên cột `label`.
        """
        for col in self._columns:
            if col.label == label:
                return col 
        raise AttributeError('Column not found: ' + label)
    
    def set_column(self, label: str, obj: Series):
        """
        Gán cột có tên `label` bằng một object `Series` khác.
        """
        assert len(obj) == self.shape()[0], 'Length mismatch'

        for col in self._columns:
            if col.label == label:
                col.rows = obj
                return 
        raise AttributeError('Column not found')
    
    def append_column(self, obj: Series):
        """
        Chèn thêm một cột vào bảng.
        """
        n_rows, n_col = self.shape()
        assert type(obj) == Series
        assert n_rows == 0 or len(obj) == n_rows
        self._columns.append(obj)

    def delete_row(self, index):
        """
        Hàm xóa hàng tại vị trí `index` khỏi bảng.
        """
        for col in self._columns:
            del col[index]
    
    def iterrows(self) -> list:
        """
        Iterator để duyệt qua từng hàng.
        Trả về một mảng các cột của hàng. Phần tử đầu luôn là index của hàng.
        """
        shape = self.shape()
        for r in range(shape[0]):
            row_data = [r] + self.get_row(r)
            yield row_data
        
    def get_column_labels(self) -> list:
        """
        Trả về danh sách các tên cột của dataframe
        """
        return [col.label for col in self._columns]
    
    def count_na_rows(self) -> int:
        """
        Trả về số lượng hàng bị thiếu dữ liệu (hàng mà có ít nhất 1 cột bị thiếu).
        """
        count = 0
        for row in self.iterrows():
            for cell in row:
                if cell is None:
                    count += 1 
                    break
        return count

    def __auto_drop_row(self, threshold):
        """
        Private: hàm drop các hàng với tỉ lệ null cho trước
        """
        n_rows, n_cols = self.shape()
        idx = 0

        while idx < n_rows:
            row = self.get_row(idx)
            # Đếm số lượng cột null
            count_null = 0
            for col in row:
                if col is None: 
                    count_null += 1
            null_perc = count_null / n_cols

            # Drop hàng nếu tỉ lệ >= threshold
            if null_perc >= threshold:
                self.delete_row(idx)
                n_rows -= 1
            else: 
                idx += 1

    def __auto_drop_col(self, threshold):
        """
        Private: hàm drop các cột với tỉ lệ null cho trước
        """
        idx = 0 
        while idx < len(self._columns):
            col = self._columns[idx]
            # Tính tỉ lệ null
            null_perc = col.count_na() / len(col)
            if null_perc >= threshold:
                print('Deleted "', col.label, '"; Null = ', null_perc * 100, '%', sep='')
                del self._columns[idx]
            else: 
                idx += 1
    
    def drop_na(self, axis=0, threshold=0.5):
        """
        Xóa các cột hoặc hàng bị thiếu dữ liệu với ngưỡng cho trước.
        - `axis`: nếu là 0 thì xóa hàng, nếu là 1 thì xóa cột.
        - `threshold`: tỉ lệ null của một cột/hàng để bị xóa.
        """
        assert threshold <= 1 and threshold >= 0
        if axis == 0:
            self.__auto_drop_row(threshold)
        elif axis == 1: 
            self.__auto_drop_col(threshold)
        else: 
            raise AttributeError('Invalid axis. Only accept 0 or 1')
    
    def drop_duplicate(self):
        """
        Hàm xóa các hàng trùng lặp
        Trả về: DataFrame chứa các hàng không trùng
        """
        # Lặp qua tất cả các hàng và xây dựng danh sách các hàng không trùng lặp
        duplicate_count = 0
        unique_rows = [] 
        for row in self.iterrows():
            # Drop cột chứa index và chuyển thành tuple (immutable thì dùng toán tử in mới chính xác)
            row = tuple(row[1:])
            if row not in unique_rows:
                unique_rows.append(row)
            else:
                duplicate_count += 1
        
        # Dựng lại dataframe mới 
        df = DataFrame()
        for col in self._columns:
            series = Series(None, label=col.label)
            df._columns.append(series)
        for row in unique_rows:
            df.append_row(row)
        
        return df

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
                self._columns.append(series)

    def write_csv(self, filename):
        """
        Hàm xuất dataframe ra CSV
        """
        df = copy.deepcopy(self)
        for column in df._columns:
            column._process_empty_cells(operation='write')

        with open(filename, 'wt', newline='') as f:
            column_labels = df.get_column_labels()
            writer = csv.DictWriter(f, fieldnames=column_labels)
            writer.writeheader()
            for row in df.iterrows():
                # Bỏ cột index
                row = row[1:]
                writer.writerow({cell[0]: cell[1] for cell in zip(column_labels, row)})

def read_csv(filename):
    df = DataFrame()
    df.read_csv(filename)
    return df