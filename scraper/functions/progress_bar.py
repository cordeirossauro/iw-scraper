import math


class ProgressBar:
    def __init__(self, total_steps, bar_size, message, current_step = 1):
        self.total_steps = total_steps
        self.current_step = current_step
        self.bar_size = bar_size
        self.message = message

    def print_bar(self):
        steps_done = math.floor(
            self.current_step / self.total_steps * self.bar_size
        )

        bar = (
            " |"
            + ("█" * steps_done)
            + (" " * (self.bar_size - 1 - steps_done))
            + "|"
        )
        progress = f" [{self.current_step}/{self.total_steps}]"

        print(self.message + progress + bar, end="\r")

    def update_bar(self, current_step):

        self.current_step = current_step
        self.print_bar()
