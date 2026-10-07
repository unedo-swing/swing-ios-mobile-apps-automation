class CancelSwingPassLocators:
    label_title = '//*[@name="Cancel Swing Pass" and contains(@traits,"Header")]'
    button_back = '//*[contains(@traits,"Header")]/preceding-sibling::XCUIElementTypeButton[1]'

    label_section = '//*[@name="Swing Pass membership"]'

    FIELD_PLAYER_NAME = "Player Name"
    FIELD_CANCEL_DATE = "Cancel Date"
    FIELD_ENDS_ON = "Ends on"
    FIELD_MEMBERSHIP_ID = "Membership ID"

    label_by_name = '//*[@name="%s"]'
    value_by_label = label_by_name + '/following-sibling::*[1]'

    label_reason_section = '//*[@name="Cancellation reason"]'
    label_reason_hint = '//*[contains(@name,"please share with us why")]'

    REASON_NO_VALUE = "much value in the benefits"
    REASON_TOO_EXPENSIVE = "too expensive"
    REASON_CANNOT_USE_UP = "struggling to use up"
    REASON_DIDNT_KNOW_AUTORENEW = "know it auto-renews"
    REASON_RARELY_USED = "using Swing that often"
    REASON_OTHER_PROVIDER = "another plan or membership"
    REASON_NO_PERKS = "perks available"

    reason_any = ('//*[contains(@traits,"Button") and (contains(@name,"value in the benefits")'
                  ' or contains(@name,"too expensive") or contains(@name,"use up")'
                  ' or contains(@name,"auto-renews") or contains(@name,"that often")'
                  ' or contains(@name,"another plan") or contains(@name,"perks available"))]')
    reason_by_text = '//*[contains(@traits,"Button") and contains(@name,"%s")]'
    reason_selected = '//*[contains(@traits,"Button") and (@value="1" or contains(@traits,"Selected")) and not(contains(@name,"Tab "))]'

    button_cancel_membership = '//*[@name="Cancel membership"]'
