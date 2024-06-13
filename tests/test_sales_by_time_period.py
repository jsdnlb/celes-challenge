import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from tests.utils.utils_test import (
    setup_test_environment,
    sort_results,
    teardown_test_environment,
)

client = TestClient(app)


class TestSalesByTimePeriod(unittest.TestCase):

    def setUp(self):
        self.data_path = "test_data/"
        self.ROUTE_ENDPOINT = "/api/sales/sales_by_time_period/"
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
    The following tests validate the correct operation of the endpoint
    """

    def test_valid_request_with_keyemployee(self):
        """
        Test to validate the correct operation with query_key KeyEmployee
        """
        response = client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2024-01-01",
                "end_date": "2024-01-02",
                "query_key": "KeyEmployee",
                "data_path": self.data_path,
            },
            headers={"Authorization": f"Bearer {self.valid_token}"},
        )

        expected_response = [
            {"KeyEmployee": 1, "TotalSalesAmount": 350.0, "TotalQuantitySold": 30},
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            sort_results(response.json(), "KeyEmployee"),
            sort_results(expected_response, "KeyEmployee"),
        )

    def test_valid_request_with_keystore_date_out_of_range(self):
        """
        Test to validate the correct operation with query_key KeyStore
        """
        response = client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2023-01-01",
                "end_date": "2023-01-02",
                "query_key": "KeyStore",
                "data_path": self.data_path,
            },
            headers={"Authorization": f"Bearer {self.valid_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json(), [])

    def test_valid_request_with_keystore(self):
        """
        Test to validate the correct operation with query_key KeyStore
        """
        response = client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2024-01-01",
                "end_date": "2024-01-04",
                "query_key": "KeyStore",
                "data_path": self.data_path,
            },
            headers={"Authorization": f"Bearer {self.valid_token}"},
        )

        expected_response = [
            {"KeyStore": 1001, "TotalSalesAmount": 350.0, "TotalQuantitySold": 30},
            {"KeyStore": 1002, "TotalSalesAmount": 1300.0, "TotalQuantitySold": 20},
        ]
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(
            sort_results(response.json(), "KeyStore"),
            sort_results(expected_response, "KeyStore"),
        )

    def test_valid_request_with_keyproduct(self):
        """
        Test to validate the correct operation with query_key KeyProduct
        """
        response = client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2024-01-01",
                "end_date": "2024-01-03",
                "query_key": "KeyProduct",
                "data_path": self.data_path,
            },
            headers={"Authorization": f"Bearer {self.valid_token}"},
        )
        expected_response = [
            {"KeyProduct": 101, "TotalSalesAmount": 450.0, "TotalQuantitySold": 25},
            {"KeyProduct": 102, "TotalSalesAmount": 200.0, "TotalQuantitySold": 20},
        ]
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(
            sort_results(response.json(), "KeyProduct"),
            sort_results(expected_response, "KeyProduct"),
        )

    def test_invalid_date_range(self):
        """
        Test to validate that start date is greater than end date
        """
        response = client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2023-01-02",
                "end_date": "2023-01-01",
                "query_key": "KeyEmployee",
                "data_path": self.data_path,
            },
            headers={"Authorization": f"Bearer {self.valid_token}"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"], "Start date must be greater than end date"
        )

    """ 
    The following tests validate that the data is as expected
    """

    def test_invalid_query_key(self):
        """
        Test to validate that input fails when entering an invalid query_key
        """
        response = client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2023-01-01",
                "end_date": "2023-01-02",
                "query_key": "InvalidKey",
                "data_path": self.data_path,
            },
            headers={"Authorization": f"Bearer {self.valid_token}"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Enter a valid query key")

    def test_to_validate_input_year(self):
        """
        Test to validate the year's input data
        """
        response = client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "20-01-01",
                "end_date": "2023-01-02",
                "query_key": "KeyProduct",
                "data_path": self.data_path,
            },
            headers={"Authorization": f"Bearer {self.valid_token}"},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            "Input should be a valid date or datetime, input is too short",
        )

    def test_to_validate_input_month(self):
        """
        Test to validate the input data of the month greater than 12 in end_date
        """
        response = client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2023-01-01",
                "end_date": "2023-13-02",
                "query_key": "KeyProduct",
                "data_path": self.data_path,
            },
            headers={"Authorization": f"Bearer {self.valid_token}"},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            "Input should be a valid date or datetime, month value is outside expected range of 1-12",
        )

    def test_to_validate_input_day(self):
        """
        Test to validate the input data of the day greater than 31 in end_date
        """
        response = client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2023-01-32",
                "end_date": "2023-13-02",
                "query_key": "KeyProduct",
                "data_path": self.data_path,
            },
            headers={"Authorization": f"Bearer {self.valid_token}"},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            "Input should be a valid date or datetime, day value is outside expected range",
        )


if __name__ == "__main__":
    unittest.main()
