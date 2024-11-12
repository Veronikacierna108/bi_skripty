import faker
from datetime import datetime, timedelta
import random
import csv

# Initialize Faker
fake = faker.Faker()

# Define table schemas
user_schema = {
    'id': 'text',
    'first_name': 'text',
    'last_name': 'text',
    'email': 'text',
    'phone': 'text',
    'created_at': 'timestamp',
    'updated_at': 'timestamp'
}

order_schema = {
    'id': 'text',
    'user_id': 'text',
    'product': 'text',
    'quantity': 'integer',
    'total_amount': 'float',
    'order_date': 'timestamp',
    'delivery_date': 'timestamp'
}

product_schema = {
    'id': 'text',
    'name': 'text',
    'description': 'text',
    'price': 'float',
    'category': 'text',
    'created_at': 'timestamp',
    'updated_at': 'timestamp'
}

review_schema = {
    'id': 'text',
    'user_id': 'text',
    'product_id': 'text',
    'rating': 'integer',
    'comment': 'text',
    'created_at': 'timestamp'
}

payment_schema = {
    'id': 'text',
    'order_id': 'text',
    'amount': 'float',
    'payment_method': 'text',
    'payment_date': 'timestamp'
}

# Generate data for each table
def generate_users(num_rows):
    users = []
    for _ in range(num_rows):
        user = {
            'id': fake.uuid4(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'created_at': fake.date_time_between(start_date='-2y', end_date='now'),
            'updated_at': fake.date_time_between(start_date='-2y', end_date='now')
        }
        users.append(user)
    return users

def generate_products(num_rows):
    products = []
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports & Outdoors']
    for _ in range(num_rows):
        product = {
            'id': fake.uuid4(),
            'name': fake.company(),
            'description': fake.text(max_nb_chars=200),
            'price': fake.pyfloat(min_value=10.0, max_value=500.0, right_digits=2),
            'category': random.choice(categories),
            'created_at': fake.date_time_between(start_date='-2y', end_date='now'),
            'updated_at': fake.date_time_between(start_date='-2y', end_date='now')
        }
        products.append(product)
    return products

def generate_orders(num_rows, users, products):
    orders = []
    for _ in range(num_rows):
        user = random.choice(users)
        product = random.choice(products)
        order = {
            'id': fake.uuid4(),
            'user_id': user['id'],
            'product': product['name'],
            'quantity': fake.pyint(min_value=1, max_value=10),
            'total_amount': product['price'] * fake.pyint(min_value=1, max_value=10),
            'order_date': fake.date_time_between(start_date='-1y', end_date='now'),
            'delivery_date': fake.date_time_between(start_date='-1y', end_date='now')
        }
        orders.append(order)
    return orders

def generate_reviews(num_rows, users, products):
    reviews = []
    for _ in range(num_rows):
        user = random.choice(users)
        product = random.choice(products)
        review = {
            'id': fake.uuid4(),
            'user_id': user['id'],
            'product_id': product['id'],
            'rating': fake.pyint(min_value=1, max_value=5),
            'comment': fake.text(max_nb_chars=300),
            'created_at': fake.date_time_between(start_date='-1y', end_date='now')
        }
        reviews.append(review)
    return reviews

def generate_payments(num_rows, orders):
    payments = []
    payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer']
    for _ in range(num_rows):
        order = random.choice(orders)
        payment = {
            'id': fake.uuid4(),
            'order_id': order['id'],
            'amount': order['total_amount'],
            'payment_method': random.choice(payment_methods),
            'payment_date': fake.date_time_between(start_date=order['order_date'], end_date='now')
        }
        payments.append(payment)
    return payments

# Generate data for 5 tables with 5000 rows each
user_data = generate_users(5000)
product_data = generate_products(5000)
order_data = generate_orders(5000, user_data, product_data)
review_data = generate_reviews(5000, user_data, product_data)
payment_data = generate_payments(5000, order_data)

# Save data to CSV files
def save_to_csv(file_name, data, schema):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=schema.keys())
        writer.writeheader()
        writer.writerows(data)

save_to_csv('users.csv', user_data, user_schema)
save_to_csv('orders.csv', order_data, order_schema)
save_to_csv('products.csv', product_data, product_schema)
save_to_csv('reviews.csv', review_data, review_schema)
save_to_csv('payments.csv', payment_data, payment_schema)

print("Data saved to CSV files.")