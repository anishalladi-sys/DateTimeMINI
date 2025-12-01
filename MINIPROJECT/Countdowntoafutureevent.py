from datetime import datetime

event_str = input("Enter the event date and time (YYYY-MM-DD HH:MM:SS): ")
event_date = datetime.strptime(event_str, '%Y-%m-%d %H:%M:%S')
now = datetime.now()
if event_date <= now:
    print("The event date must be in the future.")
else:
    delta = event_date - now
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Time remaining: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds.")
    