import inspect
import json
import logging
import os
import sys
import time
from threading import Thread

from jobs import BaseTask
from jobs import _RConsole
from taskloader import load_plugin_modules

CONFIG_FILE = 'rconjobs.json'
LOG_FILE = 'rconjobs.log'


class JobRunner(Thread):

    def __init__(self, tasks: list, console: _RConsole, verbose=False):
        super().__init__()
        self.__tasks = tasks
        self.__console = console
        self.__run = True
        self.__verbose = verbose

    def __del__(self):
        self.stop()

    def start(self):
        self.__run = True
        super().start()

    def stop(self):
        self.__run = False
        logging.debug('JobRunner is stopping.')

    def run(self):
        logging.info('Polling thread is started.')
        while self.__run:
            for task in self.__tasks:
                assert isinstance(task, BaseTask), f'Object {task} is not a valid task instance'
                tm = time.localtime()
                if task.should_run(
                        tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_wday
                ):
                    logging.info(f'Task {task.__class__.__name__} is triggered.')
                    start_time = time.time()
                    task.run(self.__console)
                    end_time = time.time()
                    if self.__verbose:
                        logging.warning(f'Task finished in {round(end_time - start_time, 2)}s.')
                    elif end_time - start_time >= 2:
                        logging.warning(f'Task {task.__class__.__name__} takes {round(end_time - start_time, 2)}s!')
            time.sleep(1)
        logging.info('Polling thread stopped.')


def _load_tasks(task_directory: str) -> list:
    task_modules = load_plugin_modules(task_directory)

    loaded_tasks = []
    logging.info(f'Loading tasks from {task_directory} ...')
    for module in task_modules:
        for name, obj in inspect.getmembers(module):
            if obj.__class__ == type and BaseTask in obj.__bases__:
                # valid concrete task class
                loaded_tasks.append(obj())
                logging.info(f'Loaded task `{obj.__name__}`')
    logging.info(f'Loaded {len(loaded_tasks)} task(s).')

    return loaded_tasks


runner = None
console = None


def interactive():
    while True:
        cmd = input('>>')
        if cmd == 'stop':
            if isinstance(runner, JobRunner):
                runner.stop()
                logging.info('Waiting JobRunner to stop...')
                start_time = time.time()
                runner.join()
                end_time = time.time()
                logging.info(f'JobRunner is stopped. time={round(end_time - start_time, 2)}s.')
                return
        else:
            print('Invalid command.')


def start(task_directory: str = 'tasks'):
    global runner, console
    if not os.path.isfile(CONFIG_FILE):
        logging.error('Config file does not exist.')
        exit()
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    config_rcon = config['rcon']
    console = _RConsole(config_rcon['host'], config_rcon['port'], config_rcon['password'], config_rcon['use_tls'])
    tasks = _load_tasks(task_directory)
    logging.info('Starting job runner...')
    runner = JobRunner(tasks, console)
    runner.start()
    return runner


if __name__ == '__main__':
    log_level = logging.INFO
    if '--verbose' in sys.argv or '-v' in sys.argv:
        log_level = logging.DEBUG
    logging.basicConfig(
        filename=LOG_FILE,
        filemode='a',
        level=log_level,
        format='[%(levelname)s][%(asctime)s][line:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    start()
    interactive()
