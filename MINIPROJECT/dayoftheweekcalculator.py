

day = int(input("Enter day: "))
month = int(input("Enter month: "))
year = int(input("Enter year: "))

if month < 3:
    month += 12
    year -= 1
k = year % 100
j = year // 100
h = (day + 13 * (month + 1) // 5 + k + k // 4 + j // 4 + 5 * j) % 7
days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

print("Day of the week is:", days[h])