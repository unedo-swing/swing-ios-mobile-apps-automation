class AdditionalItemsPageLocators:
        header_page_title = '//*[@label="Additional items"]'
        button_back_page = '//*[@label="Additional items"]/preceding-sibling::XCUIElementTypeButton[1]'

        button_add_additional_items = '//*[contains(@label,"%s") and following-sibling::XCUIElementTypeButton]/following-sibling::XCUIElementTypeButton[1]'
        button_skip_additional_items = '//*[@label="Skip additional items"]'
        button_plus_additional_items = '(//*[@label="Save items"]/preceding-sibling::*[last()]//XCUIElementTypeImage)[last()]'
        button_minus_additional_items = '(//*[@label="Save items"]/preceding-sibling::*[last()]//XCUIElementTypeImage)[last() - 1]'
        button_save_additional_items = '//*[@label="Save items"]'
        button_confirm_additional_items = '//*[@label="Confirm additional items"]'

        button_edit_additional_items = '//*[contains(@label,"%s")]/following-sibling::*[@label="Edit"][1]'
