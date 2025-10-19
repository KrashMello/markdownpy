from textual.app import App
from . import layouts
from textual.widgets import Markdown, TextArea
from app.layouts.default import DefaultLayout


class application(App):
    CSS = """
    .column_1{
        width: 30%;
    }
#directory_tree{
    background: $panel;
    }
#input_container {
        height: 5%;
    }

    .markdown_preview {
        width: 1fr;
        height: 1fr;
        overflow-y: auto;
        background: $panel;
    }

    .hidden {
        visibility: hidden;
        height: 0;
    }

#dialog {
        height: 5;
        background: $panel;
        color: $text;
    }

    /* The button class */
    Button {
        width: 1fr;
        height: 3;
    }

    /* Matches the question text */
    .question {
        text-style: bold;
        height: 100%;
        content-align: center middle;
    }

    /* Matches the button container */
    .buttons {
        width: 100%;
        height: auto;
        dock: bottom;
    }

    .footer_bar{
        background: $panel;
        color: $text;
        padding: 0 1;
    }
        """

    file_path = None

    def compose(self):
        yield DefaultLayout(id="layout")

    async def on_text_area_changed(self, event: TextArea.Changed) -> None:
        # Actualiza el widget Markdown según lo que se escribe
        preview = self.query_one("#preview", Markdown)
        preview.update(f"{event.text_area.text}")
