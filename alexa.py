from speech_recognition import Recognizer, Microphone
from pyttsx3 import init
from os import system
from pywhatkit import playonyt, search
from datetime import datetime
from playsound import playsound
from psutil import sensors_battery
from webbrowser import open
from time import sleep
import alarm_timer


r = Recognizer()
engine = init()
alarm = alarm_timer.alarm_timer()

class Alexa:
    def __init__(self):
        pass

    def talk(self, text):
        engine.say(text)
        engine.runAndWait()

    def batteryCheck(self):
        battery = sensors_battery()
        return int(battery.percent)

    def lissen(self, mic):
        voice = r.listen(mic)
        return str(r.recognize_google(voice).lower())

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

    def command(self):
        with Microphone() as mic:
            command = self.lissen(mic)
            self.confirmSound()

            if "open" in command:
                command = command.replace("open ", "")

                if command == "settings": system("start ms-settings:")
                else: system("start " + command)

            elif "play" in command:
                command = command.replace("play ", "")
                playonyt(command)

            elif "shutdown system" == command: quit()

            elif "create alarm" in command:
                time = command.replace("create alarm ", "").replace(":", "")
                hour = time[0:2]
                minute = time[2:4]
                alarm.Create_Alarm(hour, minute)

            elif "set timer" in command:
                time = command.replace("set timer ", "")
                kind = time[2:].replace(" ", "")
                alarm.Set_Timer(time, kind)

            elif "time" == command or "what time is it" == command:
                hour = self.pullTime("hour")
                minute = self.pullTime("min")
                self.talk(str(hour) + ":" + str(minute))

            elif "search on youtube" in command:
                command = command.replace("search on youtube ", "+")#.replace(" ", "+")
                open("https://www.youtube.com/results?search_query=" + command)

            elif "search" in command:
                command = command.replace("search ", "")
                search(command)

            elif "check battery" == command:
                battery = self.batteryCheck()
                self.talk(battery)

            elif ".com" in command or ".net" in command: open("https://www." + command)

            else: self.error()

    def alexa(self):
        with Microphone() as mic:
            self.startupSound()
            if self.batteryCheck() <= 25:
                sleep(1)
                self.batterySound()

            while True:
                if alarm.alarm:
                    n_hour = self.pullTime("hour")
                    n_minute = self.pullTime("min")

                    if self.hour == n_hour and self.minute == n_minute:
                        self.alarmSound()
                        alarm.closeAlarm()
 
                if alarm.timer:
                    second = self.pullTime("sec")
                    minute = self.pullTime("min")
                    hour = self.pullTime("hour")

                    if alarm.timerTime <= 60:
                        if alarm.kind == "hour" or alarm.kind == "hours":
                            if alarm.timerTime == hour and alarm.nowMinute == minute and alarm.nowSecond == second:
                                alarm.closeTimer()
                                self.alarmSound()

                        elif alarm.kind == "minute" or alarm.kind == "minutes":
                            if alarm.timerTime == minute and alarm.nowSecond == second:
                                alarm.closeTimer()
                                self.alarmSound()

                        elif alarm.kind == "second" or alarm.kind == "seconds":
                            if alarm.timerTime == second:
                                alarm.closeTimer()
                                self.alarmSound()

                    else:
                        alarm.timerTime = int(alarm.timerTime / 60)

                try:
                    text = self.lissen(mic)

                    if "alexa" == text:
                        self.ding()
                        self.command()

                except Exception: pass

if __name__ == "__main__":
    alexa = Alexa()
    alexa.alexa()