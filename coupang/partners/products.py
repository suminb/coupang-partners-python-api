import json
import os

import requests

from coupang.partners import BASE_URL
from coupang.partners.auth import generate_hmac

# Replace with your own ACCESS_KEY and SECRET_KEY
ACCESS_KEY = os.environ["CHEAPMIND_ACCESS_KEY"]
SECRET_KEY = os.environ["CHEAPMIND_SECRET_KEY"]


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
    """Sends a search request."""

    # FIXME: URL encoding for non-ASCII characters? (keyword)
    # NOTE: Query string must be included in the path, otherwise HMAC signature
    # will not be valid.
    path = (
        "/v2/providers/affiliate_open_api/apis/openapi/products/search"
        f"?keyword={keyword}&limit={limit}"
    )
    url = BASE_URL + path
    authorization = generate_hmac("GET", path, ACCESS_KEY, SECRET_KEY)
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json",
    }
    resp = requests.get(url, headers=headers)
    return Products(json.loads(resp.text))


def products_by_category(category_id, limit=50):
    """
    {
        "productId": 297564896,
        "productName": "온스타일러 블랙핑크 후드 롱원피스 가을원피스 캐주얼 원피스 후드원피스 무지원피스",
        "productPrice": 14450,
        "productImage": "https://static.coupangcdn.com/image/vendor_inventory/26d7/30fe73751e802399363357df3e92992fbcc7ea7268044910ee31af4aa24f.jpg",
        "productUrl": "https://landing.coupang.com/multi?src=1139000&spec=10799999&addtag=404&ctag=297564896&lptag=AF8304531&pt=PRODUCT&productId=297564896&traceId=19110322240980012001004814&itemId=937345786&vendorItemId=5321055944&gfrom=bestapi",
        "categoryName": "여성패션",
        "keyword": "여성패션",
        "rank": 1,
        "isRocket": false
    }
    """
    path = f"/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/{category_id}?limit={limit}"
    url = BASE_URL + path
    authorization = generate_hmac("GET", path, ACCESS_KEY, SECRET_KEY)
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json",
    }
    resp = requests.get(url, headers=headers)
    # TODO: Handle category
    return Products(json.loads(resp.text))