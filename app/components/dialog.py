from textual.app import ComposeResult
from textual.widgets import Static, Button
from textual.containers import Horizontal, Container
from textual.events import Key


class Dialog(Container):
    response = None

    def __init__(
        self, Text: str = "Texto por defecto", on_result=None, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.Text = Text
        self.on_result = on_result

    def compose(self) -> ComposeResult:
        yield Static(self.Text, classes="question")
        yield Horizontal(
            Button("Yes", flat=True, variant="success"),
            Button("No", flat=True, variant="error").focus(),
            classes="buttons",
        )

    async def on_key(self, event: Key):
        if event.key == "y" and self.on_result:
            self.remove()
            self.on_result("success")
        elif event.key == "n" and self.on_result:
            self.remove()
            self.on_result("error")
        elif event.key == "escape":
            self.remove()
        else:
            return

    def on_button_pressed(self, event: Button.Pressed):
        self.remove()
        if self.on_result:
            self.on_result(event.button.variant)
