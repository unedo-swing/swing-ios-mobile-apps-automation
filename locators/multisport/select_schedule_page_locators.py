class SelectSchedulePageLocators:
    header_select_schedule_page = '//*[@label="Select your schedule"]'
    button_back_from_select_schedule_page = '//*[@label="Select your schedule"]/preceding-sibling::XCUIElementTypeButton[1]'
    button_calendar = '//*[@label="Select your schedule"]/following-sibling::*[1]'

    text_there_is_no_schedule = '//*[@label="Unfortunately, there are no more available time slots on this date"]'
    button_go_to_next_day = '//*[@label="Go to the next day"]'
    button_pick_date = '//*[@label="%s"]'
    button_choose_schedule = '(//*[starts-with(@name,"%s") and contains(@name,"%s") and not(contains(@name,"not_available")) and not(contains(@label,"Booked"))])[%i]'
    button_confirm_schedule = '//*[@label="Confirm Schedules"]'
    text_total_price = '//*[@label="Confirm Schedules"]/preceding-sibling::*[contains(@label,"schedules selected")]'
