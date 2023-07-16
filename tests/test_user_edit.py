import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):

    def test_edit_without_auth(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # EDIT
        new_name = "Changed name"

        response2 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", data={"firstName": new_name})

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode(
            "utf-8") == "Auth token not supplied", f'Unexpected response content {response2.content}'


    def test_edit_with_auth_by_another_user(self):
        # REGISTER USER 1
        register_data1 = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user", data=register_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # REGISTER USER 2
        register_data2 = self.prepare_registration_data()
        response2 = requests.post("https://playground.learnqa.ru/api/user", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email = register_data2["email"]
        password = register_data2["password"]

        #LOGIN USER 2
        login_data = {
            'email': email,
            'password': password
        }

        response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")


        # EDIT
        new_name = "Changed name"

        response4 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name})

        Assertions.assert_code_status(response4, 400)


    def test_edit_with_incorrect_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        email = register_data["email"]
        password = register_data["password"]

        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


        # EDIT
        new_email = "Changed_email.ru"

        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"email": new_email})

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode(
            "utf-8") == "Invalid email format", f'Unexpected response content {response3.content}'


    def test_edit_with_incorrect_first_name(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        email = register_data["email"]
        password = register_data["password"]

        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


        # EDIT
        new_first_name = "A"

        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_first_name})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "Too short value for field firstName", f'Unexpected response content {response3.content}')