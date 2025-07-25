#Python-скрипт для фильтрации, аггрегации и сортировки данных csv-файлов.#

cd Csv_project # При необходимости
pip install -r requirements.txt # Устанавливаем зависимости
pytest -s -v # Запускаем тесты

# Примеры запуска скрипта: 

python main.py --file products.csv # 1 Случай. Чтение файла без изменений.

python main.py --file products.csv --where "price||>300"# 2 Случай. Фильтрация файла по заданным параметрам. (price > 300)
python main.py --file products.csv --where "rating||<4.5"# 2 Случай. Фильтрация файла по заданным параметрам. (rating < 4.5)

python main.py --file products.csv --where "price||>300" --aggregate "rating=avg" # 3 Случай. Фильтрация И аггрегация данных. (price > 300, rating=avg)
python main.py --file products.csv --where "brand||==samsung" --aggregate "rating=min" # 3 Случай. Фильтрация И аггрегация данных. (brand == samsung,  rating=min)
python main.py --file products.csv --where "price||<500" --aggregate "price=avg" # 3 Случай. Фильтрация И аггрегация данных. (price < 500,  price=avg)

python main.py --file products.csv --aggregate "price=max" # 4 Случай. Только аггрегация данных по заданным параметрам. (price=max)
python main.py --file products.csv --aggregate "rating=avg" # 4 Случай. Только аггрегация данных по заданным параметрам. (rating=avg)

python main.py --file products.csv --order "price=DESC" # 5 Случай. Только сортировка по заданным параметрам. (price=DESC)
python main.py --file products.csv --order "rating=ASC" # 5 Случай. Только сортировка по заданным параметрам. (rating=ASC)
python main.py --file products.csv --order "name=ASC" # 5 Случай. Только сортировка по заданным параметрам. (name=DESC)