from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import time

from config.settings import settings
from helpers.logger import get_logger
from locators.base_locator import to_tuple

log = get_logger("gesture")

DIRECTIONS = ("up", "down", "left", "right")


def _pointer(driver):
    return ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))


def screen_size(driver):
    size = driver.get_window_size()
    return size["width"], size["height"]


def center_of(element):
    rect = element.rect
    if not rect["width"] or not rect["height"]:
        raise AssertionError(
            f"element has no size to tap: {rect}, it is in the tree but not rendered")
    return rect["x"] + rect["width"] // 2, rect["y"] + rect["height"] // 2


def tap(driver, x, y):
    driver.execute_script("mobile: tap", {"x": x, "y": y})


def tap_element(driver, element):
    x, y = center_of(element)
    tap(driver, x, y)


def double_tap(driver, element=None, x=None, y=None):
    params = {}
    if element is not None:
        params["elementId"] = element.id
    else:
        params.update({"x": x, "y": y})
    driver.execute_script("mobile: doubleTap", params)


def long_press(driver, element=None, x=None, y=None, duration=2.0):
    params = {"duration": duration}
    if element is not None:
        params["elementId"] = element.id
    else:
        params.update({"x": x, "y": y}) # type: ignore
    driver.execute_script("mobile: touchAndHold", params)


def drag_coordinates(driver, start_x, start_y, end_x, end_y, duration=1.0):
    driver.execute_script("mobile: dragFromToForDuration", {
        "fromX": int(start_x), "fromY": int(start_y), "toX": int(end_x), "toY": int(end_y), "duration": duration,
    })


def swipe_coordinates(driver, start_x, start_y, end_x, end_y, duration_ms=800):
    actions = _pointer(driver)
    pointer = actions.pointer_action
    pointer.move_to_location(int(start_x), int(start_y))
    pointer.pointer_down()
    pointer.pause(duration_ms / 1000)
    pointer.move_to_location(int(end_x), int(end_y))
    pointer.pointer_up()
    actions.perform()


def swipe(driver, direction="up", percent=None, element=None, velocity=None):
    direction = direction.lower()
    if direction not in DIRECTIONS:
        raise ValueError(f"direction must be one of {DIRECTIONS}")
    share = settings.SWIPE_PERCENT if percent is None else percent
    params = {"direction": direction,
              "velocity": settings.SWIPE_VELOCITY if velocity is None else velocity}
    if element is not None:
        params["elementId"] = element.id
    else:
        width, height = screen_size(driver)
        margin = (1 - share) / 2
        params.update(
            {
                "left": int(width * 0.1),
                "top": int(height * margin),
                "width": int(width * 0.8),
                "height": int(height * share),
            }
        )
    driver.execute_script("mobile: swipe", params)


def scroll(driver, direction="down", element=None, percent=0.8):
    direction = direction.lower()
    if direction not in DIRECTIONS:
        raise ValueError(f"direction must be one of {DIRECTIONS}")
    params = {"direction": direction}
    if element is not None:
        params["elementId"] = element.id
    driver.execute_script("mobile: scroll", params)


def displayed_element(driver, locator):
    for candidate in driver.find_elements(*to_tuple(locator)):
        try:
            if candidate.is_displayed():
                return candidate
        except Exception:
            continue
    return None


def swipe_percent(driver, direction="up", start_pct=None, end_pct=None, duration_ms=None):
    size = driver.get_window_size()
    start = settings.SWIPE_START_PERCENT if start_pct is None else start_pct
    end = settings.SWIPE_END_PERCENT if end_pct is None else end_pct
    if direction.lower() == "down":
        start, end = end, start
    x = size["width"] // 2
    driver.swipe(x, int(size["height"] * start / 100),
                 x, int(size["height"] * end / 100),
                 settings.SWIPE_DURATION_MS if duration_ms is None else duration_ms)


