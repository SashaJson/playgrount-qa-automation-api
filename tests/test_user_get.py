from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get('/user/2')

        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'email',
            'password': 'password'
        }

        first_response = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(first_response, 'auth_sid')
        token = self.get_header(first_response, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(first_response, 'user_id')

        second_response = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        expected_fields = ['username', 'email', 'firstName', 'lastName']
        Assertions.assert_json_has_keys(second_response, expected_fields)