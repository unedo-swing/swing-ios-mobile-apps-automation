class BillingHistoryLocators:
    label_title = '//*[@name="Billing History" and contains(@traits,"Header")]'
    button_back = '//*[contains(@traits,"Header")]/preceding-sibling::XCUIElementTypeButton[1]'

    entry_any = '//*[(self::XCUIElementTypeOther or self::XCUIElementTypeButton) and contains(@name,"Rp.")]'
    entry_at = '(' + entry_any + ')[%d]'
    entry_by_text = '//*[(self::XCUIElementTypeOther or self::XCUIElementTypeButton) and contains(@name,"%s")]'
