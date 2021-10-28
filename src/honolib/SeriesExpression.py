from honolib.DataFrame import DataFrame, Series
from honolib.utils import detect_type_value

class SeriesExpression:
    def __init__(self, string, df: DataFrame):
        # Chuỗi biểu diễn biểu thức trung tố
        self.inf_expr = string
        # Chuỗi biểu diễn ký pháp ba lan ngược (suffix expression)
        self._suf_expr = None
        # Dataframe chứa các cột có trong biểu thức
        self.df = df
        # Phân tích thành suffix expression
        self.parse_tokens()

    @staticmethod
    def _is_operator(c):
        """
        Hàm kiểm tra toán tử
        """
        return c in ('+', '-', '*', '/', '(', ')')
    
    @staticmethod
    def _opr_prcdnce(c):
        """
        Hàm tính mức độ ưu tiên của các toán tử
        """
        if c in ('*', '/'):
            return 2
        elif c in ('+', '-'):
            return 1
        else: 
            return 0
    
    @staticmethod 
    def _cmp_prcdnce(a, b):
        """
        Hàm so sánh mức độ ưu tiên của 2 operator
        """
        pa = SeriesExpression._opr_prcdnce(a)
        pb = SeriesExpression._opr_prcdnce(b)

        if pa > pb:
            return 1
        elif pa < pb:
            return -1 
        else:
            return 0
    
    def __append_operand(self, obj):
        """
        Hàm thêm một object vào biểu thức hậu tố
        """
        # Nếu object có kiểu dữ liệu là số thì push vào biểu thức
        if detect_type_value(obj) in (int, float):
            self._suf_expr.append(float(obj))
        # Ngược lại, xem object đó là một tên cột và lấy ra cột tương ứng, push vào biểu thức
        # Còn nếu cột đó không tồn tại thì hàm get_column sẽ catch
        else:
            column = self.df.get_column(obj)
            self._suf_expr.append(column)

    def parse_tokens(self):
        # Thuật toán đổi infix sang suffix: https://www.geeksforgeeks.org/stack-set-2-infix-to-postfix/
        self._suf_expr = []
        tokens = self.inf_expr.split()
        stack = []

        for token in tokens:
            # If the scanned character is an operand, output it. 
            if not self._is_operator(token):
                self.__append_operand(token)
                        # If the scanned character is an ‘(‘, push it to the stack. 
            elif token == '(':
                stack.append(token)
            # If the scanned character is an ‘)’, pop the stack and output it until a ‘(‘ is encountered, and discard both the parenthesis.
            elif token == ')':
                while len(stack) > 0 and stack[-1] != '(':
                    top = stack.pop()
                    self._suf_expr.append(top)
                stack.pop()
            else: 
                # If the precedence of the scanned operator is greater than the precedence of the operator in the stack(or the stack is empty or the stack contains a ‘(‘ ), push it. 
                # Else, Pop all the operators from the stack which are greater than or equal to in precedence than that of the scanned operator. After doing that Push the scanned operator to the stack. (If you encounter parenthesis while popping then stop there and push the scanned operator in the stack.) 
                while len(stack) > 0 and self._cmp_prcdnce(token, stack[-1]) <= 0:
                    self._suf_expr.append(stack.pop())
                stack.append(token)

        # Pop and output from the stack until it is not empty.
        while len(stack) != 0:
            top = stack.pop()
            self._suf_expr.append(top)            

    def evaluate(self):
        stack = []
        for token in self._suf_expr:
            if not self._is_operator(token):
                stack.append(token)
            else:
                val2 = stack.pop()
                val1 = stack.pop()

                if token == '+':
                    stack.append(val1 + val2)
                elif token == '-':
                    stack.append(val1 - val2)
                elif token == '*':
                    stack.append(val1 * val2)
                elif token == '/':
                    stack.append(val1 / val2)
        return stack.pop()
