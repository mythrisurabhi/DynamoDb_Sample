from faker import Faker
import random
import datetime
from copy import deepcopy
from resource_1 import create_dynamodb_resource


# Define the Faker generator
fake = Faker()
start_review_id = 1
start_order_id = 100
order_status = ['Shipped', 'In process', 'Hold']


def random_date():
    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date(2023, 3, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date.strftime('%Y-%m-%d')

# Generate users


def generate_users(no_of_users: int):
    users = []
    for i in range(no_of_users):
        user_name = fake.name().replace(' ', '_') + str(random.randint(100, 100000))
        user_item = {
            'PK': 'USER#' + user_name,
            'SK': 'USER#' + user_name,
            'UserName': user_name,
            'Email': fake.email(),
            'Address': fake.street_address(),
            'CreatedAt': random_date(),
            'Type': 'USER'

        }
        users.append(user_item)
    return users


# Generate oders for each user
def generate_orders(no_of_orders: int, users: list, products: list):
    orders = []
    user_products = []
    for user in users:
        user_deep_copy = deepcopy(user)
        products_list = []
        for i in range(no_of_orders):
            order_id = str(start_order_id + i)
            status = random.choice(order_status)
            created_at = random_date()
            if len(products) > 0:
                product = random.choice(products)
            else:
                product = {'Description': fake.word().upper() + random_date()}
            products_list.append(product)
            order_item = {
                'PK': user['PK'],
                'SK': '#ORDER#' + order_id,
                'CreatedAt': created_at,
                'Orderid': order_id,
                'Type': 'ORDER',
                'Status': status,
                'ProductId': product['Description'],
                'GSI1PK': '#ORDER',
                'GSI1SK': created_at
            }
            orders.append(order_item)
        user_product = user_deep_copy
        user_product['Products'] = products_list
        user_products.append(user_product)
    return orders, user_products


# Generate reviews for each user
def generate_reviews(no_of_reviews: int, user_products):
    reviews = []
    for user in user_products:
        for i in range(no_of_reviews):
            product = random.choice(user['Products'])
            review_id = start_review_id + i
            review_item = {
                'PK': user['PK'],
                'SK': 'REVIEW#' + str(review_id + i) + random_date(),
                'CreatedAt': random_date(),
                'Type': 'REVIEW',
                'ProductId': product['Description'],
                'Description': str(random.randint(2, 5)) + 'stars',
                'GSI1PK': 'PRODUCT#' + product['Description'],
                'GSI1SK': 'REVIEW#' + str(review_id + i)
            }
            reviews.append(review_item)
    return reviews


def generate_categories(no_of_categories: int):
    categories = []
    for i in range(no_of_categories):
        category_name = fake.word().upper() + str(random.randint(100, 100000))
        category_item = {
            'PK': 'CATEGORY#' + category_name,
            'SK': 'CATEGORY#' + category_name,
            'Type': 'CATEGORY',
            'Description': category_name,
        }
        categories.append(category_item)
    return categories


def generate_products(no_of_products: int, categories):
    products = []
    for category in categories:
        for i in range(no_of_products):
            product_name = fake.word().upper() + random_date()
            product_item = {
                'PK': category['PK'],
                'SK': 'PRODUCT#' + product_name,
                'Type': 'PRODUCT',
                'Description': product_name,
            }
            products.append(product_item)
    return products

# Batch write items


def insert_items(data):

    dynamodb = create_dynamodb_resource()
    table = dynamodb.Table('orders-users-products')
    batch_size = 25
    batch = []
    for item in data:
        batch.append(item)
        if len(batch) == batch_size:
            with table.batch_writer() as batch_writer:
                for item in batch:
                    batch_writer.put_item(Item=item)
            batch = []
    if batch:
        with table.batch_writer() as batch_writer:
            for item in batch:
                batch_writer.put_item(Item=item)


# Add the entities to the table
if __name__ == "__main__":
    # Input function to get number of users
    num_users = int(input("Enter number of users to generate: "))
    num_orders = int(input("Enter number of orders per user: "))
    num_reviews = int(input("Enter number of reviews per user: "))
    num_categories = int(input("Enter number of categories to generate: "))
    num_products = int(input("Enter number of products per category: "))

    users = generate_users(no_of_users=num_users)
    categories = generate_categories(no_of_categories=num_categories)
    products = generate_products(
        no_of_products=num_products, categories=categories)
    orders, user_products = generate_orders(no_of_orders=num_orders,
                                            users=users, products=products)
    reviews = generate_reviews(
        no_of_reviews=num_reviews, user_products=user_products)
    # entities = users + orders + categories + products + reviews
    data = users + orders + categories + products + reviews
    insert_items(data=data)
