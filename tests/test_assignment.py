import pytest
import pathlib
import os
import sys

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to sys.path
sys.path.append(parent_dir)
import load_data

fake_data = """PRICING_EFFECTIVE_DATE,PRICING_END_DATE,SALES_CHANNEL_TYPE,CUSTOMER_TYPE_CODE,ITEM_CATEGORY_NAME,ITEM_SUBCATEGORY_NAME,ITEM_CLASS_NAME,PRODUCT_COUNTRY_ORIGIN_NAME,PRODUCT_SKU_NO,PRODUCT_LONG_NAME,PRODUCT_BASE_UPC_NO,PRODUCT_LITRES_PER_CONTAINER,PRD_CONTAINER_PER_SELL_UNIT,PRODUCT_ALCOHOL_PERCENT,PRODUCT_PRICE,SWEETNESS_CODE
2022-05-01 0:00,9999-12-31 0:00,,,A,,,,,,,0.75,1,14,185,0
2022-05-01 1:00,9999-12-31 0:00,,,B,,,,,,,0.75,1,14,185,0
2022-05-01 2:00,9999-12-31 0:00,,,C,,,,,,,0.75,1,14,185,0
"""

def test_file_downloaded():
    f = 'prices.csv'
    assert pathlib.Path(f).is_file()
    assert pathlib.Path(f).stat().st_size > 0

def exists_function(fun):
    return hasattr(load_data, fun)

def test_exists_process_py():
    assert exists_function('process_py')

def test_process_py_open(mocker):
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=fake_data))
    load_data.process_py()
    mock_open.assert_called_once_with('prices.csv', 'r')

def test_process_py_result(mocker):
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=fake_data))    
    assert load_data.process_py() == 185, "Incorrect Result"

def test_exists_process_csv():    
    assert exists_function('process_csv')

def test_process_csv_called(mocker):    
    mock_csv = mocker.patch('load_data.csv')
    try:
        load_data.process_csv()
    except:
        pass    
    assert len(mock_csv.mock_calls) > 0

def test_process_csv_result(mocker):    
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=fake_data))    
    r = load_data.process_csv()
    assert r == 185, "Incorrect Result"

def test_exists_process_pandas():
    assert exists_function('process_pandas')

def test_process_pandas_called(mocker):
    mock_pandas = mocker.patch('load_data.pandas.read_csv')
    load_data.process_pandas()
    mock_pandas.assert_called_once_with('prices.csv')

def test_process_pandas_result(mocker):
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=fake_data))       
    r = load_data.process_pandas()
    assert r == 185, "Incorrect Result"

def test_exists_process_csv_dict():
    assert exists_function('process_csv_dict')

def test_process_csv_dict(mocker):
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=fake_data))       
    r = load_data.process_csv_dict()
    assert r['A'] == 185

def test_exists_process_pandas_groupby():
    assert exists_function('process_pandas_groupby')

def test_process_pandas_gropuby(mocker):
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=fake_data))       
    df = load_data.process_pandas_groupby()
    assert float(df.loc['A'].iloc[0]) == 185, "Incorrect Result"
