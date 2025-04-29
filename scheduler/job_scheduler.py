import time
from threading import Timer

class JobScheduler:
    def __init__(self, interval_seconds: int, job_func: callable):
        self.interval_seconds = interval_seconds
        self.job_func = job_func

    def start(self):
        self._schedule_next_run()

    def _schedule_next_run(self):
        self.job_func()
        Timer(self.interval_seconds, self._schedule_next_run).start()