from cacpy.CACPy import CACServer
import pytest


class TestServerClass(object):

    def test_template_lookup(self, cac_api):
        template = cac_api.get_template(template_id='27')
        assert template.desc == "Ubuntu-14.04.1-LTS-64bit"

    def test_get_empty_server(self, cac_api):
        server = cac_api.get_server()
        assert (isinstance(server, CACServer))
        assert (server.api_connection == cac_api)

    def test_get_server_by_sid(self, cac_api):
        pytest.raises(LookupError, cac_api.get_server, sid='12345789')

        server = cac_api.get_server(sid='123456789')
        assert (server.sid == '123456789')
        assert (server.template == cac_api.get_template(template_id=26))

    # def test_get_server_by_label(self):

