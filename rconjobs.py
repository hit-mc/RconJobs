import inspect
import json
import os
import time
from threading import Thread

from jobs import BaseTask
from jobs import _RConsole
from taskloader import load_plugin_modules


class JobRunner(Thread):

    def __init__(self, tasks: list, console: _RConsole, verbose=False):
        super().__init__()
        self.__tasks = tasks
        self.__console = console
        self.__run = True
        self.__verbose = verbose
        self.__start_time = -1

    def __del__(self):
        self.stop()

    def start(self):
        self.__run = True
        super().start()

    def stop(self):
        self.__run = False

    def get_start_time(self):
        return self.__start_time

    def run(self):
        print('Polling thread is started.')
        self.__start_time = time.time()
        while self.__run:
            for task in self.__tasks:
                task: BaseTask
                tm = time.localtime()
                if task.should_run(
                        tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_wday
                ):
                    print(f'Task {task.__class__.__name__} is triggered.')
                    start_time = time.time()
                    task.run(self.__console)
                    end_time = time.time()
                    if self.__verbose:
                        print(f'Task finished in {round(end_time - start_time, 2)}s.')
                    elif end_time - start_time > 1:
                        print(f'Task {task.__class__.__name__} takes {round(end_time - start_time, 2)}s!')
            time.sleep(1)
        print('Polling thread stopped.')


def _load_tasks(task_directory: str) -> list:
    task_modules = load_plugin_modules(task_directory)

    loaded_tasks = []
    print(f'Loading tasks from {task_directory} ...')
    for module in task_modules:
        for name, obj in inspect.getmembers(module):
            if obj.__class__ == type and BaseTask in obj.__bases__:
                # valid concrete task class
                loaded_tasks.append(obj())
                print(f'Loaded task `{obj.__name__}`')
    print(f'Loaded {len(loaded_tasks)} task(s).')

    return loaded_tasks


runner = None
console = None


def interactive():
    while True:
        cmd = input('>>')
        if cmd == 'stop':
            if isinstance(runner, JobRunner):
                runner.stop()
            return


def start(task_directory: str = 'tasks'):
    global runner, console
    if not os.path.isfile('rconjobs.json'):
        print('Config file does not exist.')
        exit()
    with open('rconjobs.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    config_rcon = config['rcon']
    console = _RConsole(config_rcon['host'], config_rcon['port'], config_rcon['password'], config_rcon['use_tls'])
    tasks = _load_tasks(task_directory)
    print('Starting job runner...')
    runner = JobRunner(tasks, console)
    runner.start()
    return runner


if __name__ == '__main__':
    start()
    interactive()
