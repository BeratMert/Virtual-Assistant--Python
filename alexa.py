from speech_recognition import Recognizer, Microphone
from pyttsx3 import init
from os import system
from pywhatkit import playonyt, search
from datetime import datetime
from playsound import playsound
from psutil import sensors_battery
from webbrowser import open
from time import sleep
import set_timer


r = Recognizer()
engine = init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

timer = set_timer.Timer()

class Alexa:
    def __init__(self):
        self.hour = 0
        self.minute = 0
        self.alarm = False

    def talk(self, text):
        engine.say(text)
        engine.runAndWait()

    def batteryCheck(self):
        battery = sensors_battery()
        return int(battery.percent)

    def lissen(self, mic):
        voice = r.listen(mic)
        return str(r.recognize_google(voice).lower())

    def closeAlarm(self):
        self.alarmSound()

        self.alarm = False
        self.hour = 0
        self.minute = 0

    def ding(self): playsound("sounds/ding.wav")

    def startupSound(self): playsound("sounds/startup.wav")

    def batterySound(self): playsound("sounds/battery.wav")

    def confirmSound(self): playsound("sounds/confirm.wav")

    def error(self): playsound("sounds/error.wav")

    def alarmSound(self): playsound("sounds/alarm.wav")

    def pullTime(self, kind):
        if kind == "hour": return int(datetime.now().strftime("%H"))
        elif kind == "min": return int(datetime.now().strftime("%M"))
        elif kind == "sec": return int(datetime.now().strftime("%S"))
        elif kind == "a" or kind == "A": return str(datetime.now().strftime("%A"))# Day
        else: self.error()

    def command(self, cmd):
        if "open" in cmd:
            cmd = cmd.replace("open ", "")

            if cmd == "settings": system("start ms-settings:")
            else: system("start " + cmd)

        elif "play" in cmd:
            cmd = cmd.replace("play ", "")
            playonyt(cmd)

        elif "shutdown system" == cmd: quit()

        elif "create alarm" in cmd:
            time = cmd.replace("create alarm ", "").split(":")
            self.hour = int(time[0])
            self.minute = int(time[1])

            if "to" in str(self.hour): self.hour = int(2)
            elif "to" in str(self.minute): self.minute = int(2)
            self.alarm = True

        elif "set timer" in cmd:
            time = cmd.replace("set timer ", "")
            kind = time[2:].replace(" ", "")
            timer.Set_Timer(time, kind)

        elif "time" == cmd or "what time is it" == cmd:
            hour = self.pullTime("hour")
            minute = self.pullTime("min")
            self.talk(str(hour) + ":" + str(minute))
            print(str(hour) + ":" + str(minute))

        elif "search on youtube" in cmd:
            cmd = cmd.replace("search on youtube ", "")
            open("https://www.youtube.com/results?search_query=" + cmd)

        elif "search" in cmd:
            cmd = cmd.replace("search ", "")
            search(cmd)

        elif "check battery" == cmd:
            battery = self.batteryCheck()
            self.talk(battery)

        elif ".com" in cmd or ".net" in cmd: open("https://www." + cmd)

        else: 
            self.error()

    def alexa(self):
        with Microphone() as mic:
            self.startupSound()
            if self.batteryCheck() <= 25:
                sleep(1)
                self.batterySound()

            while True:
                if self.alarm:
                    n_hour = self.pullTime("hour")
                    n_minute = self.pullTime("min")

                    if self.hour == n_hour and self.minute == n_minute:
                        self.alarmSound()
                        self.closeAlarm()
 
                if timer.timer:
                    second = self.pullTime("sec")
                    minute = self.pullTime("min")
                    hour = self.pullTime("hour")

                    if timer.timerTime <= 60:
                        if timer.kind == "hour" or timer.kind == "hours":
                            if timer.timerTime == hour and timer.nowMinute == minute and timer.nowSecond == second:
                                timer.closeTimer()
                                self.timerSound()

                        elif timer.kind == "minute" or timer.kind == "minutes":
                            if timer.timerTime == minute and timer.nowSecond == second:
                                timer.closeTimer()
                                self.timerSound()

                        elif timer.kind == "second" or timer.kind == "seconds":
                            if timer.timerTime == second:
                                timer.closeTimer()
                                self.timerSound()

                    else:
                        timer.timerTime = int(timer.timerTime / 60)

                try:
                    text = self.lissen(mic)

                    if "alexa" in text:
                        self.ding()

                        command = self.lissen(mic)
                        self.confirmSound()
                        self.command(command)

                except Exception: pass

if __name__ == "__main__":
    alexa = Alexa()
    alexa.alexa()