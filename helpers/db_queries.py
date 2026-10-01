import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config.settings  # noqa: F401,E402  loads the env file, so DB_* is set
from helpers import amounts  # noqa: E402
from helpers.db_client import DbClient, DbError  # noqa: E402


def _db(db=None):
    return db or DbClient.from_env()


def _json(value):
    try:
        return json.loads(value) if isinstance(value, str) else value
    except json.JSONDecodeError:
        return value


def booking_payments(booking_code, status="PAID", timeout=60, db=None):
    code = amounts.booking_code(booking_code) or str(booking_code).strip()
    sql = """
        select booking_payments.status, booking_payments.callback
        from booking_payments
        join bookings on bookings.id = booking_payments.booking_id
        where bookings.invoice_number = %s
        order by booking_payments.created_at desc
    """
    client = _db(db)
    try:
        rows = client.wait_for(sql, [code], until=lambda rows: bool(rows) and rows[0]["status"] == status,
                               timeout=float(timeout))
    except DbError:
        rows = client.query(sql, [code])
    return [{"status": row["status"], "callback": _json(row["callback"])} for row in rows]  # pyright: ignore[reportGeneralTypeIssues]


def run_sql(sql, db=None):
    return _db(db).query(sql)


if __name__ == "__main__":
    name, *args = sys.argv[1:]
    print(json.dumps(globals()[name](*args), indent=2, default=str, ensure_ascii=False))
