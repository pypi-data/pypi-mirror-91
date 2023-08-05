from threading import Lock

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.stream import Stream
from jivago.scheduling.schedule import Schedule
from jivago.scheduling.scheduled_task_runner import ScheduledTaskRunner


class TaskScheduler(object):

    def __init__(self, service_locator: ServiceLocator):
        self.service_locator = service_locator
        self.task_runners = []
        self.lock = Lock()

    def schedule_task(self, runnable_class: type, schedule: Schedule):
        with self.lock:
            task_runner = ScheduledTaskRunner(runnable_class, schedule, self.service_locator)
            self.task_runners.append(task_runner)
            task_runner.start()

    def stop(self):
        with self.lock:
            Stream(self.task_runners).forEach(lambda x: x.stop())
