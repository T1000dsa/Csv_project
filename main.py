import csv
import argparse 
import re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
#main.py C:\Users\marse\Downloads\customers-1000.csv --filter "Index||<10" 
parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str)
parser.add_argument('--where', type=str, default='Index')
parser.add_argument('--agr', default=None)
parser.add_argument('--order', type=str, default='ASC')
args = parser.parse_args()
file = args.file
column, condition = args.where.split('||') # Index||> 34
_order = False if args.order == 'ASC' else True

condition = re.findall(r'(|<|>|==|<=|>=|!=)(\d+)', condition)

if not all(list(map(lambda x:all(map(lambda y:bool(y), x)), condition))):
    raise KeyError('Err')

with open(file, encoding='utf-8') as csv_file:
    csv_raw_data = list(csv.DictReader(csv_file))
    filtered_data = []

    for item in csv_raw_data:
        if item[column].isdigit():
            for x in condition:
                bool_res = bool(eval(f"{item[column]}{x[0]}{x[1]}"))
                if not bool_res:
                    continue
                filtered_data.append(item)
            continue

        if item[column].isascii():
            for x in condition:
                bool_res = bool(eval(f"{item[column]}{x[0]}{x[1]}"))
                logger.debug(bool_res)
                if not bool_res:
                    continue
                filtered_data.append(item)
            continue

    ordered_data = sorted(filtered_data, key=lambda x:x[column], reverse=_order)
    for i in ordered_data:
        print(i['Index'])
print(condition)