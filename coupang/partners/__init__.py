import os


__version__ = "0.1.0"

BASE_URL = "https://api-gateway.coupang.com"
ACCESS_KEY = os.environ["CHEAPMIND_ACCESS_KEY"]
SECRET_KEY = os.environ["CHEAPMIND_SECRET_KEY"]


class APIResponse:
    def __init__(self, json_response):
        self.response_code = json_response["rCode"]
        self.response_message = json_response["rMessage"]
        self.data = json_response["data"]
