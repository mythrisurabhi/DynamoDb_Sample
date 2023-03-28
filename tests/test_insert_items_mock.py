import unittest
from unittest.mock import patch, MagicMock
from sample_data_insert import insert_items
data = [
    {'user_id': '1', 'name': 'John'},
    {'order_id': '100', 'user_id': '1', 'product_id': 'p100'},
    {'category_id': 'c1', 'category_name': 'Electronics'}
]


class TestInsertItems(unittest.TestCase):

    @patch('sample_data_insert.create_dynamodb_resource')
    def test_insert_items(self, mock_create_dynamodb_resource):
        # Arrange
        mock_table = MagicMock()
        mock_batch_writer = MagicMock()
        mock_table.batch_writer.return_value.__enter__.return_value = mock_batch_writer
        mock_create_dynamodb_resource.return_value.Table.return_value = mock_table

        # Act
        insert_items(data)

        # Assert
        expected_batch_size = 25
        expected_batches = len(data) // expected_batch_size + \
            (1 if len(data) % expected_batch_size > 0 else 0)
        self.assertEqual(mock_create_dynamodb_resource.call_count, 1)
        self.assertEqual(
            mock_create_dynamodb_resource.return_value.Table.call_count, 1)
        self.assertEqual(
            mock_create_dynamodb_resource.return_value.Table.call_args[0][0], 'orders-users-products')
        self.assertEqual(mock_table.batch_writer.call_count, expected_batches)
        expected_put_items = [item for item in data]
        actual_put_items = []
        for args, kwargs in mock_batch_writer.put_item.call_args_list:
            actual_put_items.append(kwargs['Item'])
        self.assertEqual(expected_put_items, actual_put_items)


if __name__ == '__main__':
    unittest.main()
