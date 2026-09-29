from datetime import datetime
import json


def is_opening_hours(opening_hours):
    if opening_hours:
        opening_hours_data = json.loads(opening_hours)
        current_day = datetime.now().weekday()
        current_time = int(datetime.now().strftime("%H%M"))  # 將時間轉換為整數型態

        weekday_text = opening_hours_data.get("weekday_text", [])

        # 判斷是否有包含 "24 小時營業" 的字樣
        for text in weekday_text:
            if "24 小時營業" in text:
                return True

        # 如果沒有 "24 小時營業" 的字樣，則檢查指定時段
        for period in opening_hours_data.get("periods", []):
            open_day = period.get("open", {}).get("day")
            open_time = int(period.get("open", {}).get("time"))  # 將時間轉換為整數型態
            close_time = int(period.get("close", {}).get("time"))  # 將時間轉換為整數型態

            # 處理 close_time 為 隔天 的情況
            if close_time < open_time:
                close_time += 2400

            if open_day == current_day and open_time <= current_time <= close_time:
                return True

    return False
