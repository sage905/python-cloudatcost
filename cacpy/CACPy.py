# Python API Wrapper for cloudatcost.com

import requests

LIST_SERVERS_URL = "https://panel.cloudatcost.com/api/v1/listservers.php"
LIST_TEMPLATES_URL = "https://panel.cloudatcost.com/api/v1/listtemplates.php"
LIST_TASKS_URL = "https://panel.cloudatcost.com/api/v1/listtasks.php"
POWER_OPERATIONS_URL = "https://panel.cloudatcost.com/api/v1/powerop.php"
CONSOLE_URL = "https://panel.cloudatcost.com/api/v1/console.php"


class CACPy:
    """Base class for making requests to the cloud at cost API."""

    def __init__(self, mail, api_key):
        """Return a CACPy object.

        Required Arguments:
        email - The email address used to authenticate to the API.
        api_key - The key generated in the CAC panel to access the API.
        """
        self.email = email
        self.api_key = api_key

    def _make_request(self, url, options=dict(), type="GET"):
        data = {
            'key': self.api_key,
            'login': self.email
        }

        # Add any passed in options to the data dictionary to be included
        # in the web request.
        for key in options:
            data[key] = options[key]

        ret = None
        if type == "GET":
            ret = requests.get(url, params=data)
        elif type == "POST":
            ret = requests.post(url, data=data)
        else:
            raise Exception("InvalidRequestType: " + str(type))

        return ret.json()

    def _commit_power_operation(self, server_id, operation):
        options = {
            'sid': server_id,
            'action': operation
        }
        return self._make_request(POWER_OPERATIONS_URL,
                                  options=options,
                                  type="POST")

    def get_server_info(self):
        """Return an array of dictionaries containing server details.

        The dictionaries will contain keys consistent with the 'data'
        portion of the JSON as documented here:
        https://github.com/cloudatcost/api#list-servers
        """
        jdata = self._make_request(LIST_SERVERS_URL)
        return jdata['data']

    def get_template_info(self):
        """Return an array of dictionaries containing template information.

        The dictionaries will contain keys consistent with the 'data'
        portion of the JSON as documented here:
        https://github.com/cloudatcost/api#list-templates
        """
        jdata = self._make_request(LIST_TEMPLATES_URL)
        return jdata['data']

    def get_task_info(self):
        """Return an array of dictionaries containing task information.

        The dictionaries will contain keys consistent with the 'data'
        portion of the JSON as documented here:
        https://github.com/cloudatcost/api#list-tasks
        """
        jdata = self._make_request(LIST_TASKS_URL)
        return jdata['data']

    def power_on_server(self, server_id):
        """Request that the server specified be powered on.

        Required Arguments:
        server_id - The unique ID assaciated with the server to power on.
                    Specified by the 'sid' key returned by get_server_info()

        The return value will be a dictionary that will contain keys consistent
        with the JSON as documented here:
        https://github.com/cloudatcost/api#power-operations
        """
        return self._commit_power_operation(server_id, 'poweron')

    def power_off_server(self, server_id):
        """Request that the server specified be powered off.

        Required Arguments:
        server_id - The unique ID associated with the server to power off.
                    Specified by the 'sid' key returned by get_server_info()

        The return value will be a dictionary that will contain keys consistent
        with the JSON as documented here:
        https://github.com/cloudatcost/api#power-operations
        """
        return self._commit_power_operation(server_id, 'poweroff')

    def reset_server(self, server_id):
        """Request that the server specified be power cycled.

        Required Arguments:
        server_id - The unique ID associated with the server to power off.
                    Specified by the 'sid' key returned by the get_server_info

        The return value will be a dictionary that will contain keys consistent
        with the JSON as documented here:
        https://github.com/cloudatcost/api#power-operations
        """
        return self._commit_power_operation(server_id, 'reset')

    def get_console_url(self, server_id):
        """Return the URL to the web console for the server specified.

        Required Arguments:
        server_id - The unique ID associated with the server you would
                    like the console URL for.
        """
        options = {
            'sid': server_id
        }
        ret_data = self._make_request(CONSOLE_URL,
                                      options=options,
                                      type="POST")
        return ret_data['console']