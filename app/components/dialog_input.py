from app.components.input import KmInput
from textual.widgets import Static, Input
from textual.containers import Horizontal, Container
from textual.app import ComposeResult
from textual.events import Key


class DialogInput(Container):
    def __init__(self, placeholder: str, on_summit: None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.placeholder = placeholder
        self.input_widget = KmInput(placeholder=self.placeholder, on_summit=on_summit)

    def compose(self) -> ComposeResult:
        yield (Static("Crear archivo"))
        yield (Horizontal(self.input_widget.focus()))

    def on_key(self, event: Key):
        if event.key == "escape":
            self.remove()
        else:
            return
