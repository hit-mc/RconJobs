from jobs import BaseTask, _RConsole


class GoBedNotification(BaseTask):
    __last_notified_day = -1

    def should_run(self, year: int, month: int, day: int, hour: int, minute: int, week_day: int) -> bool:
        if hour == 0 and minute == 0:
            if day != self.__last_notified_day:
                self.__last_notified_day = day
                return True
        return False

    def run(self, console: _RConsole) -> None:
        console.execute('say 该睡觉了！')
