from pages.base_page import BasePage


class AndroidCompatPage(BasePage):

    CHECKED_VALUES = ("1", "true", True)

    def capture_step(self, name=None, detail=None, data=None):
        return super().capture_step(name, detail if detail not in ("", None) else None)

    def click(self, locator, timeout=None):
        self.bring_into_view(locator)
        return super().click(locator, timeout)

    def find_all(self, locator, timeout=None):
        return self.find_all_present(locator)

    def find_anywhere(self, locator, max_swipes=10):
        element = self.bring_into_view(locator, "up", max_swipes)
        if element is None:
            element = self.bring_into_view(locator, "down", max_swipes)
        return element

    def is_visible_after_scroll(self, locator, timeout=5, log=True):
        if self.find_anywhere(locator) is None:
            return False
        return self.is_visible(locator, timeout, log)

    def scroll_and_find(self, locator):
        if self.is_visible(locator, 3, log=False):
            return self.find(locator)
        element = self.find_anywhere(locator)
        if element is not None:
            return element
        return self.find(locator)

    def text_of_element(self, element):
        return element.get_attribute("label") or element.get_attribute("value") or element.text or ""

    def _desc(self, locator):
        return self.text_of_element(self.scroll_and_find(locator))

    def _optional_desc(self, locator):
        element = self.find_anywhere(locator)
        return self.text_of_element(element) if element is not None else ""

    def is_checked(self, element):
        traits = element.get_attribute("traits") or ""
        return element.get_attribute("value") in self.CHECKED_VALUES or "Selected" in traits

    def slide_to_end(self, track_locator, thumb_locator=None):
        self.scroll_and_find(track_locator)
        thumb = thumb_locator or f"{track_locator}/following-sibling::XCUIElementTypeImage[1]"
        return self.slide_right(thumb, track_locator)

    def fill_verified(self, locator, text, clear=True, retries=2):
        for _ in range(max(1, retries)):
            self.type(locator, text, clear=clear)
            if (self.find(locator).get_attribute("value") or "") == text:
                break
        self.hide_keyboard()

    def scroll_to_element(self, locator, max_swipes=None):
        return self.bring_into_view(locator, "up", max_swipes)

    def type_text(self, locator, text, clear=True):
        return self.type(locator, text, clear=clear)
