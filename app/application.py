from textual.app import App
from . import layouts
from textual.widgets import Markdown, TextArea
from app.layouts.default import DefaultLayout


class application(App):
    CSS_PATH = "./assets/css/utility_containers.tcss"
    file_path = None

    def compose(self):
        yield DefaultLayout(id="layout")

    async def on_text_area_changed(self, event: TextArea.Changed) -> None:
        # Actualiza el widget Markdown según lo que se escribe
        preview = self.query_one("#preview", Markdown)
        preview.update(f"{event.text_area.text}")
