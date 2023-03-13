import boto3
from faker import Faker
import random
import datetime
from dynamodb_client import create_dynamodb_client



# Define the number of entities to add to the table


num_users = 5000
num_orders = 50000
num_categories = 1000
num_products = 3000
num_reviews = 1000


start_review_id = 1
start_order_id = 100
order_status = ['Shipped', 'In process', 'Hold']

users = []
orders = []
categories = []
products = []
reviews = []

# Define the Faker generator
fake = Faker()
client = create_dynamodb_client

def random_date():
    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date(2023, 3, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return str(random_date)
# Generate users data


def get_users():
    response = client.query(
        TableName='orders-users-products',
        IndexName='GSI2',
        KeyConditionExpression='#Type = :Type',
        ExpressionAttributeNames={
            '#Type': 'Type'
        },
        ExpressionAttributeValues={
            ':Type': {'S': 'USER'}
        })
    #print (len(response.get('Items')))

    for item in response.get('Items'):
        user = {
            'PK': item['PK']['S'],
            'SK': item['SK']['S'],
            'UserName': item['UserName']['S'],
            'Email': item['Email']['S'],
            'Address': item['Address']['S'],
            'CreatedAt': item['CreatedAt']['S'],
            'Type': item['Type']['S']

        }
        users.append(user)


def get_products():
    response = client.query(
        TableName='orders-users-products',
        IndexName='GSI2',
        KeyConditionExpression='#Type = :Type',
        ExpressionAttributeNames={
            '#Type': 'Type'
        },
        ExpressionAttributeValues={
            ':Type': {'S': 'PRODUCT'}
        })
    # print (len(response.get('Items')))

    for item in response.get('Items'):
        product = {
            'PK': item['PK']['S'],
            'SK': item['SK']['S'],
            'Description': item['Description']['S'],
            'Type': item['Type']['S'],

        }
        products.append(product)


def get_categories():
    response = client.query(
        TableName='orders-users-products',
        IndexName='GSI2',
        KeyConditionExpression='#Type = :Type',
        ExpressionAttributeNames={
            '#Type': 'Type'
        },
        ExpressionAttributeValues={
            ':Type': {'S': 'CATEGORY'}
        })

    for item in response.get('Items'):
        category = {
            'PK': item['PK']['S'],
            'SK': item['SK']['S'],
            'Description': item['Description']['S'],
            'Type': item['Type']['S'],

        }
        categories.append(category)


def genarate_users():
    for i in range(num_users):
        user_name = fake.name().replace(' ', '_') + str(random.randint(100, 100000))
        user = {
            'PK': 'USER#' + user_name,
            'SK': 'USER#' + user_name,
            'UserName': user_name,
            'Email': fake.email(),
            'Address': fake.street_address(),
            'CreatedAt': random_date(),
            'Type': 'USER'

        }
        users.append(user)
    insert_items(users)
    print(len(users))

# Define the orders entity


def genarate_orders():
    if len(categories) == 0:
        get_categories()
        if len(categories) == 0:
            genarate_categories()
    if len(products) == 0:
        get_products()
        if len(products) == 0:
            genarate_products()
    if len(users) == 0:
        get_users()
        if len(users) == 0:
            genarate_users()
    for i in range(num_orders):
        user_name = random.choice(users)['UserName']
        order_id = str(start_order_id + i) + random_date()
        status = random.choice(order_status)
        created_at = random_date()
        order = {
            'PK': 'USER#' + user_name,
            'SK': '#ORDER#' + order_id,
            'CreatedAt': created_at,
            'Orderid': order_id,
            'Type': 'ORDER',
            'Status': status,
            'ProductId': random.choice(products)['Description'],
            'GSI1PK': '#ORDER',
            'GSI1SK': created_at
        }
        orders.append(order)
    insert_items(orders)
    print(len(orders))


# Define the categories entity


def genarate_categories():
    for i in range(num_categories):
        category_name = fake.word().upper()+random_date()
        category = {
            'PK': 'CATEGORY#' + category_name,
            'SK': 'CATEGORY#' + category_name,
            'Type': 'CATEGORY',
            'Description': category_name,
        }
        categories.append(category)
    insert_items(categories)


# Define the products entity
def genarate_products():
    if len(categories) == 0:
        get_categories()
        if len(categories) == 0:
            genarate_categories()
    for i in range(num_products):
        product_name = fake.word().upper()+random_date()
        category_name = random.choice(categories)['Description']
        product = {
            'PK': 'CATEGORY#' + category_name,
            'SK': 'PRODUCT#' + product_name,
            'Type': 'PRODUCT',
            'Description': product_name,
        }
        products.append(product)
    insert_items(products)

# Define the reviews entity


def genarate_reviews():
    if len(products) == 0:
        get_products()
        if len(products) == 0:
            genarate_products()
    if len(users) == 0:
        get_users()
        if len(users) == 0:
            genarate_users()
    for i in range(num_reviews):
        user_name = random.choice(users)['UserName']
        product_name = random.choice(products)['Description']
        review_id = start_review_id + i
        review = {
            'PK': 'USER#' + user_name,
            'SK': 'REVIEW#' + str(review_id + i) + random_date(),
            'CreatedAt': random_date(),
            'Type': 'REVIEW',
            'ProductId': product_name,
            'Description': str(random.randint(2, 5)) + 'stars',
            'GSI1PK': 'PRODUCT#' + product_name,
            'GSI1SK': 'REVIEW#' + str(review_id + i)
        }
        reviews.append(review)
    insert_items(reviews)


def insert_items(items):
    dynamodb = boto3.resource("dynamodb", region_name="localhost", endpoint_url="http://localhost:8000/",
                            aws_access_key_id="gi8vsa", aws_secret_access_key="xl2cta")
    table = dynamodb.Table('orders-users-products')
    # Divide items into batches of 25 (the maximum number of items per batch is 25)
    batches = [items[i:i+25] for i in range(0, len(items), 25)]
    with table.batch_writer() as batch:
        for batch_items in batches:
            for item in batch_items:
                try:
                    batch.put_item(Item=item)
                except Exception as e:
                    print(e)
                    print(item)
    
  

# Add the entities to the table
# entities = users + orders + categories + products + reviews
if __name__ == "__main__":
    genarate_users()
    #get_users()
    #print(len(users))
    genarate_categories()
    genarate_products()
    genarate_orders()
    genarate_reviews()
   # get_products()
