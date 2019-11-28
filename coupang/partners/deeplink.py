import json

import requests

from coupang.partners import ACCESS_KEY, BASE_URL, SECRET_KEY
from coupang.partners import APIResponse
from coupang.partners.auth import generate_hmac


class DeeplinkResponse(APIResponse):
    def __init__(self, json_response):
        super(DeeplinkResponse, self).__init__(json_response)
        self.links = [Deeplink(x) for x in self.data]


class Deeplink:
    def __init__(self, json_data):
        self.data = json_data
        self.plain_url = self.data["originalUrl"]
        self.shortened_url = self.data["shortenUrl"]
        self.landing_url = self.data["landingUrl"]


def create_deeplink(coupang_urls):
    """Creates a deeplink for each URL.

    :param coupang_urls: Coupang URLs. For example,
        [
            "https://www.coupang.com/np/search?component=&q=good&channel=user",
            "https://www.coupang.com/np/coupangglobal",
        ]

    NOTE: It appears new links are generated when subsequent calls are made
    even if identical URLs are provided.
    """
    path = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"
    url = BASE_URL + path
    authorization = generate_hmac("POST", path, ACCESS_KEY, SECRET_KEY)
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json",
    }
    payload = {"coupangUrls": coupang_urls}
    resp = requests.post(url, headers=headers, data=json.dumps(payload))
    return DeeplinkResponse(json.loads(resp.text))
