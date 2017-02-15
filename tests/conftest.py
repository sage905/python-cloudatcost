from cacpy.CACPy import CACPy, BASE_URL, API_VERSION, LIST_SERVERS_URL, LIST_TEMPLATES_URL
import pytest

V1_LISTSERVERS_RESPONSE = {u'status': u'ok', u'action': u'listservers', u'api': u'v1', u'data': [
    {u'sdate': u'07/14/2015', u'uid': u'4482712345', u'ip': u'10.1.1.2',
     u'servername': u'c123456789-cloudpro-123456789', u'ram': u'2048', u'portgroup': u'Cloud-ip-123',
     u'id': u'123456789', u'label': u'serverlabel', u'vmname': u'c90000-CloudPRO-123456789-123456789',
     u'gateway': u'10.1.1.1', u'hdusage': u'5.123456789', u'rdns': u'server.test.example',
     u'rootpass': u'password',
     u'vncport': u'12345', u'hostname': u'server.test.example', u'storage': u'10', u'cpuusage': u'26',
     u'template': u'CentOS-7-64bit', u'sid': u'123456789', u'vncpass': u'secret', u'status': u'Powered On',
     u'lable': u'serverlabel', u'servertype': u'cloudpro', u'rdnsdefault': u'notassigned.cloudatcost.com',
     u'netmask': u'255.255.255.0', u'ramusage': u'763.086', u'mode': u'Normal', u'packageid': u'15',
     u'panel_note': u'testnote', u'cpu': u'4'}], u'time': 1487000464}

V1_LIST_TEMPLATES_RESPONSE = {u'status': u'ok', u'action': u'listtemplates', u'api': u'v1',
                              u'data': [{u'ce_id': u'1', u'name': u'CentOS 6.7 64bit'},
                                        {u'ce_id': u'3', u'name': u'Debian-8-64bit'},
                                        {u'ce_id': u'9', u'name': u'Windows 7 64bit'},
                                        {u'ce_id': u'24', u'name': u'Windows 2008 R2 64bit'},
                                        {u'ce_id': u'25', u'name': u'Windows 2012 R2 64bit'},
                                        {u'ce_id': u'26', u'name': u'CentOS-7-64bit'},
                                        {u'ce_id': u'27', u'name': u'Ubuntu-14.04.1-LTS-64bit'},
                                        {u'ce_id': u'74', u'name': u'FreeBSD-10-1-64bit'}], u'time': 1487027299}


def mocked_requests_get(*args, **kwargs):
    class MockResponse(object):
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return {
        BASE_URL + API_VERSION + LIST_SERVERS_URL: MockResponse(V1_LISTSERVERS_RESPONSE, 200),
        BASE_URL + API_VERSION + LIST_TEMPLATES_URL: MockResponse(V1_LIST_TEMPLATES_RESPONSE, 200),
    }.get(args[0], MockResponse('', 404))


# This method will be used by the mock to replace requests.get_template in all tests
@pytest.fixture(autouse=True)
def simulate_get(monkeypatch):
    monkeypatch.setattr("requests.get", mocked_requests_get)


@pytest.fixture()
def cac_api():
    return CACPy('test@user.com', 'testkey')


