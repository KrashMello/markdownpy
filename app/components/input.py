from textual.widgets import Input


class KmInput(Input):
    def __init__(self, on_summit=None, **kwargs):
        super().__init__(**kwargs)
        self.on_summit = on_summit

    async def on_input_submitted(self, event) -> None:
        if self.on_summit:
            self.on_summit(event.value)
