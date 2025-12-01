from datetime import date
from calendar import monthrange

d = int(input("Enter birth day: "))
m = int(input("Enter birth month: "))
y = int(input("Enter birth year: "))

today = date.today()
birth_date = date(y, m, d)
years = today.year - birth_date.year
months = today.month - birth_date.month
days = today.day - birth_date.day

if days < 0:
    months -= 1
    if today.month == 1:
        prev_month = 12
        prev_year = today.year - 1
    else:
        prev_month = today.month - 1
        prev_year = today.year
    days += monthrange(prev_year, prev_month)[1]
if months < 0:
    years -= 1
    months += 12

print(f"Your age is {years} years, {months} months, and {days} days.")