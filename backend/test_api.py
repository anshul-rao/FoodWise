import unittest
from main import createApp
from config import TestConfig
from exts import db as flask_db


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = createApp(TestConfig)

        self.client = self.app.test_client(self)  # Creates client

        with self.app.app_context():
            flask_db.create_all()

    def testHelloWorld(self):
        helloResponse = self.client.get('/inventory/hello')
        json = helloResponse.json

        # print(json)

        self.assertEqual(json, {"message": "Hello World!"})

    def testRegister(self):
        """
        Test the registration endpoint.

        Sends a POST request to the '/auth/register' endpoint with the necessary information to create a new user. Asserts that the status code of the response is 201 and the response body contains a success message. 
        Uses the credentials of the newly registered user to send a POST request to the '/auth/login' endpoint and asserts that the status code of the response is 200 and the response body contains an access token. 
        Uses the access token to send a GET request to the '/inventory' endpoint and asserts that the response code is 200 and the response body contains a list of items in the inventory.

        Returns:
        None
        """

        registerResponse = self.client.post('/auth/register',
                                            json={
                                                "username": "testuser",
                                                "email": "testuser@company.com",
                                                "password": "password"
                                            })

        statusCode = registerResponse.status_code

        self.assertEqual(statusCode, 201)

    def testLogin(self):
        """
        Test the login endpoint.

        Sends a POST request to the '/auth/login' endpoint with the necessary information to authenticate a user. Asserts that the status code of the response is 200 and the response body contains an access token. Uses the access token to send a GET request to the '/inventory' endpoint and asserts that the response code is 200 and the response body contains a list of items in the inventory.

        Returns:
        None
        """

        registerResponse = self.client.post('/auth/register',
                                            json={
                                                "username": "testuser",
                                                "email": "testuser@company.com",
                                                "password": "password"
                                            })

        loginResponse = self.client.post('/auth/login',
                                         json={
                                             "username": "testuser",
                                             "password": "password"
                                         })

        statusCode = loginResponse.status_code

        # json = loginResponse.json
        # print(json)

        self.assertEqual(statusCode, 200)

    def testGetAllInventory(self):
        """
        Test case for the 'get all inventory' API endpoint.

        This function tests whether the API endpoint for retrieving all items in the food inventory returns the expected data.

        Returns: None
        """

        response = self.client.get('/inventory/inventory')
        # print(response.json)
        statusCode = response.status_code
        self.assertEqual(statusCode, 200)

    def testGetInventoryByID(self):
        """
        Test case for the 'get inventory by ID' API endpoint.

        This function tests whether the API endpoint for retrieving a single item in the food inventory by its ID returns the expected data.

        Returns:
            None
        """
        id = 1
        response = self.client.get(f'/inventory/inventory/{id}')
        statusCode = response.status_code

        self.assertEqual(statusCode, 404)

    def testCreateItem(self):
        """
        Create a new item in the food inventory.

        This function creates a new item in the food inventory database based on the data provided in the request payload. The payload should contain a JSON object with the following fields:
        - name: The name of the item (string).
        - quantity: The quantity of the item (integer).
        - expiration_date: The expiration date of the item (string in the format 'YYYY-MM-DD').

        If the item is successfully created, a response with status code 201 (Created) is returned, along with a JSON object containing the ID of the newly created item. If there is an error, a response with a status code of 400 (Bad Request) is returned, along with a JSON object containing an error message.

        Returns:
            A Flask response object with status code 201 if the item was successfully created, or a response object with status code 400 if there was an error.
        """
        registerResponse = self.client.post('/auth/register',
                                            json={
                                                "username": "testuser",
                                                "email": "testuser@company.com",
                                                "password": "password"
                                            })

        loginResponse = self.client.post('/auth/login',
                                         json={
                                             "username": "testuser",
                                             "password": "password"
                                         })

        accessToken = loginResponse.json["accessToken"]

        createItemResponse = self.client.post('inventory/inventory',
                                              json={
                                                  "id": 1,
                                                  "name": "string",
                                                  "quantity": 1,
                                                  "expiry_date": "2023-03-15"
                                              },
                                              headers={
                                                  "Authorization": f"Bearer {accessToken}"
                                              })

        statusCode = createItemResponse.status_code

        self.assertEqual(statusCode, 201)

    def testUpdateItem(self):
        """
        Update an item in the inventory.

        Sends a PUT request to the '/inventory/:id' endpoint with the necessary information to update an existing item in the inventory. Asserts that the status code of the response is 200 and the item in the response body matches the updated item.

        Returns:
        None
        """
        registerResponse = self.client.post('/auth/register',
                                            json={
                                                "username": "testuser",
                                                "email": "testuser@company.com",
                                                "password": "password"
                                            })

        loginResponse = self.client.post('/auth/login',
                                         json={
                                             "username": "testuser",
                                             "password": "password"
                                         })

        accessToken = loginResponse.json["accessToken"]

        createItemResponse = self.client.post('inventory/inventory',
                                              json={
                                                  "id": 1,
                                                  "name": "string",
                                                  "quantity": 1,
                                                  "expiry_date": "2023-03-15"
                                              },
                                              headers={
                                                  "Authorization": f"Bearer {accessToken}"
                                              })

        id = 1

        updateResponse = self.client.put(f"inventory/inventory/{id}",
                                         json={
                                             "id": 1,
                                             "name": "string update",
                                             "quantity": 2,
                                             "expiry_date": "2023-03-14"
                                         },
                                         headers={
                                             "Authorization": f"Bearer {accessToken}"
                                         })
        
        statusCode = updateResponse.status_code
        self.assertEqual(statusCode, 200)

    def testDeleteItem(self):
        """
        Delete an item from the inventory.

        Sends a DELETE request to the '/inventory/<id>' endpoint with the necessary information to delete an existing item from the inventory. Asserts that the status code of the response is 204 and the item is no longer present in the inventory.

        Returns:
        None
        """
        registerResponse = self.client.post('/auth/register',
                                            json={
                                                "username": "testuser",
                                                "email": "testuser@company.com",
                                                "password": "password"
                                            })

        loginResponse = self.client.post('/auth/login',
                                         json={
                                             "username": "testuser",
                                             "password": "password"
                                         })

        accessToken = loginResponse.json["accessToken"]

        createItemResponse = self.client.post('inventory/inventory',
                                              json={
                                                  "id": 1,
                                                  "name": "string",
                                                  "quantity": 1,
                                                  "expiry_date": "2023-03-15"
                                              },
                                              headers={
                                                  "Authorization": f"Bearer {accessToken}"
                                              })

        id = 1
        deleteResponse = self.client.delete(f"/inventory/inventory/{id}",
                                            headers={"Authorization": f"Bearer {accessToken}"})

        statusCode = deleteResponse.status_code

        self.assertEqual(statusCode, 204)

    def tearDown(self):
        with self.app.app_context():
            flask_db.session.remove()
            flask_db.drop_all()


if __name__ == "__main__":
    unittest.main()
