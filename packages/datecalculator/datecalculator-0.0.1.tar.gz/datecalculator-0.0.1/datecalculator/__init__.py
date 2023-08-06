from datetime import date
k=""" 
welcome 
please make the code as this 

import datecalculator as da

da.period(enter day, enter month,enter year)

"""
print(k)

def period(day,month,year):
    r_year=0
    r_month=0
    r_day=0
    today = date.today()
    td=today.day-day
    tm=today.month-month
    ty=today.year-year
    r=td+(tm*30)+(ty*365)
    while r>=365:
        r-=365
        r_year +=1
    while r>=30:
        r-=30
        r_month+=1
    r_day=r
    print("there are ",r_year ,"years and ", r_month,"month and ",r_day ,"days .")
    return r_day,r_month,r_year