from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import time

# Підключення до локального сервера MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["online_store"]

#Частина 3
def init_collections():
    users = db["users"]
    products = db["products"]
    orders = db["orders"]

    # Дані для колекції users
    users_data = [
        {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "password": "hashed_password_1",
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "zip": "10001",
                "country": "USA"
            },
            "order_history": []
        },
        {
            "name": "Jane Smith",
            "email": "janesmith@example.com",
            "password": "hashed_password_2",
            "address": {
                "street": "456 Elm St",
                "city": "Los Angeles",
                "zip": "90001",
                "country": "USA"
            },
            "order_history": []
        }
    ]

    # Дані для колекції products
    products_data = [
        {
            "name": "Laptop",
            "category": "Electronics",
            "price": 1200.99,
            "stock": 50,
            "description": "High-performance laptop with 16GB RAM and 512GB SSD.",
            "images": ["laptop1.jpg", "laptop2.jpg"]
        },
        {
            "name": "Smartphone",
            "category": "Electronics",
            "price": 699.99,
            "stock": 150,
            "description": "Latest model with 5G support and 128GB storage.",
            "images": ["smartphone1.jpg", "smartphone2.jpg"]
        },
        {
            "name": "Wireless Mouse",
            "category": "Accessories",
            "price": 29.99,
            "stock": 200,
            "description": "Ergonomic wireless mouse.",
            "images": ["mouse1.jpg"]
        }
    ]

    # Дані для колекції orders
    orders_data = [
        {
            "user_id": None,  # Замінити після вставки users
            "products": [
                {"product_id": None, "quantity": 1, "price": 1200.99},  # Замінити після вставки products
                {"product_id": None, "quantity": 2, "price": 29.99}
            ],
            "total_amount": 1260.97,
            "status": "paid",
            "order_date": datetime.utcnow()
        }
    ]

    # Вставка даних у колекції
    inserted_users = users.insert_many(users_data)
    inserted_products = products.insert_many(products_data)

    # Оновлення orders з реальними user_id та product_id
    orders_data[0]["user_id"] = inserted_users.inserted_ids[0]
    orders_data[0]["products"][0]["product_id"] = inserted_products.inserted_ids[0]
    orders_data[0]["products"][1]["product_id"] = inserted_products.inserted_ids[2]

    # Вставка замовлення
    orders.insert_many(orders_data)

    print("Дані успішно додано!")

#Частина 4
def create_user(name, email, password, address):
    user = {
        "name": name,
        "email": email,
        "password": password,
        "address": address,
        "order_history": []
    }
    result = db.users.insert_one(user)
    print(f"User created with ID: {result.inserted_id}")

def create_product(name, category, price, stock, description, images):
    product = {
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
        "description": description,
        "images": images
    }
    result = db.products.insert_one(product)
    print(f"Product created with ID: {result.inserted_id}")

def create_order(user_id, products, total_amount, status="processing"):
    order = {
        "user_id": ObjectId(user_id),
        "products": [{"product_id": ObjectId(p["product_id"]), "quantity": p["quantity"], "price": p["price"]} for p in products],
        "total_amount": total_amount,
        "status": status,
        "order_date": datetime.utcnow()
    }
    result = db.orders.insert_one(order)
    print(f"Order created with ID: {result.inserted_id}")

# READ
def get_users():
    users = db.users.find()
    for user in users:
        print(user)

def get_products_by_category(category):
    products = db.products.find({"category": category})
    for product in products:
        print(product)

def get_orders_by_user(user_id):
    orders = db.orders.find({"user_id": ObjectId(user_id)})
    for order in orders:
        print(order)

# UPDATE
def update_user_address(user_id, new_address):
    result = db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"address": new_address}})
    print(f"Modified {result.modified_count} user(s)")

def decrement_product_stock(product_id, quantity):
    result = db.products.update_one({"_id": ObjectId(product_id)}, {"$inc": {"stock": -quantity}})
    print(f"Modified {result.modified_count} product(s)")

