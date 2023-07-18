import allure
import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Register cases")
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

    @allure.title("Test create user with incorrect email")
    @allure.description("This test checks create user with incorrect email")
    @allure.link("https://software-testing.ru/lms/mod/assign/view.php?id=341786")
    @allure.severity(allure.severity_level.CRITICAL)
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

    @allure.title("Test create user without one parameter")
    @allure.description("This test checks create user without one parameter")
    @allure.link("https://software-testing.ru/lms/mod/assign/view.php?id=341786")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("parameters", parameters)
    def test_create_user_without_one_parameter(self, parameters):
        response = requests.post("https://playground.learnqa.ru/api/user", data=parameters)

        assert response.status_code == 400, f'Unexpected status code {response.status_code}'
        assert 'The following required params are missed' in response.content.decode(
            "utf-8"), f'Unexpected response content {response.content}'

    @allure.title("Test create user with short name")
    @allure.description("This test checks create user with short name")
    @allure.link("https://software-testing.ru/lms/mod/assign/view.php?id=341786")
    @allure.severity(allure.severity_level.CRITICAL)
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

    @allure.title("Test create user with long name")
    @allure.description("This test checks create user with long name")
    @allure.link("https://software-testing.ru/lms/mod/assign/view.php?id=341786")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_long_name(self):
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