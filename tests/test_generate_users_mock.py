import unittest
from unittest.mock import patch
from sample_data_insert import generate_users




class TestGenerateUsers(unittest.TestCase):

    @patch('sample_data_insert.fake')
    def test_generate_users(self, mock_fake):
        # Set up the mock fake object
        mock_fake.name.return_value = 'John Doe'
        mock_fake.email.return_value = 'johndoe@example.com'
        mock_fake.street_address.return_value = '123 Main St'
        mock_fake.date_this_century.return_value = '2012-01-01'

        # Generate 3 mock users
        users = generate_users(3)
        print(users)

        # Assert that the number of users generated is equal to 3
        self.assertEqual(len(users), 3)
        

        # Assert that each user has a PK and SK that start with 'USER#'
        for user in users:
            self.assertTrue(user['PK'].startswith('USER#'))
            self.assertTrue(user['SK'].startswith('USER#'))

        # Assert that each user has a UserName, Email, Address, CreatedAt, and Type field
        for user in users:
            self.assertIn('UserName', user)
            self.assertIn('Email', user)
            self.assertIn('Address', user)
            self.assertIn('CreatedAt', user)
            self.assertIn('Type', user)

        # Assert that each user's UserName is formatted correctly
        for user in users:
            self.assertIn('_', user['UserName'])

        # Assert that each user's CreatedAt date is valid
        for user in users:
            self.assertIsInstance(user['CreatedAt'], str)

if __name__ == '__main__':
    unittest.main() 
