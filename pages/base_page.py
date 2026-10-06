from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException

from config.settings import settings
from helpers import alerts, device, gestures, keyboard, media, waits
from helpers.logger import get_logger
from helpers.reporter import reporter
from locators.base_locator import to_tuple

DAY_MINUTES = 24 * 60


def clock_minutes(value):
    hours, _, minutes = str(value).strip().replace(".", ":").partition(":")
    return int(hours) * 60 + int(minutes or 0)


def clock_text(minutes):
    return f"{(minutes // 60) % 24:02d}:{minutes % 60:02d}"


def line_after(text, label):
    lines = [line.strip() for line in str(text or "").splitlines()]
    return lines[lines.index(label) + 1] if label in lines and lines[-1] != label else ""


def item_pair(item, name_key, quantity_key):
    if isinstance(item, dict):
        return item[name_key], item[quantity_key]
    return item[0], item[1]


class BasePage:
    ROOT_LOCATOR = None
    PAGE_NAME = "BasePage"
    WHEEL_SETTLE = 0.3

    def __init__(self, driver):
        self.driver = driver
        self.timeout = settings.EXPLICIT_WAIT
        self.log = get_logger(self.__class__.__name__)

    def find(self, locator, timeout=None):
        return waits.wait_present(self.driver, locator, timeout or self.timeout)

    def find_visible(self, locator, timeout=None):
        return waits.wait_visible(self.driver, locator, timeout or self.timeout)

    def find_clickable(self, locator, timeout=None):
        return waits.wait_clickable(self.driver, locator, timeout or self.timeout)

    def find_all(self, locator, timeout=None):
        try:
            return waits.wait_all_visible(self.driver, locator, timeout or self.timeout)
        except TimeoutException:
            return []

    def find_all_present(self, locator):
        return self.driver.find_elements(*to_tuple(locator))

    def count(self, locator):
        return len(self.find_all_present(locator))

    def visible_count(self, locator, timeout=5):
        value = len(self.find_all(locator, timeout))
        reporter.read("visible count", locator, value)
        return value

    def click(self, locator, timeout=None):
        reporter.action("click", locator)
        self.bring_into_view(locator)
        waits.retry(self.find_clickable(locator, timeout).click)
        return self

    def click_times(self, locator, times, timeout=None):
        count = max(0, int(times))
        reporter.action("click", locator, f"x{count}")
        for _ in range(count):
            waits.retry(self.find_clickable(locator, timeout).click)
        return self

    def step_to(self, target, current, increase, decrease, timeout=None):
        delta = int(target) - int(current)
        return self.click_times(increase if delta > 0 else decrease, abs(delta), timeout)

    def set_quantities(self, items, value_template, increase_template, decrease_template,
                       name_key="add_ons_name", quantity_key="add_ons_qty"):
        for item in items or []:
            name, quantity = item_pair(item, name_key, quantity_key)
            self.step_to(quantity, self.quantity_of(value_template.format(name)),
                         increase_template.format(name), decrease_template.format(name))
        return self

    def click_each(self, template, values):
        for value in values:
            self.scroll_and_click(template.format(value))
        return self

    def tap_each(self, template, values):
        for value in values:
            self.scroll_and_tap(template.format(value))
        return self

    def click_element(self, element):
        waits.retry(element.click)
        return self

    def tap(self, locator, timeout=None):
        reporter.action("tap", locator)
        self.bring_into_view(locator)
        gestures.tap_element(self.driver, self.find(locator, timeout))
        return self

    def tap_at(self, x, y):
        gestures.tap(self.driver, x, y)
        return self

    def double_tap(self, locator):
        reporter.action("double tap", locator)
        gestures.double_tap(self.driver, self.find_visible(locator))
        return self

    def tap_row_in(self, locator, text, header_lines=1, lines_per_row=3, x_ratio=0.5, timeout=None):
        element = self.find_visible(locator, timeout)
        lines = (element.get_attribute("label") or element.text or "").split("\n")
        rows = max((len(lines) - header_lines) // lines_per_row, 1)
        row = next((index for index in range(rows)
                    if any(text in line for line in
                           lines[header_lines + index * lines_per_row:header_lines + (index + 1) * lines_per_row])), 0)
        rect = element.rect
        x = int(rect["x"] + rect["width"] * x_ratio)
        y = int(rect["y"] + rect["height"] * (row + 1.5) / (rows + 1))
        reporter.action("tap row", locator, f"{text} = row {row + 1} of {rows} at {x},{y}")
        gestures.tap(self.driver, x, y)
        return self

    def double_tap_center(self):
        width, height = gestures.screen_size(self.driver)
        reporter.action("double tap", "screen center", f"{width // 2},{height // 2}")
        gestures.double_tap(self.driver, x=width // 2, y=height // 2)
        return self

    def long_press(self, locator, duration=2.0):
        reporter.action("long press", locator)
        gestures.long_press(self.driver, self.find_visible(locator), duration=duration)
        return self

    def type(self, locator, text, clear=True, hide_keyboard=False, timeout=None, mask=False,
             dismiss_with=None):
        reporter.action("type", locator, "***" if mask else text)
        self.find_visible(locator, timeout).click()
        for attempt in range(2):
            try:
                element = self.find_visible(locator, timeout)
                if clear:
                    keyboard.clear_field(self.driver, element)
                element.send_keys(str(text))
                break
            except StaleElementReferenceException:
                if attempt:
                    raise
                self.log.info(f"field was redrawn after the tap, finding it again: {locator}")
        if hide_keyboard:
            keyboard.hide(self.driver, outside=dismiss_with)
        return self

    def clear(self, locator):
        reporter.action("clear", locator)
        keyboard.clear_field(self.driver, self.find_visible(locator))
        return self

    def text_of(self, locator, timeout=None):
        element = self.find_visible(locator, timeout)
        value = element.text or element.get_attribute("value") or element.get_attribute("label")
        reporter.read("text of", locator, value)
        return value

    def value_of(self, locator, timeout=None):
        value = self.find(locator, timeout).get_attribute("value")
        reporter.read("value of", locator, value)
        return value

    def label_of(self, locator, timeout=None):
        try:
            value = self.find(locator, timeout).get_attribute("label")
        except TimeoutException:
            value = ""
        reporter.read("label of", locator, value)
        return value

    def minutes_between(self, start, end):
        span = clock_minutes(end) - clock_minutes(start)
        return span if span >= 0 else span + DAY_MINUTES

    def time_slots(self, start, end=None, step=60):
        first = clock_minutes(start)
        last = first if end is None else clock_minutes(end)
        if last < first:
            raise ValueError(f"end time {end} is before start time {start}")
        return [clock_text(first + offset) for offset in range(0, last - first + 1, step)]

    def duration_between(self, start, end=None, step=60):
        minutes = len(self.time_slots(start, end, step)) * step
        value = f"{minutes} minute" if minutes == 1 else f"{minutes} minutes"
        reporter.read("duration between", f"{start} - {end or start}", value)
        return value

    def quantity_of(self, locator, timeout=None):
        text = self.find(locator, timeout).get_attribute("label") or ""
        digits = [line.strip() for line in text.splitlines() if line.strip().isdigit()]
        value = int(digits[-1]) if digits else 0
        reporter.read("quantity of", locator, value)
        return value

    def value_after_line(self, locator, label, timeout=None):
        value = line_after(self.find(locator, timeout).get_attribute("label"), label)
        reporter.read(f"value after {label} of", locator, value)
        return value

    def values_after_line(self, locator, label):
        values = [line_after(text, label) for text in self.texts_of(locator)]
        reporter.read(f"values after {label} of", locator, values)
        return values

    def value_after_label(self, locator, timeout=None):
        text = self.find(locator, timeout).get_attribute("label") or ""
        value = text.split("\n")[-1].strip() if "\n" in text else text.strip()
        reporter.read("value after label of", locator, value)
        return value

    def attribute(self, locator, attribute, timeout=None):
        value = self.find(locator, timeout).get_attribute(attribute)
        reporter.read(f"attribute {attribute} of", locator, value)
        return value

    def texts_of(self, locator):
        return [
            element.text or element.get_attribute("label") or ""
            for element in self.find_all(locator)
        ]

    def is_visible(self, locator, timeout=3, log=True):
        value = waits.is_visible(self.driver, locator, timeout)
        if log:
            reporter.read("is visible", locator, value)
        return value

    def is_present(self, locator, timeout=3):
        return waits.is_present(self.driver, locator, timeout)

    def is_enabled(self, locator, timeout=None):
        value = self.find(locator, timeout).is_enabled()
        reporter.read("is enabled", locator, value)
        return value

    def is_disabled(self, locator, timeout=None):
        value = not self.find(locator, timeout).is_enabled()
        reporter.read("is disabled", locator, value)
        return value

    def is_selected(self, locator, timeout=None):
        return self.find(locator, timeout).get_attribute("value") in ("1", "true", True)

    def set_switch(self, locator, on=True, timeout=None):
        reporter.action("set switch", locator, on)
        element = self.find(locator, timeout)
        if (element.get_attribute("value") in ("1", "true", True)) != bool(on):
            waits.retry(element.click)
        return self

    def wait_gone(self, locator, timeout=None):
        return waits.is_gone(self.driver, locator, timeout or self.timeout)

    def wait_text(self, locator, text, timeout=None):
        waits.wait_text_present(self.driver, locator, text, timeout or self.timeout)
        return self

    def wait_all_visible(self, locators, timeout=None):
        for locator in locators:
            self.find_visible(locator, timeout)
        return self

    def wait_until_loaded(self, timeout=None):
        reporter.note(f"wait for {self.PAGE_NAME}")
        if self.ROOT_LOCATOR is None:
            return self
        self.find_visible(self.ROOT_LOCATOR, timeout)
        return self

    def is_loaded(self, timeout=5):
        if self.ROOT_LOCATOR is None:
            return True
        return self.is_visible(self.ROOT_LOCATOR, timeout)

    def verify_screen(self):
        return self.wait_until_loaded()

    def capture_step(self, name=None, detail=None):
        label = name or self.PAGE_NAME
        caption = f"{label} = {detail}" if detail is not None else label
        if settings.STEP_CAPTURE_SCREENSHOTS:
            reporter.attach(media.screenshot(self.driver, label), caption)
        else:
            reporter.note(caption, evidence=True)
        return self

    def swipe(self, direction="up", element=None):
        gestures.swipe(self.driver, direction, element=element)
        return self

    def element_of(self, target):
        return target if hasattr(target, "id") else self.find(target)

    def find_now(self, locator, visible_only=True):
        for element in self.find_all_present(locator):
            if not visible_only:
                return element
            try:
                if element.is_displayed():
                    return element
            except WebDriverException:
                continue
        return None

    def visible_now(self, locator, timeout=1):
        if not self.find_all_present(locator):
            return None
        try:
            return self.find_visible(locator, timeout)
        except TimeoutException:
            return None

    def swipe_wheel(self, wheel, direction="up"):
        gestures.swipe(self.driver, direction, element=self.element_of(wheel))
        return self

    def wheel_direction(self, value, current, order, default="up"):
        if not order or value not in order or current not in order:
            return default
        return "up" if order.index(value) > order.index(current) else "down"

    def select_in_wheel(self, option, wheel, direction="down", max_swipes=15):
        reporter.action("select in wheel", option)
        for attempt in range(max_swipes + 1):
            if attempt:
                self.swipe_wheel(wheel, direction)
                device.wait_seconds(self.WHEEL_SETTLE)
            element = self.find_now(option) or self.visible_now(option)
            if element is not None:
                print(element)
                print(option)
                waits.retry(element.click)
                device.wait_seconds(self.WHEEL_SETTLE)
                return self
        raise AssertionError(f"{option} not reachable in the wheel after {max_swipes} swipes")

    def swipe_in(self, container, direction="left"):
        gestures.swipe(self.driver, direction, element=self.element_of(container))
        return self

    def swipe_left_in(self, container):
        return self.swipe_in(container, "left")

    def swipe_right_in(self, container):
        return self.swipe_in(container, "right")

    def swipe_to_element_in(self, locator, container, direction="left", max_swipes=5):
        reporter.action(f"swipe {direction} to", locator)
        if self.is_visible(locator, timeout=1, log=False):
            return True
        for attempt in range(max_swipes):
            before = self.driver.page_source
            self.swipe_in(container, direction)
            if self.is_visible(locator, timeout=1, log=False):
                return True
            if self.driver.page_source == before:
                self.log.info(f"{direction} swipe {attempt + 1} changed nothing, end of carousel")
                break
        self.log.info(f"{locator} not reached after {max_swipes} {direction} swipes")
        return False

    def swipe_left_to_element(self, locator, container, max_swipes=5):
        return self.swipe_to_element_in(locator, container, "left", max_swipes)

    def swipe_right_to_element(self, locator, container, max_swipes=5):
        return self.swipe_to_element_in(locator, container, "right", max_swipes)

    def scroll_to(self, locator, direction="up", max_swipes=None, check_timeout=None):
        attempts = settings.MAX_SCROLLS if max_swipes is None else max_swipes
        timeout = settings.SCROLL_CHECK_TIMEOUT if check_timeout is None else check_timeout
        for attempt in range(attempts):
            try:
                element = waits.wait_visible(self.driver, locator, timeout)
                device.wait_seconds(settings.SCROLL_SETTLE)
                return element
            except TimeoutException:
                self.log.info(f"scroll {direction} attempt {attempt + 1}/{attempts} for {locator}")
                gestures.swipe_percent(self.driver, direction)
        element = waits.wait_visible(self.driver, locator, timeout)
        device.wait_seconds(settings.SCROLL_SETTLE)
        return element

    def bring_into_view(self, locator, direction="up", max_swipes=None):
        try:
            return self.scroll_to(locator, direction, max_swipes)
        except (AssertionError, TimeoutException) as exc:
            self.log.warning(f"{locator} never became visible while scrolling: {exc}")
            return None

    def scroll_and_click(self, locator, direction="up", max_swipes=12, timeout=3):
        reporter.action("scroll and click", locator)
        self.bring_into_view(locator, direction, max_swipes)
        waits.retry(self.find_clickable(locator, timeout).click)
        return self

    def scroll_and_tap(self, locator, direction="up", max_swipes=12, timeout=3):
        reporter.action("scroll and tap", locator)
        self.bring_into_view(locator, direction, max_swipes)
        gestures.tap_element(self.driver, self.find(locator, timeout))
        return self

    def pull_to_refresh(self, times=1):
        gestures.pull_to_refresh(self.driver, times)
        return self

    def drag_to(self, source_locator, target_locator):
        gestures.drag_element_to(
            self.driver, self.find_visible(source_locator), self.find_visible(target_locator)
        )
        return self

    def pinch(self, locator=None, scale=0.5):
        element = self.find_visible(locator) if locator else None
        gestures.pinch(self.driver, element, scale)
        return self

    def zoom(self, locator=None, scale=2.0):
        element = self.find_visible(locator) if locator else None
        gestures.zoom(self.driver, element, scale)
        return self

    def accept_alert(self, timeout=3, button_label=None):
        return alerts.accept_if_present(self.driver, timeout, button_label)

    def dismiss_alert(self, timeout=3, button_label=None):
        return alerts.dismiss_if_present(self.driver, timeout, button_label)

    def alert_text(self):
        return alerts.text(self.driver)

    def hide_keyboard(self):
        keyboard.hide(self.driver)
        return self

    def press_enter(self):
        keyboard.tap_return(self.driver)
        return self

    def go_back(self, locator=None):
        if locator is not None and self.is_visible(locator, 3):
            return self.click(locator)
        try:
            self.driver.back()
        except WebDriverException:
            gestures.swipe(self.driver, "right")
        return self

    def screenshot(self, name=None):
        path = media.screenshot(self.driver, name or self.PAGE_NAME)
        reporter.attach(path, name or self.PAGE_NAME)
        return path

    def page_source(self):
        return self.driver.page_source

    def save_source(self, path):
        return device.save_source(self.driver, path)

    def open_page(self, page_class):
        return page_class(self.driver)

    def wait(self, seconds):
        device.wait_seconds(seconds)
        return self
