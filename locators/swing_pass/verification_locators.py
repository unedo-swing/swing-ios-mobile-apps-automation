class VerificationLocators:
    label_title = '//*[@name="Swing Pass verification" and contains(@traits,"Header")]'
    button_back = '//*[contains(@traits,"Header")]/preceding-sibling::XCUIElementTypeButton[1]'

    label_headline = '//*[contains(@name,"waiting for your verification")]'
    label_description = '//*[contains(@name,"complete verification to start using it")]'

    label_full_name = '//*[contains(@name,"Full name as on your identification")]'
    input_full_name = '//XCUIElementTypeTextField'

    section_photo = '//*[starts-with(@name,"Take a picture of yourself")]'
    button_open_camera = '//*[@name="Open camera"]'

    button_submit = '//*[@name="Submit verification"]'
