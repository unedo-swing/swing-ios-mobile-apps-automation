from helpers.exceldata import ExcelData


class TeeTimeTestData(ExcelData):
    SHEET = "Tee Time"
    ALIASES = {"VERIFICATION_METHOD": "METHOD_VERIFICATION", "GOLF_COURSE": "VENUE",
               "PLAYER_VERIFICATION_METHOD": "PLAYER_METHOD_VERIFICATION"}

    COUNTRY_NAME = "Indonesia"
    PHONE_NUMBER = "82165162549"
    METHOD_VERIFICATION = "whatsapp"
    OTP = ""

    SEARCH_KEYWORD = "rainbow"
    VENUE = "Rainbow Hills Golf"
    BOOKING_DATE = "08 September 2026"
    SESSION = "Morning"
    PREFERRED_TIME = "07:00"
    BOOKING_METHOD = "Standard"
    TOTAL_PLAYERS = "1"
    PAYMENT_METHOD = "DANA"
    PAYMENT_TYPE = ""
    CARD_NUMBER = ""
    CARD_EXPIRY = ""
    CARD_CVV = ""
    CARD_OTP = ""

    TC_NAME = ""
    PLAYER_TYPE = ""
    MEMBER_TYPE = ""
    HOST_NAME = ""
    PROMO_NAME = ""
    PROMO_CODE = ""

    PLAYER_SEARCH = ""
    PLAYER_USERNAME = ""
    PLAYER_NAME = ""
    PLAYER_FIRST_NAME = ""
    PLAYER_LAST_NAME = ""
    PLAYER_PHONE_NUMBER = ""
    PLAYER_COUNTRY_NAME = "Indonesia"
    PLAYER_METHOD_VERIFICATION = "whatsapp"
    PLAYER_OTP = ""
    
    SPORT_TYPE = "Golf"