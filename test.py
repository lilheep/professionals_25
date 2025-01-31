from datetime import datetime, timedelta, date

birthday = date(year=1976, month=12, day=13)

today = datetime.today().date()
age_18 = today - timedelta(days=18*365.25)

if birthday > age_18:
    print('No')
else:
    print('YES')
