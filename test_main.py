from main import main_func
from collections import namedtuple

"""
python main.py --file products.csv # 1 Случай. Чтение файла без изменений.

python main.py --file products.csv --where "price||>300"# 2 Случай. Фильтрация файла по заданным параметрам. (price > 300)
python main.py --file products.csv --where "rating||<4.5"# 2 Случай. Фильтрация файла по заданным параметрам. (rating < 4.5)

python main.py --file products.csv --where "price||>300" --aggregate "rating=avg" # 3 Случай. Фильтрация И аггрегация данных. (price > 300, rating=avg)
python main.py --file products.csv --where "brand||==samsung" --aggregate "rating=min" # 3 Случай. Фильтрация И аггрегация данных. (brand == samsung,  rating=min)


python main.py --file products.csv --aggregate "price=max" # 4 Случай. Только аггрегация данных по заданным параметрам. (price=max)
python main.py --file products.csv --aggregate "rating=avg" # 4 Случай. Только аггрегация данных по заданным параметрам. (rating=avg)

python main.py --file products.csv --order "price=DESC" # 5 Случай. Только сортировка по заданным параметрам. (price=DESC)
python main.py --file products.csv --order "rating=ASC" # 5 Случай. Только сортировка по заданным параметрам. (rating=ASC)
python main.py --file products.csv --order "name=ASC" # 5 Случай. Только сортировка по заданным параметрам. (name=DESC)
"""

def test_data(mocker): # 1 
    args_data = namedtuple('args', ['file', 'where', 'aggregate', 'order'])

    args = args_data(file="products.csv", where=None, aggregate=None,  order=None)

    mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)

    result = main_func()
    assert len(result) == 10
    
def test_filter_data(mocker): # 2
    args_data = namedtuple('args', ['file', 'where', 'aggregate', 'order'])

    args = args_data(file="products.csv", where='price||>300', aggregate=None,  order=None)

    mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)

    result = main_func()
    assert len(result) == 7

    args_data = namedtuple('args', ['file', 'where', 'aggregate', 'order'])

    args = args_data(file="products.csv", where='rating||<4.5', aggregate=None,  order=None)

    mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)

    result = main_func()
    assert len(result) == 4

def test_filter_aggregate_data(mocker): # 3
    args_data = namedtuple('args', ['file', 'where', 'aggregate', 'order'])

    args = args_data(file="products.csv", where='price||>300', aggregate="rating=avg",  order=None)

    mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)

    result = main_func()
    assert len(result) == 1
    print(result)

    args_data = namedtuple('args', ['file', 'where', 'aggregate', 'order'])

    args = args_data(file="products.csv", where='brand||==samsung', aggregate="rating=min",  order=None)

    mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)

    result = main_func()
    assert len(result) == 1
    print(result)

    args_data = namedtuple('args', ['file', 'where', 'aggregate', 'order'])

    args = args_data(file="products.csv", where='price||<500', aggregate="price=avg",  order=None)

    mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)

    result = main_func()
    assert len(result) == 1
    print(result)

def test_aggregate_data(mocker): # 4
    # Mock argparse to return test arguments
    args_data = namedtuple('args', ['file', 'where', 'aggregate', 'order'])

    args = args_data(file="products.csv", where=None, aggregate="price=max",  order=None)

    mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)

    result = main_func()
    assert len(result) == 1
    print(result)

    args_data = namedtuple('args', ['file', 'where', 'aggregate', 'order'])

    args = args_data(file="products.csv", where=None, aggregate="price=avg",  order=None)

    mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)

    result = main_func()
    assert len(result) == 1
    print(result)



def test_order_data(mocker): # 5
    args_data = namedtuple('args', ['file', 'where', 'aggregate', 'order'])

    args = args_data(file="products.csv", where=None, aggregate=None,  order="price=DESC")

    mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)

    result = main_func()
    assert len(result) == 10


    args_data = namedtuple('args', ['file', 'where', 'aggregate', 'order'])

    args = args_data(file="products.csv", where=None, aggregate=None,  order="rating=ASC")

    mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)

    result = main_func()
    assert len(result) == 10


    args_data = namedtuple('args', ['file', 'where', 'aggregate', 'order'])

    args = args_data(file="products.csv", where=None, aggregate=None,  order="name=ASC")

    mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)

    result = main_func()
    assert len(result) == 10

