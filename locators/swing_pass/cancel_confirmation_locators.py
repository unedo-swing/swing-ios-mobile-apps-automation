class CancelConfirmationLocators:
    label_title = '//*[contains(@name,"Are you sure you want to cancel")]'
    label_warning = '//*[contains(@name,"exclusive rates and benefits anymore")]'

    button_stay = '//*[@name="Stay with Swing Pass"]'
    button_proceed = '//*[@name="Proceed to cancel"]'
    button_close = '//XCUIElementTypeButton[not(@name) or @name=""]'
    scrim = '//*[@name="Scrim"]'
