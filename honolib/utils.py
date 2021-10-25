"""
Module cho các hàm tiện ích
"""
import re 

def detect_type_value(val):
        """
        Hàm "đoán" kiểu dữ liệu của một biến từ biểu diễn dạng chuỗi
        Vd: '0.5' -> float, '2' -> int, '2.' -> float, ...
        """
        if val is None:
            return None
        elif isinstance(val, str):
            if re.match('^[-+]?[0-9]+$', val):
                # 1, 2, -2 -> int
                return int
            elif re.match('^[-+]?([0-9]+\.[0-9]*|[0-9]*\.[0-9]+)$', val):
                # 0.5, -0.5, .5, 5. -> float
                return float
            else:
                return str
        else:
            return type(val)
