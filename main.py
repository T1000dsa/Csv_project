from tabulate import tabulate
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

def order_helper(result:list[dict], order_by:str, is_reverse:bool, column_add:str = None):
    #logger.debug(order_by)
    if order_by[0]:
        if result[0].get(order_by[0]).replace('.', '').isdigit():
            return sorted([i for i in result if i[order_by[0]].replace('.', '').isdigit()], key=lambda x:float(x[order_by[0]]), reverse=is_reverse)
        else:
            return sorted(result, key=lambda x:x[order_by[0]], reverse=is_reverse)

    else:
        if column_add:
            if result[0].get(column_add).isdigit():
                return sorted(result, key=lambda x:float(x[column_add]), reverse=is_reverse)
            else:
                return sorted(result, key=lambda x:x[column_add], reverse=is_reverse)
        else:
            return result

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

    if args.where:
        condition_f = re.findall(r'(|<|>|==|<=|>=|!=)([\d\.]+|[A-z\s\(\)]+)', condition_f)
        if not all(list(map(lambda x:all(map(lambda y:bool(y), x)), condition_f))):
            raise KeyError('Лишние аргументы')

if args.aggregate:
    column_a, condition_a = args.aggregate.split('=')


if args.order:
    order_by:list = args.order.split('=') # --order "value=ASC"

    if len(order_by) == 2:
        is_reverse = True if order_by[1] == 'DESC' else False

    elif len(order_by) == 1:
        order_by.insert(0, '')
        is_reverse = True if order_by[1] == 'DESC' else False


#logger.debug(f'{args.file}  {args.where}  {args.aggregate}  {args.order}')

def main_func():
    with open(file, encoding='utf-8') as csv_file:
        csv_raw_data = list(csv.DictReader(csv_file))
        filtered_data = []

        if column_f and condition_f: #2 Если есть только аргумент фильтрации
            filter_data_helper(column_f, condition_f, csv_raw_data, filtered_data)

            if args.order:
                filtered_data = order_helper(filtered_data, order_by, is_reverse, column_f)

            if column_a and condition_a: #3 Если есть аргумент фильтрации И аггрегации
                print()
                if filtered_data[0][column_a].replace('.', '').isdigit():
                    result = aggr_data.get(condition_a)([float(i[column_a]) for i in filtered_data if i[column_a].replace('.', '').isdigit()])
                
                elif filtered_data[0][column_a].isascii():
                    result = aggr_data.get(condition_a)([i[column_a] for i in filtered_data])

                return [{f"{column_a} - {condition_a}":result}]
            
            return filtered_data


        elif column_a and condition_a: #4 Если есть только аргумент аггрегации
            if csv_raw_data[0][column_a].replace('.', '').isdigit():
                result = aggr_data.get(condition_a)([float(i[column_a]) for i in csv_raw_data if i[column_a].replace('.', '').isdigit()])
            
            elif csv_raw_data[0][column_a].isascii():
                result = aggr_data.get(condition_a)([i[column_a] for i in csv_raw_data])

            return [{f"{column_a} - {condition_a}":result}]
        
        elif order_by: #5 Если есть только аргумент сортировки
            csv_raw_data = order_helper(csv_raw_data, order_by, is_reverse)
            return csv_raw_data

        
        else: #1 Если нет аргументов
            return csv_raw_data


result = main_func()

print(tabulate(result, headers='keys', tablefmt='grid'))