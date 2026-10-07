from helpers.exceldata import ExcelData


class MultisportTestData(ExcelData):
    SHEET = "Multisport"

    COUNTRY_NAME = "Indonesia"
    PHONE_NUMBER = "82165162549"
    METHOD_VERIFICATION = "whatsapp"
    OTP = ""
    SPORT_TYPE = "Golf"

    TC_NAME = ""
    SPORT_NAME = ""
    VENUE_NAME = ""
    TITLE_SCHEDULE = ""
    HOW_MUCH_SCHEDULE = 1
    PLAYER_NAME = ""
    PAYMENT_METHOD = ""
    ADDITIONAL_ITEMS = ""

    @classmethod
    def load(cls, tc_id):
        super().load(tc_id)
        cls.HOW_MUCH_SCHEDULE = 1 if cls.HOW_MUCH_SCHEDULE in (None, "") else int(cls.HOW_MUCH_SCHEDULE)
        return cls

    @classmethod
    def items_list(cls):
        if not cls.ADDITIONAL_ITEMS:
            return []
        return [item.strip() for item in str(cls.ADDITIONAL_ITEMS).split(",") if item.strip()]
