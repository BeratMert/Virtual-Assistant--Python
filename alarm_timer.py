class alarm_timer():
    def __init__(self):
        self.alarm = False
        self.hour = 0
        self.minute = 0

        self.timer = False
        self.timerTime = 0
        self.kind = ""
        self.nowMinute = 0
        self.nowSecond = 0

    def Create_Alarm(self, a_hour, a_min):
        self.alarm = True
        self.hour = int(a_hour)
        self.minute = int(a_min)

    def Set_Timer(self, kind, time):
        if kind == "hour" or kind == "hours":
            time = time.replace(kind, "")
            self.timerTime = int(time) * 3600
            self.timerTime += self.pullTime("hour") * 3600
            self.nowMinute = self.pullTime("min")
            self.nowSecond = self.pullTime("sec")
            self.timer = True

        elif kind == "minute" or kind == "minutes":
            time = time.replace(kind, "")
            self.timerTime = int(time) * 60
            self.timerTime += self.pullTime("min") * 60
            self.nowSecond = self.pullTime("sec")
            self.timer = True

        elif kind == "second" or kind == "seconds": 
            time = time.replace(kind, "")
            self.timerTime = int(time)
            self.timerTime += self.pullTime("sec")
            self.timer = True

        else:
            pass

    def closeTimer(self):
        print("Timer is finish")

        self.timer = False
        self.timerTime = 0

    def closeAlarm(self):
        print("Alarm is finish")

        self.alarm = False
        self.hour = 0
        self.minute = 0