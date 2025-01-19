import sqlite3
import info

def initiate_db():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    ''')

    connection.commit()
    connection.close()


def insert_product(title, description, price):
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    # Проверяем, существует ли продукт с таким же id
    cursor.execute('SELECT * FROM Products WHERE title = ?', (title,))
    existing_product = cursor.fetchone()

    if existing_product is None:
        cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                       (title, description, price))
        connection.commit()
    else:
        pass

    connection.close()

def populate_db():
    insert_product(info.name_D3, info.description_D3, info.price_D3)
    insert_product(info.name_O3, info.description_O3, info.price_O3)
    insert_product(info.name_kid, info.description_kid, info.price_kid)
    insert_product(info.name_Mg, info.description_Mg, info.price_Mg)

def get_all_products():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    # Сделаем выборку всех записей при помощи fetchall():
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.close()
    for prod in products:
        id, title, description, price = prod
        print(f'ID: {id} | Название продукта: {title} | Описание: {description} | Цена: {price}')

    return products

# Запустить инициализацию базы данных
initiate_db()
# Заполнить базу данных данными из info
populate_db()
# Получить все продукты и вывести на экран
get_all_products()
