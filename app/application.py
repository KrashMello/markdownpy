from textual.app import App
from textual.widgets import Markdown, TextArea, Static
from textual.containers import Vertical, VerticalScroll
from app.layouts.default import DefaultLayout
from app.components.textArea import KmTextArea


class application(App):
    CSS = """
    .column_1{
        width: 25%;
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
    HELPER = """# pysidian

## key bindings

- i: editor insert mode
- ctrl+n: create file
- ctrl+d: delete file
- control+e: toggle hidden sidebar
- ctrl+q: exit
- ?: help

### INSERT mode

- ctrl+s: save file
- j: cursor down
- k: cursor up
- l: select cursor
- h: cursor left
- l: cursor right

### NORMAL mode
- ctrl+j: cursor down
- ctrl+k: cursor up
- ctrl+l: select cursor
- ctrl+h: cursor left
- ctrl+l: cursor right
- ctrl+s: save file
- ctrl+v: paste line
- ctrl+x: cut line
- K: scroll up
- J: scroll down
- o: cursor line end
- O: cursor line start
- $: cursor line end
- 0: cursor line start
- u: undo
- r: redo
- x: delete right
- w: save file
        """
    file_path = None
    vim_mode = "NORMAL"
    hidden = False
    BINDINGS = [
        ("i", "editor_mode", "Editor mode"),
        ("question_mark", "helper", "activar helper"),
        ("ctrl+e", "hidden_sidebar", "Toggle hidden sidebar"),
        ("K", "preview_scroll_up", "Preview scroll up"),
        ("J", "preview_scroll_down", "Preview scroll down"),
    ]

    def compose(self):
        yield DefaultLayout(id="layout")

    def action_preview_scroll_up(self):
        markdown = self.query_one("#markdown_container", VerticalScroll)
        markdown.scroll_up()

    def action_preview_scroll_down(self):
        markdown = self.query_one("#markdown_container", VerticalScroll)
        markdown.scroll_down()

    def action_hidden_sidebar(self):
        if self.hidden:
            self.hidden = False
            self.app.query_one("#sidebar", Vertical).remove_class("hidden")
        else:
            self.hidden = True
            self.app.query_one("#sidebar", Vertical).add_class("hidden")

    def action_helper(self):
        text_area = self.query_one("#editor", KmTextArea)
        markdown = self.query_one("#markdown_container", VerticalScroll)
        text_area.add_class("hidden")
        text_area.remove_class("markdown_preview")
        markdown.remove_class("hidden")
        markdown.add_class("markdown_preview")
        text_area.text = self.HELPER
        text_area.is_file = False

    async def on_text_area_changed(self, event: TextArea.Changed) -> None:
        # Actualiza el widget Markdown según lo que se escribe
        preview = self.query_one("#preview", Markdown)
        preview.update(f"{event.text_area.text}")

    def action_editor_mode(self):
        text_area = self.query_one("#editor", KmTextArea)
        markdown = self.query_one("#markdown_container", VerticalScroll)
        if self.vim_mode == "NORMAL":
            self.vim_mode = "INSERT"
            footer = self.app.query_one("#footer", Static)
            footer.content = self.vim_mode
            markdown.add_class("hidden")
            markdown.remove_class("markdown_preview")
            text_area.remove_class("hidden")
            text_area.add_class("markdown_preview")
            text_area.focus()
