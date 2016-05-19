from newrelic_api.base import Resource

class Synthetics(Resource):
    """
    A base class for Synthetics API resources
    """
    URL = 'https://synthetics.newrelic.com/synthetics/api/v1/'