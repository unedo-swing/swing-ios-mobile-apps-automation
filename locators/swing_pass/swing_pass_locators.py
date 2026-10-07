class SwingPassLocators:
    label_title = '//*[@name="Swing Pass" and contains(@traits,"Header")]'
    button_back = '//*[contains(@traits,"Header")]/preceding-sibling::XCUIElementTypeButton[1]'
    button_region = '//*[@name="Swing Pass" and contains(@traits,"Header")]/following-sibling::XCUIElementTypeImage[1]'
    button_region_by_code = '//XCUIElementTypeImage[@name="%s"]'

    card_membership = '//*[contains(@name,"Active until")]'
    card_membership_inactive = '//*[contains(@name,"Inactive")]'
    card_membership_waiting = '//*[contains(@name,"Waiting for verification")]'
    card_membership_any = ('//*[contains(@name,"Active until")'
                           ' or contains(@name,"Inactive")'
                           ' or contains(@name,"Waiting for verification")]')
    label_beta = '//*[@name="BETA"]'
    button_enlarge_card = '//*[@name="Enlarge card"]'

    label_verification_submitted = '//*[@name="Verification submitted!"]'
    label_verification_note = '//*[contains(@name,"will be verified within")]'
    button_ok_got_it = '//*[@name="Ok, got it!"]'
    button_contact_support = '//*[@name="Contact Swing Support"]'

    label_tagline = '//*[@name="The one true ultimate golf membership"]'
    label_subscribe_info = '//*[contains(@name,"Subscribe to Swing pass")]'
    button_join = '//*[@name="Join Swing Pass" and not(contains(@traits,"Header"))]'

    card_savings = '//*[contains(@name," saved")]'

    card_comparison = '//*[contains(@name,"Without Swing Pass")]'
    button_see_earnings = '//*[contains(@name,"more with Swing Pass since")]'

    button_manage = '//*[@name="Manage"]'
    card_billing = '//XCUIElementTypeImage[following-sibling::XCUIElementTypeButton[@name="Manage"]]'
    label_renews_on = '//*[contains(@name,"Renews on")]'
    label_ends_on = '//*[contains(@name,"Ends on")]'
    label_plan_updated = '//*[contains(@name,"updated your plan")]'

    label_cancellation_notice = '//*[contains(@name,"auto renewed")]'
    label_renew_prompt = '//*[contains(@name,"Keep your membership active")]'
    button_renew = '//*[@name="Renew"]'

    label_promos_section = '//*[contains(@name,"Exclusive promos")]'
    promo_any = '//XCUIElementTypeOther[@name and following-sibling::XCUIElementTypeImage[@name="Driving Range" or @name="Tee Time" or @name="Tee time"]]'
    promo_by_code = '//XCUIElementTypeOther[starts-with(@name,"%s")]'
    promo_category_by_code = promo_by_code + '/following-sibling::XCUIElementTypeImage[1]'

    benefit_by_title = '//*[starts-with(@name,"%s")]'
    button_see_all_cashbacks = '//*[@name="See all cashbacks"]'
    benefit_any = button_see_all_cashbacks + '/preceding-sibling::XCUIElementTypeOther[1]//XCUIElementTypeImage[@name]'

    label_faq_section = '//*[@name="FAQs about Swing Pass"]'
    faq_any = label_faq_section + '/following-sibling::XCUIElementTypeOther[1]//XCUIElementTypeImage[@name]'
    faq_by_question = '//*[starts-with(@name,"%s")]'

    label_other_questions = '//*[contains(@name,"Have any other questions")]'
    button_contact_us = '//*[@name="Contact us here."]'
