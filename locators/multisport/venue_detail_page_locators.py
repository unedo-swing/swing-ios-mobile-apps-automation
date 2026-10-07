class VenueDetailPageLocators:
    header_venue_details = '//*[@label="Venue details"]'
    button_back_from_venue_details = '//*[@label="Venue details"]/preceding-sibling::XCUIElementTypeButton[1]'

    text_venue_name = '//*[@label="%s"]'
    button_tab_venue_info = '//*[starts-with(@label,"Tab 1")]'
    button_tab_menu_packages = '//*[starts-with(@label,"Tab 2")]'

    button_book_venue = '//*[@label="Book venue"]'