def update_order_status(order_id, new_status):
    result = db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": new_status}})
    print(f"Modified {result.modified_count} order(s)")

# DELETE
def delete_user(user_id):
    result = db.users.delete_one({"_id": ObjectId(user_id)})
    print(f"Deleted {result.deleted_count} user(s)")

def delete_product(product_id):
    result = db.products.delete_one({"_id": ObjectId(product_id)})
    print(f"Deleted {result.deleted_count} product(s)")

def delete_orders_by_status(status):
    result = db.orders.delete_many({"status": status})
    print(f"Deleted {result.deleted_count} order(s)")

def start_crud_operations():
    # Створення даних
    create_user("Alice Brown", "alicebrown@example.com", "hashed_password_3", {
        "street": "789 Pine St", "city": "San Francisco", "zip": "94103", "country": "USA"
    })
    create_product("Tablet", "Electronics", 499.99, 80, "10-inch tablet with high resolution.", ["tablet1.jpg", "tablet2.jpg"])
    # Отримання даних
    print("\nUsers:")
    get_users()
    print("\nProducts in Electronics:")
    get_products_by_category("Electronics")
    # Створення замовлення
    user_id = db.users.find_one({"name": "Alice Brown"})["_id"]
    product_id = db.products.find_one({"name": "Tablet"})["_id"]
    create_order(str(user_id), [{"product_id": str(product_id), "quantity": 1, "price": 499.99}], 499.99)
    # Оновлення даних
    print("\nUpdating address for Alice Brown...")
    update_user_address(user_id, {
        "street": "123 New St", "city": "Los Angeles", "zip": "90002", "country": "USA"
    })
    print("\nDecrementing stock for Tablet...")
    decrement_product_stock(product_id, 1)
    print("\nUpdating order status...")
    order_id = db.orders.find_one({"user_id": user_id})["_id"]
    update_order_status(order_id, "shipped")
    # Видалення даних
    print("\nDeleting Tablet product...")
    delete_product(product_id)
    print("\nDeleting orders with status 'shipped'...")
    delete_orders_by_status("shipped")

def measure_time(func):
    """Декоратор для вимірювання часу виконання функції"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} виконано за {end - start:.4f} секунд")
        return result
    return wrapper

@measure_time
def create_users(n):
    """Створення n користувачів"""
    for i in range(n):
        user = {
            "name": f"Test User {i}",
            "email": f"test{i}@example.com",
            "password": f"password{i}"
        }
        db["users"].insert_one(user)

@measure_time
def create_products(n):
    """Створення n продуктів"""
    for i in range(n):
        product = {
            "name": f"Test Product {i}", 
            "category": f"Test {i}", 
            "price": 99.99, 
            "stock": 100
        }
        db["products"].insert_one(product)

@measure_time
def read_users():
    """Читання всіх користувачів"""
    list(db["users"].find())

@measure_time
def update_user(n):
    """Оновлення користувача"""
    for i in range(n):
        db["users"].update_one({"email": f"test{i}@example.com"}, {"$set": {"name": f"Updated User{i}"}})

@measure_time
def delete_users():
    """Видалення всіх користувачів"""
    db["users"].delete_many({})

@measure_time
def delete_products():
    """Видалення всіх продуктів"""
    db["products"].delete_many({})

def analisys_execution():
    db["users"].delete_many({})
    db["products"].delete_many({})
    print("Тестування продуктивності MongoDB:")
    create_users(1000)          # Створення 1000 користувачів
    create_products(1000)       # Створення 1000 продуктів
    read_users()                # Читання всіх користувачів
    update_user(1000)           # Оновлення одного користувача
    delete_users()              # Видалення всіх користувачів
    delete_products()           # Видалення всіх продуктів


#Розкоментувати для першого запуску
#init_collections()

#Розкоментувати для CRUD операцій
#start_crud_operations()

#Розкоментувати для аналізу виконання операцій
#analisys_execution()