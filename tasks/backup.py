from jobs import BaseTask, _RConsole


class BackupTask(BaseTask):
    __last_executed_day = -1

    def should_run(self, year: int, month: int, day: int, hour: int, minute: int, week_day: int) -> bool:
        if hour == 1:
            if day != self.__last_executed_day:
                self.__last_executed_day = day
                return True
        return False

    def run(self, console: _RConsole) -> None:
        console.execute('say Backup the world...')
        console.execute('kb backup')
