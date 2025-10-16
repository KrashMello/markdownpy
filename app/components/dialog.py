from textual.app import ComposeResult
from textual.widgets import Static, Button
from textual.containers import Horizontal, Container

class Dialog(Container):
    response = None
    def __init__(self, Text: str = "Texto por defecto", on_result=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.Text = Text
        self.on_result = on_result

    def compose(self) -> ComposeResult:
        yield Static(self.Text, classes="question")
        yield Horizontal(
            Button("Yes", flat=True, variant="success"),
            Button("No", flat=True, variant="error"),
            classes="buttons",
        )

    def on_button_pressed(self,event: Button.Pressed):
        self.remove()
        if self.on_result:
            self.on_result(event.button.variant)

