import unittest
from unittest.mock import patch
from faker import Faker
from sample_data_insert import generate_products

class TestGenerateProducts(unittest.TestCase):
    
    # Test case 1: Test if the returned list of products is not empty
    def test_generate_products_not_empty(self):
        categories = [{'PK': 'CATEGORY#1'}]
        products = generate_products(5, categories)
        self.assertTrue(len(products) > 0)
    
    # Test case 2: Test if the returned list of products contains the expected number of products
    def test_generate_products_correct_number(self):
        categories = [{'PK': 'CATEGORY#1'}]
        num_products = 5
        products = generate_products(num_products, categories)
        print(products)
        self.assertEqual(len(products), len(categories) * num_products)
    
    # Test case 3: Test if the generated products have the expected attributes
    def test_generate_products_correct_attributes(self):
        categories = [{'PK': 'CATEGORY#1'}]
        products = generate_products(1, categories)
        product = products[0]
        self.assertTrue('PK' in product)
        self.assertTrue('SK' in product)
        self.assertTrue('Type' in product)
        self.assertTrue('Description' in product)
        self.assertEqual(product['PK'], categories[0]['PK'])
        self.assertEqual(product['Type'], 'PRODUCT')
    
    
   

         


       
if __name__ == '__main__':
    unittest.main() 



