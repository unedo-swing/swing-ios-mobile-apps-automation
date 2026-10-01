from helpers.exceldata import ExcelData


class DrivingRangeTestData(ExcelData):
    SHEET = "Driving Range"
    ALIASES = {"VERIFICATION_METHOD": "METHOD_VERIFICATION"}

    COUNTRY_NAME = "Indonesia"
    PHONE_NUMBER = "82165162549"
    METHOD_VERIFICATION = "whatsapp"
    OTP = ""

    SPORT_TYPE = "Golf"

    SEARCH_KEYWORD = "albatross"
    VENUE = "Albatross Driving Range"

    BOOKING_DATE = "08 September 2026"
    BOOKING_START_TIME = "13:00"
    BOOKING_END_TIME = "14:00"
    BAY_TYPE = "Regular"
    NUMBER_OF_BAYS = "1"
    PLAYER_NAME = "Test Baru"

    PROMO_NAME = ""
    PROMO_CODE = "SWING123"
    PAYMENT_METHOD = "DANA"
    PAYMENT_TYPE = ""
    CARD_NUMBER = ""
    CARD_EXPIRY = ""
    CARD_CVV = ""
    CARD_OTP = ""
    
    TC_NAME = ""
    
    MEMBER_TYPE = "swing-pass"
