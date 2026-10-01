from helpers.db_client import DbClient

BOOKING_PAYMENT_CALLBACKS = """
    select booking_payment.callback
    from booking_payment
    join booking on booking.id = booking_payment.booking_id
"""


def booking_payment_callbacks(db=None):
    db = db or DbClient.from_env()
    return [row["callback"] for row in db.query(BOOKING_PAYMENT_CALLBACKS)] # pyright: ignore[reportGeneralTypeIssues]
