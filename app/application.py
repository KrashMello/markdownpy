from textual.app import App
from . import layouts

class application(App):

    CSS_PATH = "./assets/css/utility_containers.tcss"

    def compose(self):
        yield from layouts.default.compose(self)


