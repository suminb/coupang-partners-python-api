from coupang.partners.deeplink import create_deeplink


def test_create_deeplink():
    urls = [
        "https://www.coupang.com/np/coupangglobal",
    ]
    resp = create_deeplink(urls)
