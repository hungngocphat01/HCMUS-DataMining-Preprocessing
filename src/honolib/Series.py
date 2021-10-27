import math 
from honolib.utils import detect_type_value

class Series:
    """
    Class biểu diễn một cột trong DataFrame 
    """

    def __init__(self, obj, label=''):
        # Các dòng trong series
        self.rows = []
        # Tên cột
        self.label = label
        self.dtype: type = None

        if isinstance(obj, list):
            self.__init_from_list(obj)

    def __init_from_list(self, obj):
        self.rows = obj
        self._process_empty_cells(operation='read')
        self.__process_col_type()

    def __process_col_type(self):
        """
        Hàm để xử lý tự động kiểu dữ liệu của cột
        """
        for index, row in enumerate(self.rows):
            if row is None:
                continue

            t: type = detect_type_value(row)
            # Nếu trong cột có kiểu dữ liệu không đồng nhất -> cột có kiểu object
            if self.dtype is None:
                self.dtype = t
            elif self.dtype != t:
                self.dtype = object

            # Ép kiểu của hàng sang kiểu dữ liệu đúng của nó
            self.rows[index] = t(row)


    def _process_empty_cells(self, operation='read'):
        """
        Hàm xử lý các hàng rỗng
        - Nếu đang đọc từ CSV: gán tất cả hàng rỗng thành None
        - Nếu đang ghi xuống CSV: gán tất cả hàng None thành chuỗi rỗng
        operation = ['read' | 'write']
        """
        assert operation in ('read', 'write'), 'Operation not supported'

        for index, row in enumerate(self.rows):
            if operation == 'read' and len(row) == 0:
                self.rows[index] = None
            elif operation == 'write' and row is None:
                self.rows[index] = ''
    
    def __len__(self):
        return len(self.rows)
    
    def cast(self, dtype: type):
        """
        Hàm để ép kiểu cột sang kiểu dữ liệu tương ứng
        Không ép kiểu được thì gán là None
        """
        for index, row in enumerate(self.rows):
            try:
                self.rows[index] = dtype(row)
            except:
                self.rows[index] = None
        self.dtype = dtype
    
    def count_na(self):
        """
        Đếm số hàng bị thiếu trong cột
        """
        count = 0
        for row in self.rows:
            if row is None: 
                count += 1
        return count

    def count_non_na(self):
        """
        Đếm số hàng không bị thiếu trong cột
        """
        return len(self.rows) - self.count_na()
    
    def sum(self):
        """
        Tính tổng cột
        """
        if self.dtype not in [int, float]:
            return None 
        
        s = 0
        for row in self.rows:
            if row is not None:
                s += row 
        return s 
    
    def mean(self):
        """
        Tính giá trị trung bình của cột
        """
        if self.dtype not in [int, float]:
            return None 

        n = self.count_non_na()
        s = self.sum()
        return s/n
    
    def std(self):
        """
        Tính độ lệch chuẩn của cột
        """
        if self.dtype not in [int, float]:
            return None 

        n = self.count_non_na()
        m = self.mean()
        s = 0
        for row in self.rows:
            if row is None:
                continue
            s += (row - m) ** 2
        return math.sqrt(s / n)
    
    def frequency_table(self):
        """
        Lập bảng tần suất các giá trị phân biệt trong bảng (bao gồm None)
        """
        frequency_table = {}
        for row in self.rows:
            if row in frequency_table:
                frequency_table[row] += 1 
            else: 
                frequency_table[row] = 1
        return frequency_table
    
    def mode(self):
        """
        Tính giá trị mode của cột. Nếu có nhiều mode chỉ lấy giá trị đầu tiên.
        Trả về: mode_value, frequency
        """
        frequency_table = self.frequency_table()
        max_freq = 0
        max_value = 0
        for (value, freq) in frequency_table.items():
            if value is not None:
                if freq > max_freq:
                    max_freq = freq 
                    max_value = value 
        return max_value, max_freq
    
    def minmax(self):
        """
        Hàm tính giá trị min và max của cột
        """
        if self.dtype not in [int, float]:
            return None 

        min_value = +math.inf
        max_value = -math.inf

        for row in self.rows: 
            if row is None:
                continue
            if row < min_value:
                min_value = row 
            if row > max_value: 
                max_value = row 
        return min_value, max_value
    
    def median(self):
        """
        Hàm tính giá trị trung vị của cột
        """
        if self.dtype not in [int, float]:
            return None 

        n = len(self.rows)
        m = math.floor((n + 1) / 2)

        filtered_rows = list(filter(lambda x: x is not None, self.rows))
        sorted_rows = sorted(filtered_rows)

        return sorted_rows[m]
    
    def describe(self):
        """
        Hàm in ra thông tin mô tả của cột
        """
        rnd = lambda x: round(x, 4) if x is not None else None

        print('Type:            ', self.dtype)
        print('Length:          ', len(self.rows))
        print('Null values:     ', self.count_na())
        print('Label:           ', self.label)
        print('Sum:             ', rnd(self.sum()))
        print('Mean:            ', rnd(self.mean()))
        print('Median:          ', rnd(self.median()))
        print('Std:             ', rnd(self.std()))
        print('Min-Max:         ', self.minmax())
        print('Mode:            ', self.mode())
    
    def fill_na(self, method='mean'):
        """
        Điền giá trị rỗng cho cột
        method = ['mean' | 'med' | 'mode']
        Nếu cột không có giá trị gì (cả cột đều rỗng) thì điền giá trị 0 cho cột.
        """
        assert method in ['mean', 'median', 'mode'], 'Unsupported fill method' 
        
        if self.dtype not in [int, float]:
            print('Forcing method "mode" for categorical column')
            method = 'mode'

        if method == 'mean':
            fill_value = self.mean()
        elif method == 'median':
            fill_value = self.median()
        elif method == 'mode':
            fill_value, freq = self.mode()
        
        for i, row in enumerate(self.rows):
            if row is None:
                if self.dtype is not None:
                    # Đôi khi cột là int nhưng mean là float nên ta cần ép kiểu lại cho đúng
                    self.rows[i] = self.dtype(fill_value)
                else: 
                    self.rows[i] = 0

        if self.dtype is None:
            self.dtype = 0
    
    def normalize(self, method='zscore'):
        """
        Chuẩn hóa cột
        method = ['zscore' | 'zscore']
        """
        assert method in ['zscore', 'minmax'], 'Invalid normalize method'
        
        if method == 'zscore':
            mean = self.mean()
            std = self.std()
        elif method == 'minmax':
            min_value, max_value = self.minmax()


        for i, row in enumerate(self.rows):
            if row is None:
                continue
            if method == 'zscore':
                self.rows[i] = (row - mean) / std
            elif method == 'minmax':
                self.rows[i] = (row - min_value) / (max_value - min_value)
        
        # Sau khi chuẩn hóa, dữ liệu chắc chắn trở thành số thập phân
        self.dtype = float
