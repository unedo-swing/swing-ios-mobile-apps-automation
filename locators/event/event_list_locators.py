class EventListLocators:
    TXT_TITLE = '//XCUIElementTypeStaticText[contains(@name,"Register events")]'
    BTN_BACK = '//XCUIElementTypeOther[XCUIElementTypeOther[XCUIElementTypeScrollView]]/preceding-sibling::XCUIElementTypeButton[1]'
    IMG_SWING_PASS_FILTER = '//XCUIElementTypeImage[@name="Only show Swing Pass partners"]'
    SWITCH_SWING_PASS_FILTER = '//XCUIElementTypeImage[@name="Only show Swing Pass partners"]/following-sibling::XCUIElementTypeSwitch'
    LIST_CARDS = '//XCUIElementTypeOther[@name="product_explore_card_final_price"]'
    EL_CARD_BY_TEXT = '//XCUIElementTypeOther[@name="product_explore_card_final_price" and contains(@label,"{}")]'
    IMG_SAVE_BADGE = '//XCUIElementTypeImage[@name="product_explore_card_save_badge"]'
