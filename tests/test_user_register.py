import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):
    parameters = [
        {
            #'password': '123',
            'username': 'username',
            'firstName': 'firstName',
            'lastName': 'lastName',
            'email': 'example@example.ru'
        },
        {
            'password': '123',
            #'username': 'username',
            'firstName': 'firstName',
            'lastName': 'lastName',
            'email': 'example@example.ru'
        },
        {
            'password': '123',
            'username': 'username',
            #'firstName': 'firstName',
            'lastName': 'lastName',
            'email': 'example@example.ru'
        },
        {
            'password': '123',
            'username': 'username',
            'firstName': 'firstName',
            #'lastName': 'lastName',
            'email': 'example@example.ru'
        },
        {
            'password': '123',
            'username': 'username',
            'firstName': 'firstName',
            'lastName': 'lastName'
            #'email': 'example@example.ru'
        }
    ]

    def test_create_user_with_incorrect_email(self):
        email = 'example.example.ru'
        data = {
            'password': '123',
            'username': 'username',
            'firstName': 'firstName',
            'lastName': 'lastName',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user", data=data)

        assert response.status_code == 400, f'Unexpected status code {response.status_code}'
        assert response.content.decode("utf-8") == "Invalid email format", f'Unexpected response content {response.content}'


    @pytest.mark.parametrize("parameters", parameters)
    def test_create_user_without_one_parameter(self, parameters):
        response = requests.post("https://playground.learnqa.ru/api/user", data=parameters)

        assert response.status_code == 400, f'Unexpected status code {response.status_code}'
        assert 'The following required params are missed' in response.content.decode(
            "utf-8"), f'Unexpected response content {response.content}'


    def test_create_user_with_short_name(self):
        name = 'A'
        data = {
            'password': '123',
            'username': name,
            'firstName': 'firstName',
            'lastName': 'lastName',
            'email': 'example@example.ru'
        }

        response = requests.post("https://playground.learnqa.ru/api/user", data=data)

        assert response.status_code == 400, f'Unexpected status code {response.status_code}'
        assert response.content.decode(
            "utf-8") == "The value of 'username' field is too short", f'Unexpected response content {response.content}'

    def test_create_user_with_short_name(self):
        name = 'Ааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааа' \
               'ааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааа' \
               'ааааааааааааааааааааааааааааааааааааааааааааааааааааааааа'
        data = {
            'password': '123',
            'username': name,
            'firstName': 'firstName',
            'lastName': 'lastName',
            'email': 'example@example.ru'
        }

        response = requests.post("https://playground.learnqa.ru/api/user", data=data)

        assert response.status_code == 400, f'Unexpected status code {response.status_code}'
        assert response.content.decode(
            "utf-8") == "The value of 'username' field is too long", f'Unexpected response content {response.content}'