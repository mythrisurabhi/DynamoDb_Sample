import random
import unittest
from unittest.mock import patch
from sample_data_insert import generate_reviews


def first_item(items):
    return items[0]


class TestGenerateReviews(unittest.TestCase):

    @patch('random.choice')
    @patch('random.randint')
    @patch('sample_data_insert.random_date')
    def test_generate_reviews(self, mock_random_date, mock_randint, mock_choice):
        # Set up mock values
        mock_randint.return_value = 3 # Mock random integer to always return 3
        mock_random_date.return_value = '2012-01-01'# Mock random date to always return a fixed date
        mock_choice.side_effect = first_item  # Mock random.choice to always return the first item in the list

        # Set up test data
        user_products = [
            {'PK': 'USER#1', 'Products': [
                {'Description': 'Product1'}, {'Description': 'Product2'}]},
            {'PK': 'USER#2', 'Products': [
                {'Description': 'Product3'}, {'Description': 'Product4'}]}
        ]
        no_of_reviews = 2

        # Call the function being tested
        result = generate_reviews(no_of_reviews, user_products)

        # Check the result
        # expected total of 4 reviews (2 per user)
        self.assertEqual(len(result), 4)
        for review in result:
            self.assertIn('PK', review)
            self.assertIn('SK', review)
            self.assertIn('CreatedAt', review)
            self.assertIn('Type', review)
            self.assertIn('ProductId', review)
            self.assertIn('Description', review)
            self.assertIn('GSI1PK', review)
            self.assertIn('GSI1SK', review)
            self.assertEqual(review['Type'], 'REVIEW')
            self.assertEqual(review['Description'], '3stars')
            self.assertTrue(review['SK'].startswith('REVIEW#'))
            self.assertTrue(review['GSI1PK'].startswith('PRODUCT#'))
            self.assertTrue(review['GSI1SK'].startswith('REVIEW#'))

        
        # Check that each user has the expected number of reviews
        self.assertCountEqual(
            [review['PK'] for review in result],
            ['USER#1', 'USER#1', 'USER#2', 'USER#2']
        )
        self.assertEqual(
            len([review for review in result if review['PK'] == 'USER#1']),
            2  # expected 2 reviews for user1
        )
        self.assertEqual(
            len([review for review in result if review['PK'] == 'USER#2']),
            2  # expected 2 reviews for user2
        )


if __name__ == '__main__':
    unittest.main()
