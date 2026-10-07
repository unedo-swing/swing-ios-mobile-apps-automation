from pages.android_compat_page import AndroidCompatPage
from locators.multisport.bottomsheet_add_player import BottomsheetAddPlayer as L
import time


class BottomsheetAddPlayerPage(AndroidCompatPage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.title_bottomsheet, timeout=20), (
            "Add a player bottom sheet not shown"
        )
        self.capture_step("add_player_sheet", "Add a player bottom sheet shown")

    def verify_player_added(self, name: str):
        if self.is_visible(L.button_close_bottomsheet_switch_to_group_registration) :
            self.click(L.button_close_bottomsheet_switch_to_group_registration)
        self.capture_step("add_player_done", f"Player selected: {name}")

    # ================= action steps =================
    def search_friend(self, name: str):
        self.type_text(L.input_search_friend_name, name)
        time.sleep(3)
        self.capture_step("add_player_search", f"Searched friend: {name}")

    def select_player(self, name: str):
        self.tap_row_in(L.button_option_player_name_static, name, x_ratio=0.12)
        self.capture_step("add_player_select", f"Selected player: {name}")
