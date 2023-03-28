import unittest
from unittest.mock import Mock, patch
from sample_data_insert import generate_categories

class TestGenerateCategories(unittest.TestCase):

    @patch('sample_data_insert.fake')
    def test_generate_category(self, mock_fake):
        # Set up the mock fake object
        mock_fake.word.return_value = 'John Doe'

        # Generate 3 mock users
        categories = generate_categories(3)

        # Assert that the number of users generated is equal to 3
        self.assertEqual(len(categories), 3)

        # Assert that each user has a PK and SK that start with 'CATEGORY#'
        for category in categories:
            self.assertTrue(category['PK'].startswith('CATEGORY#'))
            self.assertTrue(category['SK'].startswith('CATEGORY#'))

        # Assert that each category has Description and Type field
        for category in categories:
            self.assertIn('Description', category)
            self.assertIn('Type', category)

if __name__ == '__main__':
    unittest.main() 
