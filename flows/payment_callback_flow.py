import json
import os

from flows.base_flow import BaseFlow
from helpers.checks import CheckTable
from helpers.db_queries import booking_payments

EXISTING_BUSINESS_ID = "5f0401bcf8cc8d13feb11bb2"


def business_ids(value, found=None):
    found = set() if found is None else found
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "business_id":
                found.add(str(item))
            business_ids(item, found)
    elif isinstance(value, list):
        for item in value:
            business_ids(item, found)
    return found


class PaymentCallbackFlow(BaseFlow):
    FLOW_NAME = "PaymentCallbackFlow"

    def verify_existing_payment_callback(self, booking_code, status="PAID", business_id=None):
        expected = business_id or os.getenv("XENDIT_EXISTING_BUSINESS_ID", EXISTING_BUSINESS_ID)
        payments = booking_payments(booking_code, status)
        text = json.dumps(payments, indent=2, default=str, ensure_ascii=False)
        print(f"\npayment callback {booking_code}:\n{text}")
        self.reporter.note(f"Payment callback {booking_code}:\n{text}", evidence=True)
        table = CheckTable(f"Payment callback {booking_code}")
        latest = payments[0]["status"] if payments else "no payment row"
        table.add("Payment status", status, latest, latest == status)
        for index, payment in enumerate(payments, start=1):
            found = business_ids(payment["callback"])
            table.add(f"Callback {index} business_id", f"{expected} or not present",
                      ", ".join(sorted(found)) or "not present", found <= {expected})
        table.verify()
