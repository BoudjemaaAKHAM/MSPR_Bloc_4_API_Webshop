# tests unitaires pour le module benchmark_api.py
# A vérifier car c'est juste un draft !!!!!!!!!!!!!!

import unittest
from unittest.mock import patch
from benchmark_api import get_customers, get_customer, get_customer_orders


class TestBenchmarkApi(unittest.TestCase):

    @patch('benchmark_api.requests.get')
    def test_get_customers(self, mock_get):
        mock_get.return_value.json.return_value = 'test'
        self.assertEqual(get_customers(), 'test')

    @patch('benchmark_api.requests.get')
    def test_get_customer(self, mock_get):
        mock_get.return_value.json.return_value = 'test'
        self.assertEqual(get_customer(1), 'test')

    @patch('benchmark_api.requests.get')
    def test_get_customer_orders(self, mock_get):
        mock_get.return_value.json.return_value = 'test'
        self.assertEqual(get_customer_orders(1), 'test')


if __name__ == '__main__':
    unittest.main()
