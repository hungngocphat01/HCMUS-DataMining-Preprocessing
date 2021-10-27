"""
Honoda v1.0
Simple data cleasing tool
By 19120615 -- Hung Ngoc Phat @ FIT, VNU-HCMUS
"""
import argparse 
import traceback
from command_controller import Controller

def main():
    parser = argparse.ArgumentParser(description='Honoka\'s Data Preprocessing Toolbox')
    subparsers = parser.add_subparsers(help='Honoda subcommands', dest='command')

    # Nhóm các lệnh để xuất thông tin cơ bản của dữ liệu (số hàng/cột, tên các cột, số hàng/cột bị null)
    stats_parser = subparsers.add_parser('stats', help='Display data statistics')
    stats_exclusive = stats_parser.add_mutually_exclusive_group()
    stats_exclusive.add_argument('--shape', 
        action='store_true', 
        help='Print dataframe\'s shape'
    )

    stats_exclusive.add_argument('-ls', '--list-columns',
        dest='list_columns', 
        action='store_true', 
        help='List all columns and their detected datatype'
    )
    stats_exclusive.add_argument('-d', '--describe', 
        metavar='COLUMN', 
        help='Display statistical info (min, max, mean, mode, ...) of a column'
    )
    stats_exclusive.add_argument('-cnr', '--count-null-rows', 
        dest='count_null_rows', 
        action='store_true', 
        help='Count all rows with at least one null value, and display the total null-ed rows'
    )
    stats_exclusive.add_argument('-lnc', '--list-null-columns', 
        dest='list_null_columns', 
        action='store_true', 
        help='List all columns with at least one null value, and their total null counts'
    )

    # Lệnh để điền giá trị thiếu 
    fillna_parser = subparsers.add_parser('fillna', help='Fill null values')
    fillna_parser.add_argument('-m', '--method', 
        help='Method to fill for numeric columns (median, mean, mode are allowed). Categorical columns are always filled with their mode value', 
        metavar='METHOD', 
        type=str,
        choices=['median', 'mean', 'mode'],
        required=True
    )

    fillna_parser.add_argument('-c', '--column', 
        help='Specify the column to work on. Only this column will be processed if this argument is specified (default: process all columns)',
        metavar='COL', 
        type=str
    )

    # Lệnh xóa các dòng/cột bị thiếu dữ liệu 
    dropna_parser = subparsers.add_parser('dropna', help='Drop column or row with null values')
    dropna_parser.add_argument('-a', '--axis', 
        metavar='AXIS', 
        type=int,
        help='Axis to search for null values (0: row, 1: column)', 
        choices=[0, 1], 
        required=True
    )
    dropna_parser.add_argument('-t', '--threshold', 
        metavar='THRESHOLD', 
        type=float, 
        help='Threshold (percentage) of null values in axis to drop (from 0 to 1)', 
        default=0.5
    )

    # Lệnh xóa các mẫu trùng lặp 
    uniquefilter_parser = subparsers.add_parser('dropdup', help='Only keep unique rows from the dataframe')

    # Lệnh chuẩn hóa cột 
    normalize_parser = subparsers.add_parser('normalize', help='Normalize a column')
    normalize_parser.add_argument('-m', '--method', 
        metavar='METHOD', 
        type=str, 
        choices=['minmax', 'zscore'], 
        help='Method to normalize (minmax, zscore are allowed)'
    )
    normalize_parser.add_argument('-c', '--column', 
        help='Specify the column to work on.',
        metavar='COL', 
        type=str, 
        required=True
    )

    # Tính giá trị của biểu thức 
    evaluate_parser = subparsers.add_parser('evaluate', help='Evaluate a columnar expression')
    evaluate_parser.add_argument('expression', type=str, help='Expression to evaluate. Tokens MUST be seperated by spaces. Ex: Col1 * Col2 + Col3')
    evaluate_parser.add_argument('-c', '--column', 
        help='Specify the output column name',
        metavar='COL', 
        type=str, 
        required=True
    )

    parser.add_argument('input', metavar='INPUT', type=str, help='Input filename')
    parser.add_argument('-o', '--out', default=None, metavar='OUTPUT', type=str, help='Output filename')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase verbosity')

    args = parser.parse_args()
    ctrl = Controller(args.input, args.out, args.verbose)

    try:
        if args.command == 'stats':
            if args.describe:
                ctrl.describe(args.describe)
            elif args.shape:
                ctrl.shape()
            elif args.list_null_columns:
                # Yêu cầu 1: Đếm các dòng bị thiếu dữ liệu
                ctrl.list_null_columns()
            elif args.count_null_rows:
                # Yêu cầu 2: Liệt kê các cột bị thiếu dữ liệu
                ctrl.count_null_rows()
            elif args.list_columns:
                ctrl.list_columns()
            else: 
                print('Invalid action or action not specified')
            
        elif args.command == 'fillna':
            # Yêu cầu 3: Điền giá trị bị thiếu
            ctrl.fillna(args.method, args.column)
        elif args.command == 'dropna':
            # Yêu cầu 4, 5: Xóa các dòng/cột bị thiếu với ngưỡng cho trước
            ctrl.dropna(args.axis, args.threshold)
        elif args.command == 'dropdup':
            # Yêu cầu 6: Xóa các mẫu trùng lặp
            ctrl.drop_duplicate()
        elif args.command == 'normalize':
            # Yêu cầu 7: Chuẩn hóa một thuộc tính
            ctrl.normalize(args.method, args.column)
        elif args.command == 'evaluate':
            # Yêu cầu 8: Tính giá trị biểu thức 
            ctrl.evaluate(args.expression)
        else: 
            print('Unknown command:', args.command)
    except KeyboardInterrupt:
        print('Good bye!')
    except Exception as e:
        print('An error occurred while running the program. Run with -v flag for more information:\n', e)
        if args.verbose:
            print('\n', traceback.format_exc())


if __name__ == '__main__':
    main()