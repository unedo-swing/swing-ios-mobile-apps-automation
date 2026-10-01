import json

from flows.base_flow import BaseFlow
from helpers.checks import CheckTable
from helpers.db_queries import booking_payments


def has_key(value, key):
    if isinstance(value, dict):
        return key in value or any(has_key(item, key) for item in value.values())
    if isinstance(value, list):
        return any(has_key(item, key) for item in value)
    return False


class PaymentCallbackFlow(BaseFlow):
    FLOW_NAME = "PaymentCallbackFlow"

    def verify_existing_payment_callback(self, booking_code, status="PAID"):
        payments = booking_payments(booking_code, status)
        text = json.dumps(payments, indent=2, default=str, ensure_ascii=False)
        print(f"\npayment callback {booking_code}:\n{text}")
        self.reporter.note(f"Payment callback {booking_code}:\n{text}", evidence=True)
        table = CheckTable(f"Payment callback {booking_code}")
        latest = payments[0]["status"] if payments else "no payment row"
        table.add("Payment status", status, latest, latest == status)
        for index, payment in enumerate(payments, start=1):
            found = has_key(payment["callback"], "business_id")
            table.add(f"Callback {index} business_id", "not present", "present" if found else "not present", not found)
        table.verify()
