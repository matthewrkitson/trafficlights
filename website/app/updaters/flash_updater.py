from app.controller import Controller

class FlashUpdater:
    def __init__(self, lights, logger, enable_lights=False, enable_buzz=False):
        self.lights = lights
        self.logger = logger
        self.enable_lights = enable_lights
        self.enable_buzz = enable_buzz
        self.lights_state = Controller.RED

    def update(self):
        if self.enable_lights:
            new_lights_state = Controller.RED if self.lights_state == Controller.GREEN else Controller.GREEN
            for x in range(self.lights.num_indicators):
                self.lights.set_indicator(x, new_lights_state)

            self.lights_state = new_lights_state

        if self.enable_buzz:
            self.lights.buzz(0, 100)
