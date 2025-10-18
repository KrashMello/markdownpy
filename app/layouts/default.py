from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll, Container, Grid
from textual.widgets import Static
from app.components.filesTree import KmDirectoryTree
from app.components.textArea import KmTextArea
from textual.widgets import Markdown, TextArea
from textual.events import Event


class DefaultLayout(Horizontal):
    BINDINGS = [
        ("ctrl+e", "editor_mode", "Editor mode"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="sidebar", classes="column_1"):
            yield KmDirectoryTree("./", id="directory_tree")
        with Vertical():
            markdown = Markdown(id="preview", classes="markdown_preview")
            markdown.code_indent_guides = False
            yield markdown
            text_area = KmTextArea(language="markdown", classes="hidden", id="editor")
            yield text_area
            yield Static(text_area.vim_mode, classes="footer_bar", id="footer")

    def action_editor_mode(self):
        text_area = self.query_one("#editor", KmTextArea)
        markdown = self.query_one("#preview", Markdown)
        markdown.add_class("hidden")
        markdown.remove_class("markdown_preview")
        text_area.remove_class("hidden")
        text_area.add_class("markdown_preview")
        text_area.focus()
