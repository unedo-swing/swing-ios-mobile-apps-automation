from appium.webdriver.common.appiumby import AppiumBy

from helpers.logger import get_logger
from locators.base_locator import to_tuple

log = get_logger("keyboard")


def is_shown(driver):
    return driver.is_keyboard_shown()


def keyboard_top(driver):
    elements = driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeKeyboard")
    if elements:
        return elements[0].rect["y"]
    return int(driver.get_window_size()["height"] * 0.55)


def tap_outside(driver, locator=None):
    if locator is not None:
        driver.find_element(*to_tuple(locator)).click()
        return True
    x = 8
    y = max(int(keyboard_top(driver) * 0.5), 1)
    driver.execute_script("mobile: tap", {"x": x, "y": y})
    return True


def hide(driver, key_name="done", strategy=None, outside=None):
    if not driver.is_keyboard_shown():
        return False
    try:
        driver.execute_script("mobile: hideKeyboard", {"keys": [key_name, "Return"]})
        if not driver.is_keyboard_shown():
            return True
    except Exception as exc:
        log.info(f"no dismiss key on this keyboard: {exc}")
    try:
        if tap_return(driver) and not driver.is_keyboard_shown():
            return True
    except Exception as exc:
        log.info(f"return key not tappable: {exc}")
    try:
        tap_outside(driver, outside)
        if not driver.is_keyboard_shown():
            return True
    except Exception as exc:
        log.warning(f"tap outside failed: {exc}")
    log.warning("keyboard still shown after every dismiss attempt")
    return False


def press_key(driver, key):
    driver.execute_script("mobile: keys", {"keys": [key]})


def press_enter(driver):
    press_key(driver, "\n")


def type_text(driver, text):
    driver.execute_script("mobile: keys", {"keys": list(text)})


def tap_keyboard_key(driver, label):
    driver.find_element(AppiumBy.IOS_PREDICATE, f"name == '{label}'").click()


def tap_return(driver):
    for label in ("Return", "return", "Go", "Done", "Search", "Next", "Send"):
        elements = driver.find_elements(AppiumBy.ACCESSIBILITY_ID, label)
        if elements:
            elements[0].click()
            return label
    return None


def clear_field(driver, element):
    element.clear()
    if element.tag_name == "XCUIElementTypeSecureTextField":
        return
    if element.get_attribute("value"):
        element.click()
        current = element.get_attribute("value") or ""
        driver.execute_script("mobile: keys", {"keys": ["\b"] * len(current)})
