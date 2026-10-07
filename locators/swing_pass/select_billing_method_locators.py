class SelectBillingMethodLocators:
    label_title = '//*[@name="Select billing method" and contains(@traits,"Header")]'
    button_back = '//*[contains(@traits,"Header")]/preceding-sibling::XCUIElementTypeButton[1]'

    label_credit_cards = '//*[@name="Credit cards"]'
    card_any = ('//XCUIElementTypeImage[starts-with(@name,"VISA") or starts-with(@name,"MASTERCARD")'
                ' or starts-with(@name,"Mastercard") or starts-with(@name,"JCB") or starts-with(@name,"AMEX")]')
    card_at = '(' + card_any + ')[%d]'
    card_by_label = '//*[@name="%s"]'
    button_add_card = '//*[@name="Add credit card"]'

    label_ewallets = '//*[@name="E-wallets"]'
    wallet_any = label_ewallets + '/following-sibling::XCUIElementTypeOther[1]//XCUIElementTypeImage[@name]'
    wallet_by_name = '//XCUIElementTypeImage[starts-with(@name,"%s")]'
    button_connect_by_wallet = wallet_by_name + '/following-sibling::XCUIElementTypeButton[1]'
