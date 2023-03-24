import random
from copy import deepcopy
from datetime import datetime, timedelta
import unittest
from unittest.mock import patch

from sample_data_insert import generate_orders
users = [
    {
        'PK': 'USER#1',
        'SK': 'PROFILE#1',
        'Name': 'John Doe',
        'Email': 'johndoe@example.com',
        'Address': '123 Main St, Anytown USA'
    },
    {
        'PK': 'USER#2',
        'SK': 'PROFILE#2',
        'Name': 'Jane Smith',
        'Email': 'janesmith@example.com',
        'Address': '456 Oak St, Othertown USA'
    }
]
products = [
    {
        'Description': 'Product 10'
    },
    {
        'Description': 'Product 2'
    },
    {
        'Description': 'Product 3'
    }
]
order_status = ['Pending1', 'Shipped1', 'Delivered1']


def first_item(items):
    return items[0]


class TestGenerateOrders(unittest.TestCase):
    @patch('random.randint')
    @patch('sample_data_insert.random_date')
    @patch('random.choice')
    def test_generate_orders(self, mock_choice, mock_random_date, mock_randint):
        # Set up mock values
        mock_randint.return_value = 3  # Mock random integer to always return 3
        # Mock random date to always return a fixed date
        mock_random_date.return_value = '2012-01-01'
        mock_choice.side_effect = first_item

        no_of_orders = 2
        # Call the function
        orders, user_products = generate_orders(no_of_orders, users, products)
        # Check the output
        assert len(orders) == 4
        assert len(user_products[0]['Products']) == 2
        assert len(user_products[1]['Products']) == 2
        self.assertTrue(orders[0]['ProductId'].startswith('Product'))
        self.assertTrue(orders[1]['Status'], any(
            ele in order_status for ele in order_status))
        self.assertTrue(datetime.strptime(orders[2]['GSI1SK'], "%Y-%m-%d"))
        assert orders[3]['PK'] == 'USER#2'


if __name__ == '__main__':
    unittest.main()
