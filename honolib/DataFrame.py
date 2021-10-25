import csv 
import re
import math 
from honolib.Series import Series

class DataFrame:
    def __init__(self):
        self.columns = []

def read_csv(filename):
        df = DataFrame()
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
            df.columns.append(series)
        return df
