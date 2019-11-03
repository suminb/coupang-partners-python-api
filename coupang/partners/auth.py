"""Mostly copied from https://partners.coupang.com/#help/open-api"""

import hashlib
import hmac
import os
import time


def generate_hmac(method, url, access_key, secret_key, encoding="utf-8"):
    path, *query = url.split("?")
    os.environ["TZ"] = "GMT+0"
    datetime = time.strftime("%y%m%d") + "T" + time.strftime("%H%M%S") + "Z"
    message = datetime + method + path + (query[0] if query else "")

    signature = hmac.new(
        bytes(secret_key, encoding), message.encode(encoding), hashlib.sha256
    ).hexdigest()

    return (
        "CEA algorithm=HmacSHA256, "
        f"access-key={access_key}, "
        f"signed-date={datetime}, "
        f"signature={signature}"
    )
