from datetime import time, timedelta, datetime

# timeは0630などの時間を表す４けたの数字 (String)
# hours_beforeは何時間前にリマインドするかを指定する数字
# th 何分前後なら通知するか指定する閾値（分）

# 現在時刻が、alarm_timeで指定した時間からhours_before時間前の+-th分ならTrueを返し、それ以外ではFalseを返す

def is_remind_time(alarm_time_str, hours_before, th):
    # 4桁の数字を時と分に分ける
    hour = int(alarm_time_str[:2])
    minute = int(alarm_time_str[2:])
    
    now = datetime.now()
    now = now.replace(hour=23, minute=59) - timedelta(days=1) # テスト用


    alarm_datetime = now.replace(hour=hour, minute=minute) + timedelta(days=1)
    
    # アラーム時間のhours_before時間前を計算
    reminder_time = alarm_datetime - timedelta(hours=hours_before)

    
    print("now is :", now)
    print("alarm_time is :", alarm_datetime)
    print("reminder_time is :", reminder_time)

    start_time = now - timedelta(minutes=th)
    end_time = now + timedelta(minutes=th)

    return start_time <= reminder_time <= end_time


# 使用例
if is_remind_time("0600", 6, 5):
    print("nero")