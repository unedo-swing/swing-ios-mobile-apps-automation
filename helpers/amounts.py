import re

DASHES = ("−", "–", "—")
AMOUNT = re.compile(r"[+-]?\s*\d[\d.,]*")
AMOUNT_LINE = re.compile(r"^[+-]?\s*\d[\d.,]*$")
TIME = re.compile(r"\b\d{1,2}:\d{2}\b")
CURRENCY = re.compile(r"(Rp\.?|RM|S\$|SGD|MYR|IDR|\$)\s*([+-]?\s*\d[\d.,]*)")


def normalize(value):
    text = str(value or "")
    for dash in DASHES:
        text = text.replace(dash, "-")
    return text


def amount_text(value):
    text = normalize(value)
    for line in text.splitlines():
        stripped = line.strip()
        if AMOUNT_LINE.match(stripped):
            return stripped
    match = AMOUNT.search(TIME.sub("", text))
    return match.group(0).strip() if match else ""


def currency_of(value):
    match = CURRENCY.search(normalize(value))
    return match.group(1).rstrip(".") if match else ""


def in_currency(value, currency):
    """'Rp. 200,000 ≈ RM 47.62' in RM -> '47.62'; '' when that currency is not shown."""
    for match in CURRENCY.finditer(normalize(value)):
        if match.group(1).rstrip(".") == currency:
            return match.group(2)
    return ""


def to_number(value):
    raw = amount_text(value)
    digits = re.sub(r"[^0-9]", "", raw)
    if not digits:
        return 0
    number = int(digits)
    if raw.startswith("-"):
        return -number
    if raw.startswith("+"):
        return number
    return -number if direction(value) == "used" else number


def credit_text(number):
    return f"- {abs(int(number)):,}" if number else ""


def total(values):
    return sum(to_number(value) for value in values)


def direction(value):
    lowered = str(value or "").lower()
    if "earned" in lowered:
        return "earned"
    if "used" in lowered:
        return "used"
    return ""


def booking_code(value):
    match = re.search(r"#([A-Z0-9]+)", str(value or ""))
    return match.group(1) if match else ""


def booking_tag(value):
    code = booking_code(value)
    if code:
        return f"#{code}"
    text = str(value or "").strip()
    if not text or not text.isalnum():
        return text
    return f"#{text}"


def matching(values, code):
    wanted = str(code or "").lstrip("#").upper()
    return [v for v in values if booking_code(v).upper() == wanted]
