import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app


class TestSalesByTimePeriod(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.valid_token = self.get_valid_token()
        self.ROUTE_ENDPOINT = "/api/sales/sales_by_time_period/"

    def get_valid_token(self):
        with patch("firebase_admin.auth"):
            # Simulate POST request to obtain an authorization token
            response = self.client.post(
                "/api/users/token",
                data={"username": "test@example.com", "password": "password"},
            )

            assert response.status_code == 200

            # Extract the token from the body of the response and return it
            return response.json()["access_token"]

    """
    The following tests validate the correct operation of the endpoint
    """

    def test_valid_request_with_keyemployee(self):
        """
        Test to validate the correct operation with query_key KeyEmployee
        """
        response = self.client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2023-01-01",
                "end_date": "2023-01-02",
                "query_key": "KeyEmployee",
            },
            headers={"Authorization": f"Bearer {self.valid_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_valid_request_with_keystore(self):
        """
        Test to validate the correct operation with query_key KeyStore
        """
        response = self.client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2023-01-01",
                "end_date": "2023-01-02",
                "query_key": "KeyStore",
            },
            headers={"Authorization": f"Bearer {self.valid_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_valid_request_with_keyproduct(self):
        """
        Test to validate the correct operation with query_key KeyProduct
        """
        response = self.client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2023-01-01",
                "end_date": "2023-01-02",
                "query_key": "KeyProduct",
            },
            headers={"Authorization": f"Bearer {self.valid_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_invalid_date_range(self):
        """
        Test to validate that start date is greater than end date
        """
        response = self.client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2023-01-02",
                "end_date": "2023-01-01",
                "query_key": "KeyEmployee",
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
        response = self.client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2023-01-01",
                "end_date": "2023-01-02",
                "query_key": "InvalidKey",
            },
            headers={"Authorization": f"Bearer {self.valid_token}"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Enter a valid query key")

    def test_to_validate_input_year(self):
        """
        Test to validate the year's input data
        """
        response = self.client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "20-01-01",
                "end_date": "2023-01-02",
                "query_key": "KeyProduct",
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
        response = self.client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2023-01-01",
                "end_date": "2023-13-02",
                "query_key": "KeyProduct",
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
        response = self.client.get(
            self.ROUTE_ENDPOINT,
            params={
                "start_date": "2023-01-32",
                "end_date": "2023-13-02",
                "query_key": "KeyProduct",
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
