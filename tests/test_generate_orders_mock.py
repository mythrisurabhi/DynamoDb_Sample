import random
from copy import deepcopy
from datetime import datetime, timedelta
import unittest
from unittest.mock import patch

from sample_data_insert import generate_orders

class TestGenerateOrders(unittest.TestCase):
    @patch('sample_data_insert.fake')
    def test_generate_orders(self, mocker):
        # Define input values
        no_of_orders = 2
        users = [
            {
                'PK': 'USER#1',
                'SK': 'PROFILE#1',
                'Name': 'John Doe',
                'Email': 'johndoe@example.com',
                'Address': '123 Main St, Anytown USA',
                'Products': []
            },
            {
                'PK': 'USER#2',
                'SK': 'PROFILE#2',
                'Name': 'Jane Smith',
                'Email': 'janesmith@example.com',
                'Address': '456 Oak St, Othertown USA',
                'Products': []
            }
        ]
        products = [
            {
                'Description': 'Product 1'
            },
            {
                'Description': 'Product 2'
            },
            {
                'Description': 'Product 3'
            }
        ]
        order_status = ['Pending', 'Shipped', 'Delivered']
        
        # Mock random.choice to return fixed values
        mocker.patch('generate_orders.random.choice', side_effect=[products[0], order_status[1], 
                                                datetime(2022, 1, 1), products[1], 
                                                order_status[2], datetime(2022, 1, 2)])
        
        # Mock random_date to return fixed values
        mocker.patch('generate_orders.random_date', side_effect=[datetime(2022, 1, 1, 10, 30), 
                                                                datetime(2022, 1, 2, 15, 45)])
        
        # Call the function
        orders, user_products = generate_orders(no_of_orders, users, products)
        print(orders)
        print(user_products)
        # Check the output
        assert len(orders) == 4
        assert len(user_products[0]['Products']) == 2
        assert len(user_products[1]['Products']) == 2
        self.assertTrue(orders[0]['ProductId'].startswith('Product'))
        self.assertTrue(orders[1]['Status'], any(ele in order_status for ele in order_status))
        self.assertTrue(datetime.strptime(orders[2]['GSI1SK'], "%Y-%m-%d"))
        assert orders[3]['PK'] == 'USER#2'

if __name__ == '__main__':
    unittest.main() 