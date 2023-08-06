#!/usr/bin/python3
import os
import sys
try:
    import keyboard
    import datetime
    import pyperclip
    from time import sleep
except ModuleNotFoundError:
    os.system("/usr/bin/pip3 install keyboard datetime pyperclip time --user")

location = sys.argv[0]
os.system("clear")
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
        sleep(60)
        now = datetime.datetime.now()
        hour = now.strftime('%H:%M')
        print(hour)
        hour_classes = hour_dict.get(hour, "")
        if hour_classes != "":
            meetCode = (hour_classes[now.weekday()])
            break

    print(meetCode)
    os.system("open -a /Applications/zoom.us.app &")
    sleep(1)
    keyboard.press_and_release('command+j')
    sleep(1)
    keyboard.press_and_release('command+a')
    keyboard.press_and_release('delete')
    sleep(1)
    pyperclip.copy(meetCode)
    keyboard.write(meetCode)
    keyboard.press_and_release('enter')
