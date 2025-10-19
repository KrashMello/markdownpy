from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll, Container, Grid
from textual.widgets import Static
from app.components.filesTree import KmDirectoryTree
from app.components.textArea import KmTextArea
from textual.widgets import Markdown, TextArea
from textual.events import Event


class DefaultLayout(Horizontal):
    def compose(self) -> ComposeResult:
        with Vertical(id="sidebar", classes="column_1"):
            yield KmDirectoryTree("./", id="directory_tree")
        with Vertical():
            with VerticalScroll(
                id="markdown_container", can_focus=True, classes="markdown_preview"
            ):
                markdown = Markdown(id="preview")
                markdown.code_indent_guides = False
                yield markdown
            text_area = KmTextArea(language="markdown", classes="hidden", id="editor")
            text_area.text = self.app.HELPER
            yield text_area
            yield Static(self.app.vim_mode, classes="footer_bar", id="footer")
