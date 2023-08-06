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
print("si quieres añadir tu horario abre el .csv o corre con -v \npara parar usa ^c (control+c) en la terminal\nrecuerda que el programa solo iniciara cuando cierres completamente tu editor de tablas")
try:
    sys.argv.index("-v")
    v = True
except ValueError:
    v = False
    pass
if v:
    if sys.platform == "darwin":
        os.system("open "+location.replace("__main__.py", "")+ '/' + "schedule.csv -W")
    else:
        print("only works in OS X")
print("Started")


f = open(location.replace("__main__.py", "")+ '/' + "schedule.csv", "r+")
dayDictionary = {"Date": "Empty"}
for line in f.readlines():
    if line.lower().startswith("date"):
        continue
    line = line.strip('\n')
    day = line.split(",")
    dayDictionary[day.pop(0)] = day
f.close()
meetingSchedule = [dayDictionary["Monday"],
                   dayDictionary["Tuesday"],
                   dayDictionary["Wednesday"],
                   dayDictionary["Thursday"],
                   dayDictionary["Friday"],
                   dayDictionary["Saturday"],
                   dayDictionary["Sunday"]]
day = 0
while True:
    date = datetime.datetime.now()
    old = date.hour
    new = date.hour
    while old == new:
        try:
            date = datetime.datetime.now()
            day = date.today().weekday()
            new = date.hour
            sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)
    try:
        print(meetingSchedule[day][date.hour])
        print(day)
        print(date.hour)
        if meetingSchedule[day][date.hour] != "":
            os.system("open -a /Applications/zoom.us.app &")
            sleep(1)
            keyboard.press_and_release('command+j')
            sleep(1)
            keyboard.press_and_release('command+a')
            keyboard.press_and_release('delete')
            sleep(1)
            pyperclip.copy(meetingSchedule[day][date.hour])
            keyboard.write(meetingSchedule[day][date.hour])
            print(meetingSchedule[day][date.hour])
            if meetingSchedule[day][date.hour] == "":
                print("Nada")
            keyboard.press_and_release('enter')
            sleep(2400)
        else:
            print("Skipped")
    except IndexError:
        print("Skipped")
        pass
