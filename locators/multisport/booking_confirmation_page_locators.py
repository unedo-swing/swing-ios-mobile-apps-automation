class BookingConfirmationPageLocators:
    header_booking_confirmation_page = '//*[@label="Booking Confirmation"]'
    button_back_from_booking_page = '//*[@label="Booking Confirmation"]/preceding-sibling::XCUIElementTypeButton[1]'

    button_edit_schedule = '//*[@label="Edit"]'
    button_add_player = '//*[@label="Add a player" or contains(@label,"more players")]'
    button_delete_player = '(//*[@label="Players"]/following-sibling::*//XCUIElementTypeImage)[%i]'
    text_all_player_total = '//*[@label="Players"]/following-sibling::*[1]/*/*'
    button_select_payment = '//*[@label="Select payment"]'

    button_pay_now = '//*[@label="Pay now"]'
