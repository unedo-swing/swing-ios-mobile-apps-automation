class ChangeBillingPlanLocators:
    label_title = '//*[@name="Change billing plan" and contains(@traits,"Header")]'
    button_back = '//*[contains(@traits,"Header")]/preceding-sibling::XCUIElementTypeButton[1]'

    label_section = '//*[@name="Swing Pass membership"]'

    FIELD_PLAYER_NAME = "Player name"
    FIELD_RENEW_DATE = "Renew date"
    FIELD_MEMBERSHIP_ID = "Membership ID"

    label_by_name = '//*[@name="%s"]'
    value_by_label = label_by_name + '/following-sibling::*[1]'

    label_select_plan = '//*[@name="Select new billing plan"]'

    plan_any = '//*[contains(@name," month") and contains(@name,"Rp.") and not(contains(@name,"for ")) and following-sibling::XCUIElementTypeButton]'
    plan_selected = '//*[contains(@name," month") and contains(@name,"Rp.") and following-sibling::XCUIElementTypeButton[1][@value="1" or contains(@traits,"Selected")]]'
    plan_by_duration = '//*[contains(@name,"%s") and contains(@name,"Rp.") and not(contains(@name,"for ")) and following-sibling::XCUIElementTypeButton]'
    radio_by_duration = plan_by_duration + '/following-sibling::XCUIElementTypeButton[1]'
    badge_current_plan = '//*[@name="Current plan"]'
    plan_current = ('//*[contains(@name,"Current plan") and contains(@name,"Rp.")]'
                    ' | //*[@name="Current plan"]/parent::*')

    label_start_note = '//*[contains(@name,"new billing plan will begin")]'

    checkbox_terms = '//*[contains(@traits,"Link") and contains(@name,"terms")]/../preceding-sibling::XCUIElementTypeSwitch[1]'
    row_terms = checkbox_terms + '/parent::*'
    label_agree = '//*[contains(@name,"I have read and agreed")]'
    link_terms = '//*[contains(@traits,"Link") and contains(@name,"terms")]'

    slider_confirm = '//*[@name="Slide to confirm"]'
    slider_thumb = slider_confirm + '/following-sibling::XCUIElementTypeImage[1]'
