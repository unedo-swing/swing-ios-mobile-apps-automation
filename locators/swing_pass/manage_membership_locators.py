class ManageMembershipLocators:
    ROW_BILLING_HISTORY = "See billing history"
    ROW_CHANGE_PLAN = "Change billing plan"
    ROW_CHANGE_METHOD = "Change billing method"
    ROW_CONTACT_SUPPORT = "Contact Swing Support"
    ROW_CANCEL_MEMBERSHIP = "Cancel Swing Pass membership"

    row_by_label = '//*[@name="%s"]'
    row_billing_history = row_by_label % ROW_BILLING_HISTORY
    row_change_plan = row_by_label % ROW_CHANGE_PLAN
    row_change_method = row_by_label % ROW_CHANGE_METHOD
    row_contact_support = row_by_label % ROW_CONTACT_SUPPORT
    row_cancel_membership = row_by_label % ROW_CANCEL_MEMBERSHIP

    button_close = '//XCUIElementTypeButton[not(@name) or @name=""]'
    scrim = '//*[@name="Scrim"]'
