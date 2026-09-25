from helpers.exceldata import find_rows

SHEET = "Players"

SHETT_EVENT = "Players Event"


def load_players(tc_id):
    players = []
    for row in find_rows(SHEET, "TC_ID", tc_id):
        label = row.get("PLAYER_LABEL")
        if label in (None, ""):
            continue
        players.append({
            "player_no": int(row.get("PLAYER_NO") or len(players) + 1),
            "add_method": str(row.get("ADD_METHOD") or "search").lower(),
            "player": str(label),
            "search_keyword": str(row.get("SEARCH_KEYWORD") or ""),
            "username": str(row.get("USERNAME") or ""),
            "first_name": str(row.get("FIRST_NAME") or ""),
            "last_name": str(row.get("LAST_NAME") or ""),
            "phone_number": str(row.get("PHONE_NUMBER") or ""),
            "email": str(row.get("EMAIL") or ""),
            "promo_name": str(row.get("PROMO_NAME") or ""),
            "promo_code": str(row.get("PROMO_CODE") or ""),
            "add_ons_name": str(row.get("ADD_ONS_NAME") or ""),
            "add_ons_qty": int(row.get("ADD_ONS_QTY") or 1),
            "country_name": str(row.get("COUNTRY_NAME") or ""),
            "verification_method": str(row.get("VERIFICATION_METHOD") or ""),
            "udid": str(row.get("DEVICE_UDID") or ""),
            "device_name": str(row.get("DEVICE_NAME") or ""),
            "platform_version": str(row.get("PLATFORM_VERSION") or ""),
            "wda_port": int(row.get("WDA_PORT") or 0),
        })
    return sorted(players, key=lambda player: player["player_no"])

def load_players_event(tc_id):
    players = []
    for row in find_rows(SHETT_EVENT, "TC_ID", tc_id):
        label = row.get("PLAYER_NAME")
        if label in (None, ""):
            continue
        players.append({
            "package_type": str(row.get("PACKAGE_TYPE") or ""),
            "player_name": str(row.get("PLAYER_NAME") or ""),
            "promo_name": str(row.get("PROMO_NAME") or ""),
            "promo_code": str(row.get("PROMO_CODE") or ""),
            "player_details": str(row.get("PLAYER_DETAILS") or "") 
            
        })
    return sorted(players, key=lambda player: player["player_no"])
