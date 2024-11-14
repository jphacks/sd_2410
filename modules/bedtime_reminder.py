from datetime import time, timedelta, datetime

# timeは0630などの時間を表す４けたの数字 (String)
# hours_beforeは何時間前にリマインドするかを指定する数字
# th 何分前後なら通知するか指定する閾値（分）
# now_strはテスト用

# 現在時刻が、alarm_timeで指定した時間からhours_before時間前の+-th分ならTrueを返し、それ以外ではFalseを返す

def is_remind_time(alarm_time_str, hours_before, th, now_str=None):

    # 4桁の数字を時と分に分ける
    alarm_hour = int(alarm_time_str[:2])
    alarm_minute = int(alarm_time_str[2:])

    now = datetime.now()
    if now_str != None:
        now_hour = int(now_str[:2])
        now_minute = int(now_str[2:])
        now = now.replace(hour=now_hour, minute=now_minute) # テスト用


    alarm_datetime = now.replace(hour=alarm_hour, minute=alarm_minute) + timedelta(days=1)
    
    # アラーム時間のhours_before時間前を計算
    reminder_time = alarm_datetime - timedelta(hours=hours_before)

    
    print("now is :", now)
    print("alarm_time is :", alarm_datetime)
    print("reminder_time is :", reminder_time)

    start_time = now - timedelta(minutes=th)
    end_time = now + timedelta(minutes=th)

    return start_time <= reminder_time <= end_time