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
        self.dtype = None

        if isinstance(obj, list):
            self.__init_from_list(obj)

    def __init_from_list(self, obj):
        self.rows = obj
        self.__process_empty_cells(operation='read')
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


    def __process_empty_cells(self, operation='read'):
        """
        Hàm xử lý các hàng rỗng
        - Nếu đang đọc từ CSV: gán tất cả hàng rỗng thành None
        - Nếu đang ghi xuống CSV: gán tất cả hàng None thành chuỗi rỗng
        """
        assert operation in ('read', 'write'), 'Operation not supported'

        for index, row in enumerate(self.rows):
            if operation == 'read' and len(row) == 0:
                self.rows[index] = None
            elif operation == 'write' and row is None:
                self.rows[index] = ''
    
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
