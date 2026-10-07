class PaymentMethodLocators:
    title_header = '//*[@label="Select payment method"]'
    button_back = '//*[@label="Select payment method"]/preceding-sibling::XCUIElementTypeButton[1]'
    button_payment_type = '//*[contains(@label,"%s") and not(contains(@label,"Connect"))]'
