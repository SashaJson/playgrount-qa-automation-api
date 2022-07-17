from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        first_response = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(first_response, 200)
        Assertions.assert_json_has_key(first_response, 'id')

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(first_response, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        second_response = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(second_response, 'auth_sid')
        token = self.get_header(second_response, 'x-csrf-token')

        # EDIT
        new_name = 'Changed Name'

        third_response = MyRequests.put(
            f"/user/{user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(third_response, 200)

        # GET
        fourth_response = MyRequests.get(
            f"/user/{user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_json_value_by_name(
            fourth_response,
            'firstName',
            new_name,
            'Wrong name of the user after edit'
        )
