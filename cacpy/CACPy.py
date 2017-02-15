# Python API Wrapper for cloudatcost.com

import requests
import attr

BASE_URL = "https://panel.cloudatcost.com/api/"
API_VERSION = "v1"

LIST_SERVERS_URL = "/listservers.php"
LIST_TEMPLATES_URL = "/listtemplates.php"
LIST_TASKS_URL = "/listtasks.php"
POWER_OPERATIONS_URL = "/powerop.php"
CONSOLE_URL = "/console.php"
RENAME_SERVER_URL = "/renameserver.php"
REVERSE_DNS_URL = "/rdns.php"
RUN_MODE_URL = "/runmode.php"

# CloudPRO functions:

SERVER_BUILD_URL = "/cloudpro/build.php"
SERVER_DELETE_URL = "/cloudpro/delete.php"
RESOURCE_URL = "/cloudpro/resources.php"


class CACPy(object):
    """Base class for making requests to the cloud at cost API.
    """

    def __init__(self, email, api_key, timeout=30):
        """Return a CACPy object.

        Required Arguments:
        email - The email address used to authenticate to the API.
        api_key - The key generated in the CAC panel to access the API.
        """
        self.email = email
        self.api_key = api_key
        self.timeout = timeout

    def _make_request(self, endpoint, options=None, type="GET"):
        if options is None:
            options = dict()
        data = {
            'key': self.api_key,
            'login': self.email
        }

        # Add any passed in options to the data dictionary to be included
        # in the web request.
        for key in options:
            data[key] = options[key]

        url = BASE_URL + API_VERSION + endpoint

        if type == "GET":
            ret = requests.get(url, params=data, timeout=self.timeout)
        elif type == "POST":
            ret = requests.post(url, data=data, timeout=self.timeout)
        else:
            raise Exception("InvalidRequestType: " + str(type))

        if ret.status_code != 200:
            raise IOError("CAC API did not return valid response.  Status Code: " + str(ret.status_code))

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
        return self._make_request(LIST_SERVERS_URL)

    def get_template_info(self):
        """Return an array of dictionaries containing template information.

        The dictionaries will contain keys consistent with the 'data'
        portion of the JSON as documented here:
        https://github.com/cloudatcost/api#list-templates
        NOTE: The format of data returned by this has changed from what is posted in the documentation

        """
        return self._make_request(LIST_TEMPLATES_URL)

    def get_task_info(self):
        """Return an array of dictionaries containing task information.

        The dictionaries will contain keys consistent with the 'data'
        portion of the JSON as documented here:
        https://github.com/cloudatcost/api#list-tasks
        """
        return self._make_request(LIST_TASKS_URL)

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
                    Specified by the 'sid' key returned by get_server_info()

        The return value will be a dictionary that will contain keys consistent
        with the JSON as documented here:
        https://github.com/cloudatcost/api#power-operations
        """
        return self._commit_power_operation(server_id, 'reset')

    def rename_server(self, server_id, new_name):
        """Modify the name label of the specified server.

        Required Arguments:
        server_id - The unique ID associated with the server to change the
                    label of. Specified by the 'sid' key returned by
                    get_server_info()
        new_name - String to set as the name label.

        The return value will be a dictionary that will contain keys consistent
        with the JSON as documented here:
        https://github.com/cloudatcost/api#rename-server
        """
        options = {
            'sid': server_id,
            'name': new_name
        }
        return self._make_request(RENAME_SERVER_URL,
                                  options=options,
                                  type="POST")

    def change_hostname(self, server_id, new_hostname):
        """Modify the hostname of the specified server.

        Required Arguments:
        server_id - The unique ID associated with the server to change the
                    hostname of. Specified by the 'sid' key returned by
                    get_server_info()
        new_hostname - Fully qualified domain name to set for the host

        The return value will be a dictionary that will contain keys consistent
        with the JSON as documented here:
        https://github.com/cloudatcost/api#modify-reverse-dns
        """
        options = {
            'sid': server_id,
            'hostname': new_hostname
        }
        return self._make_request(REVERSE_DNS_URL,
                                  options=options,
                                  type="POST")

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

    def set_run_mode(self, server_id, run_mode):
        """Set the run mode of the server.

        Required Arguments:
        server_id - The unique ID associated with the server to change the
                    hostname of. Specified by the 'sid' key returned by
                    get_server_info()
        run_mode -  Set the run mode of the server to either 'normal' or 'safe'.
                    Safe automatically turns off the server after 7 days of idle usage.
                    Normal keeps it on indefinitely.
        """
        options = {
            'sid': server_id,
            'mode': run_mode
        }
        return self._make_request(RUN_MODE_URL,
                                  options=options,
                                  type="POST")

    def server_build(self, cpu, ram, disk, os):
        """Build a server from available cloudPRO resources.

        Required Arguments:
        cpu - The number of vCPUs to provision to the new server.
              Use an integer from 1 to 9.
        ram - The amount of memory to provision to the new server.
              Value in megabytes, must be a multiple of 4.
              Examples: 1024, 2048, 4096
        disk - The amount of disk space to provision to the server.
               Value in gigabytes in multiples of 10.
        os - The Operating System template to apply to the server.
             Specified by an id number returned by get_template_info()
        """
        options = {
            'cpu': cpu,
            'ram': ram,
            'storage': disk,
            'os': os
        }
        return self._make_request(SERVER_BUILD_URL,
                                  options=options,
                                  type="POST")

    def server_delete(self, server_id):
        """Delete a cloudPRO server and free associated resources.

        Required Arguments:
        server_id - The unique ID associated with the server to change the
                    hostname of. Specified by the 'sid' key returned by
                    get_server_info()
        """
        options = {
            'sid': server_id
        }
        return self._make_request(SERVER_DELETE_URL,
                                  options=options,
                                  type="POST")

    def get_resources(self):
        """Returns information about CloudPRO resource usage.
        """

        return self._make_request(RESOURCE_URL,
                                  type="GET")

    def get_template(self, desc=None, template_id=None):
        """Return a CACTemplate after querying the Cloudatcost API for a list of templates for a match.

        Required Arguments:
        api_connection - CACPy object to use for connection
        desc - Description to be matched (or use template_id)
        template_id - Template ID to be matched (or use desc)

        Raises:
        LookupError if desc or template_id can't be found
        ValueError if no lookup parameters are provided
        """
        if isinstance(template_id, int):
            template_id = str(template_id)
        templates = self.get_template_info()['data']

        if template_id is not None:
            try:
                template = next(template for template in templates if template.get('ce_id') == template_id)
            except StopIteration:
                raise LookupError("Template with ID: " + template_id + " was not found")
            return CACTemplate(template.get('name'), template_id)
        elif desc is not None:
            try:
                template = next(template for template in templates if template.get('name') == desc)
            except StopIteration:
                raise LookupError("Template with description: " + desc + " was not found")
            return CACTemplate(desc, template.get('ce_id'))
        else:
            raise ValueError("One of 'desc' or 'template_id' must be provided to template lookup.")

    def get_server(self, sid=None, label=None):
        """Get a CACServer Instance.

        If neither sid nor label are specified, returns an empty instance.
        If both sid and label are specified, sid takes precedence.

        :param sid: Server ID to lookup
        :param label: Server label to lookup
        :return: CACServer Instance
        """
        for key,value in (('sid', sid ), ('label', label)):
            if value is not None:
                try:
                    server = next(
                        server for server in self.get_server_info().get('data') if server[key] == value)
                except StopIteration:
                    raise LookupError("Server with " + key + ": " + value + " was not found.")
                return CACServer(self, **server)

        return CACServer(self)

@attr.s
class CACTemplate(object):
    """ Mapping of CAC template description and ID
    """

    desc = attr.ib(convert=str)
    template_id = attr.ib(convert=str)


class CACServer(object):
    """Represent a server instance at cloudatost.
    """

    __attrs__ = ('uid', 'servername', 'sdate', 'sid', 'label', 'rdns', 'cpu', 'ram', 'storage', 'panel_note',
                 'rootpass', 'ip', 'netmask', 'gateway', 'status', 'mode', 'servertype', 'ramusage', 'cpuusage',
                 'hdusage')

    def __init__(self, api_connection, template=None, **kwargs):
        assert isinstance(api_connection, CACPy)

        self.api_connection = api_connection

        [setattr(self, name, kwargs.get(name)) for name in CACServer.__attrs__]

        if template is not None:
            self.template = api_connection.get_template(desc=template)

    def __repr__(self):
        return ('{cls.__name__}(api_account={self.api_connection.email}, sid={self.sid}, '
                'label={self.label})').format(
            cls=type(self), self=self)


        # class Ram(object):
        #     def __init__(self, name, default=None):
        #         self.name = name
        #         self.default = default
        #
        #     def __get__(self, instance, owner):
        #         return getattr(instance, self.name, self.default)
        #
        #     def clean(self, value):
        #         if isinstance(value, int) or str(value).isdigit():
        #             return int(value)
        #         return value
        #
        #     def __set__(self, instance, value):
        #         if isinstance(self.clean(value), int):
        #             setattr(instance, self.name, value)
        #         else:
        #             raise TypeError('`{}` not a valid integer'.format(value))
