from datetime import timedelta, datetime
 
now = datetime.now()
print(now)                      # 2017-05-03 17:46:44.558754
two_days = timedelta(2)
in_two_days =  timedelta(two_days-now )
print(in_two_days)              # 2017-05-05 17:46:44.558754
