from .base import Synthetics
import json

class Monitors(Synthetics):
    """
    An interface for interacting with the NewRelic Synthetics monitors API.
    """

    def list(self, page=None):
        """
        This API endpoint returns a paginated list of the monitors
        associated with your New Relic account.

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::
            {
                "monitors": [
                    {
                        "id": UUID,
                        "name": string,
                        "type": string,
                        "frequency": integer,
                        "uri": string,
                        "locations": array of strings,
                        "status": string,
                        "slaThreshold": double,
                        "userId": integer,
                        "apiVersion": string
                    }
                ],
                "pages": {
                    "last": {
                        "url": "https://synthetics.newrelic.com/synthetics/api/v1/monitors?page=2",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://synthetics.newrelic.com/synthetics/api/v1/monitors?page=2",
                        "rel": "next"
                    }
                }
            }

        """

        filters = [
            'page={0}'.format(page) if page else None
        ]

        return self._get(
            url='{0}monitors'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def show(self, id):
        """
        This API endpoint returns a single monitor, identified by
        ID.

        :type id: int
        :param id: monitor ID

        :rtype: dict
        :return: The JSON response of the API
        """
        return self._get(
            url='{0}monitors/{1}'.format(self.URL, id),
            headers=self.headers,
        )

    def show_locations(self):
        """
        This API endpoint the list of valid monitoring locations.

        :rtype: dict
        :return: The JSON response of the API
        """
        return self._get(
            url='{0}locations'.format(self.URL, id),
            headers=self.headers,
        )

    def create(self, name, type, frequency, locations, status, **kwargs):
        """
        This API endpoint will create a new monitor

        :type name: str
        :param name: The name of the monitor

        :type type: str
        :param type: The type of monitor (must be one of SIMPLE, BROWSER, SCRIPT_API, SCRIPT_BROWSER)

        :type frequency: int
        :param frequency: Monitor interval (in minutes).  Must be one of 1, 5, 10, 15, 30, 60, 360, 720, or 1440.

        :type locations: list of str
        :param locations: The API names of the locations from which to monitor.  At least one required.
            Send a GET request to https://synthetics.newrelic.com/synthetics/api/v1/locations to get a list
            of valid locations.

        :type status: str
        :param status: One of ENABLED, MUTED, or DISABLED

        :rtype: str
        :return: The newly created monitor ID

        ::

        """

        data = {
            "name": name,
            "type": type,
            "frequency": frequency,
            "locations": locations,
            "status": status
        }
        data.update(**kwargs)

        response = self._post(
            url='{0}monitors'.format(self.URL),
            headers=self.headers,
            data=data,
            get_raw_response=True
        )

        return response.headers['Location'].rsplit('/', 1)[-1]

    def update(self, id, name, type, frequency, locations, status, **kwargs):
        """
        This API endpoint will update an existing monitor

        :type id: str
        :param id: The ID of the monitor to update

        :type name: str
        :param name: The name of the monitor

        :type type: str
        :param type: The type of monitor (must be one of SIMPLE, BROWSER, SCRIPT_API, SCRIPT_BROWSER)

        :type frequency: int
        :param frequency: Monitor interval (in minutes).  Must be one of 1, 5, 10, 15, 30, 60, 360, 720, or 1440.

        :type locations: list of str
        :param locations: The API names of the locations from which to monitor.  At least one required.
            Send a GET request to https://synthetics.newrelic.com/synthetics/api/v1/locations to get a list
            of valid locations.

        :type status: str
        :param status: One of ENABLED, MUTED, or DISABLED

        :rtype: bool
        :return: Returns True on success, False otherwise

        ::

        """

        data = {
            "name": name,
            "type": type,
            "frequency": frequency,
            "locations": locations,
            "status": status
        }
        data.update(**kwargs)

        response = self._put(
            url='{0}monitors/{1}'.format(self.URL, id),
            headers=self.headers,
            data=data,
            get_raw_response=True
        )

        if response.ok:
            return True
        else:
            return False

    def update_script(self, id, scriptText, scriptLocations=None):
        """
            This API endpoint will update an existing SCRIPT_BROWSER or SCRIPT_API monitor with the appropriate script

            :type id: str
            :param id: The ID of the monitor to update

            :type scriptText: str
            :param scriptText: The BASE64 encoded text for scripted monitors

            :type scriptLocations: list of dict
            :param scriptLocations: The name and hmac values for private locations using Verified Script Execution.

            :rtype: bool
            :return: Returns True on success, False otherwise

            ::

            """

        data = {
            'scriptText': scriptText
        }
        if scriptLocations is not None:
            data['scriptLocations'] = scriptLocations

        response = self._put(
            url='{0}monitors/{1}/script'.format(self.URL, id),
            headers=self.headers,
            data=data,
            get_raw_response=True
        )

        if response.ok:
            return True
        else:
            return False

    def delete(self, id):
        """
        This API endpoint will create a new label with the provided name and
        category

        :type id: str
        :param id: The ID of the monitor to delete

        :rtype: bool
        :return: Returns True on success, False otherwise

        ::

        """

        response = self._delete(
            url='{0}monitors/{1}'.format(self.URL, id),
            headers=self.headers,
            get_raw_response=True
        )

        if response.ok:
            return True
        else:
            return False