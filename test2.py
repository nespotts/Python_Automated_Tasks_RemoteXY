from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=-5))

now1 = datetime.now(tz)

print(now1.hour)