from jobs import BaseTask, _RConsole


class TestTask(BaseTask):
    __last_executed_min = -1

    def should_run(self, year: int, month: int, day: int, hour: int, minute: int, week_day: int) -> bool:
        # if self.__last_executed_min != minute:
        #     self.__last_executed_min = minute
        #     return True
        return True

    def run(self, console: _RConsole) -> None:
        console.execute('say test3')
