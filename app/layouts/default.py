from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll, Container, Grid
from textual.widgets import Static
from ..componets.filesTree import KmDirectoryTree
from textual.widgets import Markdown, TextArea
EXAMPLE_MARKDOWN = """\
# Markdown Viewer

This is an example of Textual's `MarkdownViewer` widget.


## Features

Markdown syntax and extensions are supported.

- Typography *emphasis*, **strong**, `inline code` etc.
- Headers
- Lists (bullet and ordered)
- Syntax highlighted code blocks
- Tables!

## Tables

Tables are displayed in a DataTable widget.

| Name            | Type   | Default | Description                        |
| --------------- | ------ | ------- | ---------------------------------- |
| `show_header`   | `bool` | `True`  | Show the table header              |
| `fixed_rows`    | `int`  | `0`     | Number of fixed rows               |
| `fixed_columns` | `int`  | `0`     | Number of fixed columns            |
| `zebra_stripes` | `bool` | `False` | Display alternating colors on rows |
| `header_height` | `int`  | `1`     | Height of header row               |
| `show_cursor`   | `bool` | `True`  | Show a cell cursor                 |


## Code Blocks

Code blocks are syntax highlighted.

```python
class ListViewExample(App):
    def compose(self) -> ComposeResult:
        yield ListView(
            ListItem(Label("One")),
            ListItem(Label("Two")),
            ListItem(Label("Three")),
        )
        yield Footer()
```

## Litany Against Fear

I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
I will permit it to pass over me and through me.
And when it has gone past, I will turn the inner eye to see its path.
Where the fear has gone there will be nothing. Only I will remain.
"""

TEXT = """\
def hello(name):
    print("hello" + name)

def goodbye(name):
    print("goodbye" + name)
"""
QUESTION = "Do you want to learn about Textual CSS?"
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
    

