import json
import os

import requests

from coupang.partners.auth import generate_hmac

# Replace with your own ACCESS_KEY and SECRET_KEY
ACCESS_KEY = os.environ["CHEAPMIND_ACCESS_KEY"]
SECRET_KEY = os.environ["CHEAPMIND_SECRET_KEY"]

BASE_URL = "https://api-gateway.coupang.com"
PATH = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"


# TODO: Move this to upper level
class APIResponse:

    def __init__(self, json_response):
        self.response_code = json_response["rCode"]
        self.response_message = json_response["rMessage"]
        self.data = json_response["data"]


class Products(APIResponse):

    def __init__(self, json_response):
        super(Products, self).__init__(json_response)
        self.landing_url = self.data["landingUrl"]
        self.records = [Product(r) for r in self.data["productData"]]


class Product:
    """Represents a single product.

    Raw data example:

        {
            "productId": 210191841,
            "productName": "Apple 에어팟 2세대 유선 충전 모델, MV7N2KH/A",
            "productPrice": 159000,
            "productImage": "https://static.coupangcdn.com/image/product/image/vendoritem/2019/09/02/4643936599/1d600ddf-f0ca-4f91-b62e-d1d86797451d.jpg",
            "productUrl": "https://landing.coupang.com/multi?src=1139000&spec=10799999&addtag=404&ctag=210191841&lptag=AF8304531&pt=PRODUCT&productId=210191841&traceId=19110315194302416001007864&itemId=625998234&vendorItemId=4643936599&gfrom=searchapi",
            "keyword": "apple",
            "rank": 1,
            "isRocket": true
        }
    """
    def __init__(self, json_response):
        self.id = json_response["productId"]
        self.name = json_response["productName"]
        self.price = json_response["productPrice"]
        self.image = json_response["productImage"]
        self.url = json_response["productUrl"]

        # Transient properties
        self.keyword = json_response["keyword"]
        self.rank = json_response["rank"]
        self.rocket_delivery = json_response["isRocket"]


def search(keyword, limit=20):
    """
    """
    # FIXME: URL encoding for non-ASCII characters? (keyword)
    # NOTE: Query string must be included in the path, otherwise HMAC signature
    # will not be valid.
    path = "/v2/providers/affiliate_open_api/apis/openapi/products/search" \
        f"?keyword={keyword}&limit={limit}"
    url = BASE_URL + path
    authorization = generate_hmac('GET', path, ACCESS_KEY, SECRET_KEY)
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json",
    }
    resp = requests.get(url, headers=headers)
    return Products(json.loads(resp.text))