def drag_scroll(driver, direction="up", percent=None, duration=None, hold=0.3):
    direction = direction.lower()
    if direction not in DIRECTIONS:
        raise ValueError(f"direction must be one of {DIRECTIONS}")
    width, height = screen_size(driver)
    share = settings.SWIPE_PERCENT if percent is None else percent
    seconds = settings.SCROLL_DURATION if duration is None else duration
    near = 0.5 - share / 2
    far = 0.5 + share / 2
    if direction in ("up", "down"):
        x = width // 2
        top, bottom = int(height * near), int(height * far)
        start, end = (bottom, top) if direction == "up" else (top, bottom)
        drag_and_drop(driver, x, start, x, end, hold=hold, duration=seconds)
    else:
        y = height // 2
        left, right = int(width * near), int(width * far)
        start, end = (right, left) if direction == "left" else (left, right)
        drag_and_drop(driver, start, y, end, y, hold=hold, duration=seconds)


def scroll_once(driver, direction="up", element=None):
    if element is None and settings.SLOW_SCROLL:
        return drag_scroll(driver, direction)
    return swipe(driver, direction, element=element)


def scroll_to_element(driver, locator, direction="down", max_swipes=12, settle=None):
    pause = settings.SCROLL_SETTLE if settle is None else settle
    for attempt in range(max_swipes + 1):
        element = displayed_element(driver, locator)
        if element is not None:
            return element
        if attempt == max_swipes:
            break
        log.info(f"scroll {direction} attempt {attempt + 1}/{max_swipes} for {locator}")
        scroll_once(driver, direction)
        time.sleep(pause)
    raise AssertionError(f"element not found after {max_swipes} swipes: {locator}")


def scroll_to_visible(driver, element):
    driver.execute_script("mobile: scroll", {"elementId": element.id, "toVisible": True})
    return element


def scroll_to_name(driver, name, direction="down"):
    driver.execute_script("mobile: scroll", {"direction": direction, "name": name})


def scroll_to_predicate(driver, predicate_string, direction="down"):
    driver.execute_script(
        "mobile: scroll", {"direction": direction, "predicateString": predicate_string}
    )


def drag_and_drop(driver, start_x, start_y, end_x, end_y, hold=1.0, duration=1.0):
    driver.execute_script(
        "mobile: dragFromToForDuration",
        {
            "fromX": start_x,
            "fromY": start_y,
            "toX": end_x,
            "toY": end_y,
            "duration": duration,
            "pressDuration": hold,
        },
    )


def drag_element_to(driver, source, target, hold=1.0, duration=1.0):
    sx, sy = center_of(source)
    tx, ty = center_of(target)
    drag_and_drop(driver, sx, sy, tx, ty, hold, duration)


def pinch(driver, element=None, scale=0.5, velocity=-1.0):
    params = {"scale": scale, "velocity": velocity}
    if element is not None:
        params["elementId"] = element.id
    driver.execute_script("mobile: pinch", params)


def zoom(driver, element=None, scale=2.0, velocity=1.0):
    pinch(driver, element, scale, velocity)


def pull_to_refresh(driver, times=1):
    width, height = screen_size(driver)
    for _ in range(times):
        swipe_coordinates(
            driver,
            width // 2,
            int(height * 0.3),
            width // 2,
            int(height * 0.75),
            duration_ms=600,
        )


def swipe_until(driver, condition, direction="up", max_swipes=12):
    for _ in range(max_swipes):
        if condition():
            return True
        swipe(driver, direction)
    return condition()


def select_picker_wheel(driver, element, order="next", offset=0.15):
    driver.execute_script(
        "mobile: selectPickerWheelValue",
        {"elementId": element.id, "order": order, "offset": offset},
    )


def rotate_gesture(driver, element, rotation=3.14, velocity=1.5):
    driver.execute_script(
        "mobile: rotateElement",
        {"elementId": element.id, "rotation": rotation, "velocity": velocity},
    )


def force_touch(driver, element, pressure=1.0, duration=1.0):
    driver.execute_script(
        "mobile: forcePress",
        {"elementId": element.id, "pressure": pressure, "duration": duration},
    )
