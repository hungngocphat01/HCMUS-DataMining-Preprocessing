"""
Honoda v1.0
Simple data cleasing tool
By 19120615 -- Hung Ngoc Phat @ FIT, VNU-HCMUS
"""
import argparse 
from honolib import DataFrame

def main():
    df = DataFrame.from_csv('house-prices.csv')
    df.col_types

if __name__ == '__main__':
    main()