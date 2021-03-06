from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
import pytest
import allure


@allure.epic('Authorization cases')
class TestUserAuth(BaseCase):
    exclude_params = [
        ('no_cookie'),
        ('no_token')
    ]

    def setup(self):
        data = {
            'email': 'email',
            'password': 'password'
        }

        first_response = MyRequests.post('/user/login', data=data)

        self.auth_sid = self.get_cookie(first_response, 'auth_sid')
        self.token = self.get_header(first_response, 'x-csrf-token')
        self.user_id_from_auth_method = self.get_json_value(first_response, 'user_id')

    @allure.description('This test successfully authorize user by email and password')
    def test_auth_user(self):

        second_response = MyRequests.get(
            '/user/auth',
            headers={'x-csrf-token': self.token},
            cookies={'auth_sid': self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            second_response,
            'user_id',
            self.user_id_from_auth_method,
            'User id from auth method is not equal to user id from check method'
        )

    @allure.description('This test checks authorization status w/o sending auth cookie ot token')
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == 'no_cookie':
            second_response = MyRequests.get('/user/auth', headers={'x-csrf-token': self.token})
        else:
            second_response = MyRequests.get('/user/auth', cookies={'auth_sid': self.auth_sid})

        Assertions.assert_json_value_by_name(
            second_response,
            'user_id',
            0,
            f"User is authorized with condition {condition}"
        )
