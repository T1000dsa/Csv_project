import csv
import argparse 
import re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

def bool_check(column:str, cond:tuple, item:dict):
    try:
        bool_res = bool(eval(f"{item[column]}{cond[0]}{cond[1]}"))
        if not bool_res:
            return False
    except:
        return False
    return True


def case_helper(column:str, condition:list, item:dict):
    for x in condition:
        res = bool_check(column, x, item)
        if res:
            return item

def filter_data_helper(column:str, condition:list, csv_raw_data:list[dict], filtered_data:list):
    for item in csv_raw_data:
        if item[column].isdigit():
            res = case_helper(column, condition, item)
            if res:
                filtered_data.append(res)

        elif item[column].isascii():
            res = case_helper(column, condition, item)
            if res:
                filtered_data.append(res)

        
parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str)
parser.add_argument('--where', default=None)
parser.add_argument('--agr', default=None)
parser.add_argument('--order', type=str, default='ASC')
args = parser.parse_args()

column, condition = None, None
file = args.file

if args.where:
    column, condition = args.where.split('||')

if args.where:
    condition = re.findall(r'(|<|>|==|<=|>=|!=)(\d+)', condition)
    if not all(list(map(lambda x:all(map(lambda y:bool(y), x)), condition))):
        raise KeyError('Err')
    
_order = False if args.order == 'ASC' else True


with open(file, encoding='utf-8') as csv_file:
    csv_raw_data = list(csv.DictReader(csv_file))
    filtered_data = []

    if column and condition:
        filter_data_helper(column, condition, csv_raw_data, filtered_data)

        if csv_raw_data[0][column].isdigit():
            logger.debug(f'{column}')
            #logger.debug(f'{filtered_data}')
            ordered_data = sorted(filtered_data, key=lambda x:int(x[column]), reverse=_order)

        elif csv_raw_data[0][column].isascii():
            ordered_data = sorted(filtered_data, key=lambda x:x[column], reverse=_order)
    else:
        if args.where:
            ordered_data = sorted(csv_raw_data, reverse=_order)
        else:
            ordered_data = csv_raw_data


    for i in ordered_data:
        print(i)