import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from tests.utils.utils_test import (
    setup_test_environment,
    teardown_test_environment,
    sort_results,
)

client = TestClient(app)


class TestTotalAndAverageSales(unittest.TestCase):

    def setUp(self):
        self.data_path = "test_data/"
        self.ROUTE_ENDPOINT = "/api/sales/total_and_average_sales/"
        self.valid_token = self.get_valid_token()
        setup_test_environment(self.data_path)

    def tearDown(self):
        teardown_test_environment(self.data_path)

    def get_valid_token(self):
        with patch("firebase_admin.auth"):
            response = client.post(
                "/api/users/token",
                data={"username": "test@example.com", "password": "password"},
            )
            assert response.status_code == 200
            return response.json()["access_token"]

    """ 
    The following tests validate that the endpoint brings the average and
    total amount for KeyStore, KeyProdiuct and KeyEmployee.
    """

    def test_total_and_average_sales_keystore(self):
        response = client.get(
            self.ROUTE_ENDPOINT,
            headers={"Authorization": f"Bearer {self.valid_token}"},
            params={"query_key": "KeyStore", "data_path": self.data_path},
        )
        expected_response = [
            {"KeyStore": 1001, "TotalAmount": 350.0, "AvgAmount": 175.0},
            {"KeyStore": 1002, "TotalAmount": 1300.0, "AvgAmount": 650.0},
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            sort_results(response.json(), "KeyStore"),
            sort_results(expected_response, "KeyStore"),
        )

    def test_total_and_average_sales_keyproduct(self):
        response = client.get(
            self.ROUTE_ENDPOINT,
            headers={"Authorization": f"Bearer {self.valid_token}"},
            params={"query_key": "KeyProduct", "data_path": self.data_path},
        )
        expected_response = [
            {
                "KeyProduct": 101,
                "TotalAmount": 1450.0,
                "AvgAmount": 483.3333333333333,
            },
            {"KeyProduct": 102, "TotalAmount": 200.0, "AvgAmount": 200.0},
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            sort_results(response.json(), "KeyProduct"),
            sort_results(expected_response, "KeyProduct"),
        )

    def test_total_and_average_sales_keyemployee(self):
        response = client.get(
            self.ROUTE_ENDPOINT,
            headers={"Authorization": f"Bearer {self.valid_token}"},
            params={"query_key": "KeyEmployee", "data_path": self.data_path},
        )
        expected_response = [
            {
                "KeyEmployee": 1,
                "TotalAmount": 350.0,
                "AvgAmount": 175.0,
            },
            {"KeyEmployee": 2, "TotalAmount": 300.0, "AvgAmount": 300.0},
            {"KeyEmployee": 3, "TotalAmount": 1000.0, "AvgAmount": 1000.0},
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            sort_results(response.json(), "KeyEmployee"),
            sort_results(expected_response, "KeyEmployee"),
        )

    def test_total_and_average_sales_invalid_key(self):
        """
        This test validates the exception that we must enter a valid query_key.
        """
        response = client.get(
            self.ROUTE_ENDPOINT,
            headers={"Authorization": f"Bearer {self.valid_token}"},
            params={"query_key": "InvalidKey", "data_path": self.data_path},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Enter a valid query key"})

    def test_total_and_average_sales_without_token(self):
        """
        This test validates that we are logged in to access the endpoint.
        """
        response = client.get(
            self.ROUTE_ENDPOINT,
            headers={"Authorization": f"Bearer fake-token"},
            params={"query_key": "KeyStore", "data_path": self.data_path},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(), {"detail": "Invalid authentication credentials"}
        )


if __name__ == "__main__":
    unittest.main()
