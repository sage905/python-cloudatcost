import CACPy
import mock


class TestAPI(object):
    def test_api_calls_correct_url(self):
        cac_api = CACPy.CACPy('test@user.com', 'testkey')

        with mock.patch('requests.get') as get_mock:
            cac_api.get_server_info()
            get_mock.assert_called_with(CACPy.BASE_URL + CACPy.API_VERSION + CACPy.LIST_SERVERS_URL, params={'login': 'test@user.com', 'key': 'testkey'}, timeout=30)

