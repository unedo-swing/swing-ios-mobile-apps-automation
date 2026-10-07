class BillingDetailsLocators:
    label_title = '//*[@name="Billing Details" and contains(@traits,"Header")]'
    button_back = '//*[contains(@traits,"Header")]/preceding-sibling::XCUIElementTypeButton[1]'

    label_section = '//*[@name="Swing Pass membership"]'

    FIELD_PLAYER_NAME = "Player name"
    FIELD_MEMBERSHIP_ID = "Membership ID"
    FIELD_BILLING_DURATION = "Billing duration"
    FIELD_JOIN_DATE = "Join date"
    FIELD_RENEWS_ON = "Renews on"
    FIELD_PAYMENT_DATE = "Payment date"
    FIELD_TOTAL = "Total"
    FIELD_PAYMENT_METHOD = "Payment method"

    label_by_name = '//*[@name="%s"]'
    value_by_label = label_by_name + '/following-sibling::*[1]'

    label_helping_hand = '//*[@name="Need a helping hand?"]'
    button_contact_support = '//*[@name="Contact Swing Support"]'

    button_send_receipt = '//*[@name="Send receipt"]'
