class PaymentOptionLocators:
    label_title = '//*[contains(@name,"How would you like to pay")]'

    OPTION_RECURRING = "Recurring payment"
    OPTION_ONE_TIME = "One time payment"

    option_any = label_title + '/following-sibling::XCUIElementTypeOther/*[@name and not(@name="Scrim")]'
    option_by_name = '//*[starts-with(@name,"%s")]'
    option_recurring = option_by_name % OPTION_RECURRING
    option_one_time = option_by_name % OPTION_ONE_TIME

    button_manual_transfer = '//*[@name="Or manually transfer to us"]'
    button_continue = button_manual_transfer + '/following-sibling::XCUIElementTypeButton[1]'

    button_close = button_continue
    scrim = '//*[@name="Scrim"]'
