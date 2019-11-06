import json

import requests

from coupang.partners import ACCESS_KEY, BASE_URL, SECRET_KEY
from coupang.partners import APIResponse
from coupang.partners.auth import generate_hmac


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
    return APIResponse(json.loads(resp.text))
