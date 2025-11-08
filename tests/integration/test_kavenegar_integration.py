import os
import pytest
import json
from kavenegar import KavenegarAPI, HTTPException, APIException

# ------------------------
# Helper fixture
# ------------------------
@pytest.fixture
def api():
    api_key = os.getenv("KAVENEGAR_API_KEY")
    if not api_key:
        pytest.skip("KAVENEGAR_API_KEY not set, skipping integration tests")
    return KavenegarAPI(apikey=api_key)


# ------------------------
# 1️⃣ verify_lookup test
# ------------------------
@pytest.mark.integration
def test_verify_lookup(api):
    receptor = os.getenv("KAVENEGAR_TEST_PHONE")
    template = os.getenv("KAVENEGAR_TEMPLATE_NAME")
    if not receptor:
        pytest.skip("KAVENEGAR_TEST_PHONE not set, skipping verify_lookup test")

    params = {
        "receptor": receptor,
        "token": "1234",        # Test token
        "template": template    # Must match a template in your Kavenegar panel
    }

    try:
        result = api.verify_lookup(params)
        assert result is not None
        print("✅ verify_lookup result:", result)
    except (APIException, HTTPException) as e:
        pytest.fail(f"verify_lookup failed: {e}")


# ------------------------
# 2️⃣ sms_send test
# ------------------------
@pytest.mark.integration
def test_sms_send(api):
    receptor = os.getenv("KAVENEGAR_TEST_PHONE")
    if not receptor:
        pytest.skip("KAVENEGAR_TEST_PHONE not set, skipping sms_send test")

    params = {
        "receptor": receptor,
        "message": "تست ارسال پیام 🚀"
    }

    try:
        result = api.sms_send(params)
        assert result is not None
        print("✅ sms_send result:", result)
    except (APIException, HTTPException) as e:
        pytest.fail(f"sms_send failed: {e}")


# ------------------------
# 3️⃣ sms_sendarray test
# ------------------------
@pytest.mark.integration
def test_sms_sendarray(api):
    receptor = os.getenv("KAVENEGAR_TEST_PHONE")
    sender = os.getenv("KAVENEGAR_SENDER_LINE_NUMBER")
    if not receptor:
        pytest.skip("KAVENEGAR_TEST_PHONE not set, skipping sms_sendarray test")

    params = {
        "sender": json.dumps([sender, sender]),
        "receptor": json.dumps([receptor, receptor]),
        "message": json.dumps(["تست ارسال پیام 1 🚀", "تست ارسال پیام 2 🚀"])
    }

    try:
        result = api.sms_sendarray(params)
        assert result is not None
        print("✅ sms_sendarray result:", result)
    except (APIException, HTTPException) as e:
        pytest.fail(f"sms_sendarray failed: {e}")
