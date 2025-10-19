from textual.app import App
from textual.widgets import Markdown, TextArea
from app.layouts.default import DefaultLayout
from app.components.textArea import KmTextArea


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
        border: blank;
        margin: 0;
        scrollbar-size: 1 1;
        padding: 0;
    }

    .hidden {
        display: none;
        visibility: hidden;
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
    HELPER = """
# pysidian
## key bindings
- ctrl+e: editor mode
- ctrl+n: create file
- ctrl+d: delete file
- ctrl+q: exit
- j: cursor down
- k: cursor up
- l: select cursor
- h: cursor left
- l: cursor right
- o: cursor line end
- O: cursor line start
- $: cursor line end
- 0: cursor line start
- u: undo
- r: redo
- x: delete right
- w: write file
- ?: help
        """
    file_path = None
    BINDINGS = [
        ("ctrl+e", "editor_mode", "Editor mode"),
    ]

    def compose(self):
        yield DefaultLayout(id="layout")

    async def on_text_area_changed(self, event: TextArea.Changed) -> None:
        # Actualiza el widget Markdown según lo que se escribe
        preview = self.query_one("#preview", Markdown)
        preview.update(f"{event.text_area.text}")

    def action_editor_mode(self):
        text_area = self.query_one("#editor", KmTextArea)
        markdown = self.query_one("#preview", Markdown)
        markdown.add_class("hidden")
        markdown.remove_class("markdown_preview")
        text_area.remove_class("hidden")
        text_area.add_class("markdown_preview")
        text_area.focus()
