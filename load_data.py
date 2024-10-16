#!/usr/bin/python3

import pandas as pd 
import csv

def process_pandas():
    df = pd.read_csv('prices.csv')
    return df['PRODUCT_PRICE'].mean()

def process_csv():
    f = open('prices.csv', 'r')
    reader = csv.DictReader(f)
    total = 0
    count = 0
    for row in reader:
        price = float(row['PRODUCT_PRICE'])
        total += price
        count += 1
    f.close()    
    return total / count

def process_py():
    f = open('prices.csv', 'r')
    header = f.readline().rstrip().split(',')
    rows = 0
    dollars = 0
    for line in f:
        columns = line.split(',')
        price = float(columns[-2])
        dollars += price
        rows += 1
    f.close()
    return dollars / rows

def process_csv_dict():
    df = pd.read_csv('prices.csv')
    products = df['ITEM_CATEGORY_NAME'].unique()
    price_dict = {}
    for p in products:
        pdf = df[df['ITEM_CATEGORY_NAME'] == p]
        price_dict[p] = float(pdf['PRODUCT_PRICE'].mean())
    return price_dict

def process_pandas_groupby():
    df = pd.read_csv('prices.csv')
    prices = df[['ITEM_CATEGORY_NAME', 'PRODUCT_PRICE']]
    return prices.groupby(['ITEM_CATEGORY_NAME']).mean()




if __name__ == "__main__":
    print("Average price using pure python: ", end='')
    print(process_py())
    print("Average price using csv module: ", end='')
    print(process_csv())
    print("Average price using pandas module: ", end='')
    print(process_pandas())
    print(process_csv_dict())
    print(process_pandas_groupby())
    
    