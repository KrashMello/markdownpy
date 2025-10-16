from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll, Container, Grid
from textual.widgets import Static
from app.components.filesTree import KmDirectoryTree
from textual.widgets import Markdown, TextArea

def compose(self) -> ComposeResult:
    with Horizontal():
        with Vertical(id="sidebar", classes="column_1"):
            yield KmDirectoryTree("./", id="directory_tree")
        with Vertical():
                markdown = Markdown(id='preview', classes="markdown_preview")
                markdown.code_indent_guides = False
                yield markdown
                text_area = TextArea(language='markdown', classes="markdown_text")
                yield text_area
    

