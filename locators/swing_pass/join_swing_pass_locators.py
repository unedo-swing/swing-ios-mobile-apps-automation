class JoinSwingPassLocators:
    label_title = '//*[@name="Join Swing Pass" and contains(@traits,"Header")]'
    button_back = '//*[contains(@traits,"Header")]/preceding-sibling::XCUIElementTypeButton[1]'

    label_summary = '//*[starts-with(@name,"Rp.") and contains(@name,"for ")]'

    label_select_plan = '//*[@name="Select billing plan"]'

    BADGE_MOST_POPULAR = "MOST POPULAR!"

    plan_any = '//*[contains(@name," month") and contains(@name,"Rp.") and not(contains(@name,"for ")) and following-sibling::XCUIElementTypeButton]'
    plan_selected = '//*[contains(@name," month") and contains(@name,"Rp.") and following-sibling::XCUIElementTypeButton[1][@value="1" or contains(@traits,"Selected")]]'
    plan_by_duration = '//*[contains(@name,"%s") and contains(@name,"Rp.") and not(contains(@name,"for ")) and following-sibling::XCUIElementTypeButton]'
    radio_by_duration = plan_by_duration + '/following-sibling::XCUIElementTypeButton[1]'
    plan_most_popular = ('//*[starts-with(@name,"' + BADGE_MOST_POPULAR + '")'
                         ' and following-sibling::XCUIElementTypeButton]')

    PLACEHOLDER_METHOD = "Select billing method"

    label_select_method = '//XCUIElementTypeStaticText[@name="Select billing method"]'
    row_promo = '//*[@name="Swing Pass promo code" and following-sibling::XCUIElementTypeButton]'
    button_add_promo = row_promo + '/following-sibling::XCUIElementTypeButton[1]'
    row_method = row_promo + '/../following-sibling::XCUIElementTypeOther[1]/*[1]'
    button_select_method = row_promo + '/../following-sibling::XCUIElementTypeOther[1]/XCUIElementTypeButton[1]'

    checkbox_terms = '//*[contains(@traits,"Link") and contains(@name,"terms")]/../preceding-sibling::XCUIElementTypeSwitch[1]'
    row_terms = checkbox_terms + '/parent::*'
    label_agree = '//*[contains(@name,"I have read and agreed")]'
    link_terms = '//*[contains(@traits,"Link") and contains(@name,"terms")]'

    slider_confirm = '//*[@name="Slide to confirm"]'
    slider_thumb = slider_confirm + '/following-sibling::XCUIElementTypeImage[1]'
