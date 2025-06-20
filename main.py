import csv
import argparse 
import re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

aggr_data = {
    'avg':lambda x:sum(x)/len(x),
    'max':max,
    'min':min
}

def bool_check(column:str, cond:tuple[str], item:dict):
    try:
        if cond[1].isdigit():
            bool_res = bool(eval(f"{item[column]}{cond[0]}{cond[1]}"))
            #logger.debug(bool_res)

        elif cond[1].isascii():
            bool_res = bool(eval(f"'{item[column]}'{cond[0]}'{cond[1]}'"))
            #logger.debug(f"{item[column]}{cond[0]}{cond[1]}")

        if not bool_res:
            return False
    except Exception as err:
        #logger.error(err)
        return False
    return True


def case_helper(column:str, condition:list, item:dict):
    for x in condition:
        res = bool_check(column, x, item)
        if res:
            return item

def filter_data_helper(column:str, condition:list, csv_raw_data:list[dict], filtered_data:list):
    for item in csv_raw_data:
        res = case_helper(column, condition, item)
        if res:
            filtered_data.append(res)

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str)
parser.add_argument('--where', default=None)
parser.add_argument('--aggregate', default=None)
parser.add_argument('--order', type=str, default='ASC')
args = parser.parse_args()

column_f, condition_f = None, None
column_a, condition_a = None, None

file = args.file

if args.where:
    column_f, condition_f = args.where.split('||')

if args.aggregate:
    column_a, condition_a = args.aggregate.split('=')


if args.where:
    condition_f = re.findall(r'(|<|>|==|<=|>=|!=)(\d+|[A-z\s\(\)]+)', condition_f)
    if not all(list(map(lambda x:all(map(lambda y:bool(y), x)), condition_f))):
        raise KeyError('Err')
    
_order = False if args.order == 'ASC' else True

def main_func():
    with open(file, encoding='utf-8') as csv_file:
        csv_raw_data = list(csv.DictReader(csv_file))
        filtered_data = []

        if column_f and condition_f:
            filter_data_helper(column_f, condition_f, csv_raw_data, filtered_data)

            if csv_raw_data[0][column_f].isdigit():
                logger.debug(f'{column_f}')
                ordered_data = sorted(filtered_data, key=lambda x:int(x[column_f]), reverse=_order)

            elif csv_raw_data[0][column_f].isascii():
                logger.debug(f'{column_f}')
                ordered_data = sorted(filtered_data, key=lambda x:x[column_f], reverse=_order)

        if column_a and condition_a:
            if filtered_data[0][column_a].isdigit():
                result = aggr_data.get(condition_a)([int(i[column_a]) for i in filtered_data])
                print(result)
            
            elif filtered_data[0][column_a].isascii():
                result = aggr_data.get(condition_a)([i[column_a] for i in filtered_data])

            return result

        return ordered_data

result = main_func()
print(result)

"""

    else:
        if args.where:
            ordered_data = sorted(csv_raw_data, key=lambda x:x[column_f], reverse=_order)
        else:
            ordered_data = csv_raw_data"""