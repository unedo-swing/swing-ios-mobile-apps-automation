class BottomsheetAddPlayer :
    title_bottomsheet = '//*[@label="Add a player" or @label="Invite a player"]'
    button_close = '//*[@label="Add a player"]/following-sibling::XCUIElementTypeButton[1]'
    button_tab_search_friend = '//*[contains(@label,"Search a friend")]'
    button_tab_add_manually = '//*[contains(@label,"Add manually")]'
    input_search_friend_name = '//*[starts-with(@label,"Search your friend")]/following-sibling::XCUIElementTypeTextField[1]'
    button_option_player_name_static = '//*[contains(@label,"search result")]'
    button_option_player_name_dynamic = '//*[contains(@label,"%s")]'
    button_close_bottomsheet_switch_to_group_registration = '//*[@label="Switch to group registration"]/following-sibling::XCUIElementTypeButton[1]'
