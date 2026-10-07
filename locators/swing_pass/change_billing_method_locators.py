class ChangeBillingMethodLocators:
    label_title = '//*[@name="Change billing method" and contains(@traits,"Header")]'
    button_back = '//*[contains(@traits,"Header")]/preceding-sibling::XCUIElementTypeButton[1]'

    label_section = '//*[@name="Swing Pass membership"]'

    FIELD_PLAYER_NAME = "Player name"
    FIELD_RENEW_DATE = "Renew date"
    FIELD_MEMBERSHIP_ID = "Membership ID"

    label_by_name = '//*[@name="%s"]'
    value_by_label = label_by_name + '/following-sibling::*[1]'

    label_select_method = '//*[@name="Select new billing method"]'
    PLACEHOLDER_METHOD = "Select billing method"
    row_method = '//XCUIElementTypeImage[following-sibling::XCUIElementTypeButton[@name="Select" or @name="Change"]]'
    button_select = '//XCUIElementTypeButton[@name="Select" or @name="Change"]'

    checkbox_terms = '//*[contains(@traits,"Link") and contains(@name,"terms")]/../preceding-sibling::XCUIElementTypeSwitch[1]'
    row_terms = checkbox_terms + '/parent::*'
    label_agree = '//*[contains(@name,"I have read and agreed")]'
    link_terms = '//*[contains(@traits,"Link") and contains(@name,"terms")]'

    slider_confirm = '//*[@name="Slide to confirm"]'
    slider_thumb = slider_confirm + '/following-sibling::XCUIElementTypeImage[1]'
