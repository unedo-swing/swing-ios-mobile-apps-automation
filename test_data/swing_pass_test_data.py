from helpers.exceldata import ExcelData

TRUE_WORDS = ("true", "yes", "y", "1", "run")


class SwingPassTestData(ExcelData):
    SHEET = "Swing Pass"

    COUNTRY = "Indonesia"
    PHONE_NUMBER = "82165162549"
    VERIFICATION_METHOD = "whatsapp"
    OTP = ""
    SPORT_TYPE = "Golf"

    TC_NAME = ""
    ACTION = "run"
    PAYMENT_OPTION = ""
    BILLING_PLAN = ""
    NEW_PLAN = ""
    BILLING_METHOD = ""
    CARD_INDEX = 1
    EWALLET = ""
    PROMO_CODE = ""
    CANCEL_REASON = ""
    FULL_NAME = ""
    CONFIRM = True
    EXPECTED_RESULT = ""

    @classmethod
    def load(cls, tc_id):
        super().load(tc_id)
        cls.PHONE_NUMBER = str(cls.PHONE_NUMBER)
        cls.VERIFICATION_METHOD = str(cls.VERIFICATION_METHOD or "whatsapp").strip().lower()
        cls.CARD_INDEX = int(cls.CARD_INDEX or 1)
        cls.CONFIRM = cls.CONFIRM if isinstance(cls.CONFIRM, bool) else str(cls.CONFIRM).strip().lower() in TRUE_WORDS
        return cls
