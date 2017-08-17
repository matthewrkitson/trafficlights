import _thread as thread
import time
import traceback

class Poller:
    def __init__(self, lights, updaters, logger, poll_interval_seconds = 5):
        self.lights = lights
        self.updaters = updaters
        self.logger = logger
        self.poll_interval_seconds = poll_interval_seconds

    def start(self):
        thread.start_new_thread(self._poll, ())

    def _poll(self):
        while True:
            for updater in self.updaters:
                if updater:
                    try:                    
                        updater.update()
                    except Exception as e:
                        self.logger.error(e)
                        self.logger.error(''.join(traceback.format_exc()))

            time.sleep(self.poll_interval_seconds)
