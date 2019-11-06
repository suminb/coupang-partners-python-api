import json
import os
from urllib.parse import urlencode

import requests

from coupang.partners import ACCESS_KEY, BASE_URL, SECRET_KEY
from coupang.partners import APIResponse
from coupang.partners.auth import generate_hmac


categories = {
    1001: "여성패션",
    1002: "남성패션",
    1003: "베이비패션 (0~3세)",
    1004: "여아패션 (3세 이상)",
    1005: "남아패션 (3세 이상)",
    1006: "스포츠패션",
    1007: "신발",
    1008: "가방/잡화",
    1009: "명품패션",
    1010: "뷰티",
    1011: "출산/유아동",
    1012: "식품",
    1013: "주방용품",
    1014: "생활용품",
    1015: "홈인테리어",
    1016: "가전디지털",
    1017: "스포츠/레저",
    1018: "자동차용품",
    1019: "도서/음반/DVD",
    1020: "완구/취미",
    1021: "문구/오피스",
    1024: "헬스/건강식품",
    1025: "국내여행",
    1026: "해외여행",
    1029: "반려동물용품",
}


class SearchResults(APIResponse):
    def __init__(self, json_response):
        super(SearchResults, self).__init__(json_response)
        self.landing_url = self.data["landingUrl"]
        self.records = [Product(r) for r in self.data["productData"]]


class Products(APIResponse):
    def __init__(self, json_response):
        super(Products, self).__init__(json_response)
        self.records = [Product(r) for r in self.data]


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
        # NOTE: Category name is empty when calling the search API
        self.category = json_response.get("categoryName")
        self.rocket_delivery = json_response["isRocket"]

        # Transient properties
        self.keyword = json_response["keyword"]
        self.rank = json_response["rank"]

    def __repr__(self):
        return f"{self.name} ({self.id})"


def search(keyword, limit=20):
    """Sends a search request."""

    # FIXME: URL encoding for non-ASCII characters? (keyword)
    # NOTE: Query string must be included in the path, otherwise HMAC signature
    # will not be valid.
    params = {"keyword": keyword, "limit": limit}
    path = "/v2/providers/affiliate_open_api/apis/openapi/products/search?" + urlencode(
        params
    )
    url = BASE_URL + path
    authorization = generate_hmac("GET", path, ACCESS_KEY, SECRET_KEY)
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json",
    }
    resp = requests.get(url, headers=headers)
    return SearchResults(json.loads(resp.text))


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
