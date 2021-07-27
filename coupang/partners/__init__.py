import os


__version__ = "0.1.0"

BASE_URL = "https://api-gateway.coupang.com"
ACCESS_KEY = os.environ.get("COUPANG_ACCESS_KEY")
SECRET_KEY = os.environ.get("COUPANG_SECRET_KEY")


class APIException(Exception):
    pass


class APIResponse:
    def __init__(self, json_response):
        self.response_code = int(json_response["rCode"])
        self.response_message = json_response["rMessage"]
        if self.response_code != 0:
            raise APIException(self.response_message)
        self.data = json_response["data"]
