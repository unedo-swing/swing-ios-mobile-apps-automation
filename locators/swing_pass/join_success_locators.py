class JoinSuccessLocators:
    label_title = '//*[@name="Membership acquired!"]'
    label_subtitle = '//*[@name="Welcome to Swing Pass"]'

    FIELD_PLAYER_NAME = "Player name"
    FIELD_JOIN_DATE = "Join date"
    FIELD_ENDS_ON = "Ends on"
    FIELD_MEMBERSHIP_ID = "Membership ID"
    FIELD_BILLING_AMOUNT = "Billing amount"
    FIELD_BILLING_METHOD = "Billing method"

    label_by_name = '//*[@name="%s"]'
    value_by_label = label_by_name + '/following-sibling::*[1]'

    label_verification_note = '//*[contains(@name,"complete the verification process")]'
    button_continue_verification = '//*[@name="Continue to verification"]'
