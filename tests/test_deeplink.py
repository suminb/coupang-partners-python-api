import os

import pytest

from coupang.partners.deeplink import create_deeplink


api_keys_not_exist = lambda: not (
    "COUPANG_ACCESS_KEY" in os.environ and "COUPANG_SECRET_KEY" in os.environ
)


@pytest.mark.skipif(
    api_keys_not_exist,
    reason="COUPANG_ACCESS_KEY or COUPANG_SECRET_KEY is/are not provided",
)
def test_create_deeplink():
    urls = [
        "https://www.coupang.com/np/coupangglobal",
    ]
    resp = create_deeplink(urls)
