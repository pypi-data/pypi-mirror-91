#!/usr/bin/python3
import os
import sys
import time
import keyboard
import datetime
import pyperclip

location = sys.argv[0]
os.system("clear")

if not os.path.isfile(location.replace("__main__.py", "") + "schedule.csv"):
    with open(location.replace("__main__.py", "") + "schedule.csv", "w+") as f:
        import requests
        schedule = requests.get("https://raw.githubusercontent.com/DogAteMyCode/autozoom/master/schedule.csv").text
        f.write(schedule)


print("If you want to add your schedule run with -v flag\nto stop use ^c (control+c) keyboardInterrupt\n")
try:
    sys.argv.index("-v")
    v = True
except ValueError:
    v = False
    pass
if v:
    if sys.platform == "darwin":
        print("Appliciation won't start untill the .csv editor is fully closed")
        os.system("open "+location.replace("__main__.py", "") + "schedule.csv -W")
    else:
        print("only works in OS X")
print("Started")


with open(location.replace("__main__.py", "") + "schedule.csv", "r+") as f:
    rows = [row.strip('\n').split(",") for row in f.readlines()]
columns = []
column_count = len(rows[0])
column = []
for i in range(column_count):
    for row in rows:
        column.append(row[i])
    columns.append(column)
    column = []
hour_dict = {"*":""}
for column in columns:
    hour_dict[column.pop(0)] = column
while True:
    while True:
        time.sleep(60)
        now = datetime.datetime.now()
        hour = now.strftime('%H:%M')
        if hour.startswith("0"):
            hour = hour.replace("0", "", 1)
        hour_classes = hour_dict.get(hour, "")
        if hour_classes != "":
            meetCode = (hour_classes[now.weekday()])
            if meetCode != "":
                break

    print(meetCode)
    os.system("open -a /Applications/zoom.us.app &")
    time.sleep(2)
    keyboard.press_and_release('command+j')
    time.sleep(1)
    keyboard.press_and_release('command+a')
    keyboard.press_and_release('delete')
    time.sleep(1)
    pyperclip.copy(meetCode)
    keyboard.write(meetCode)
    keyboard.press_and_release('enter')
