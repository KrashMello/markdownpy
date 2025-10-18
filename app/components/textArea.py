from textual.widgets import TextArea, Static, Markdown
from textual.events import Key
from app.components.filesTree import KmDirectoryTree


class KmTextArea(TextArea):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vim_mode = "normal"
        self.cursor_pos = 0

    BINDINGS = []

    async def on_key(self, event: Key) -> None:
        self.cursor_pos = self.cursor_location
        # self.app.notify(event.key)
        if self.vim_mode == "normal":
            event.prevent_default()
            if event.key == "i":
                self.vim_mode = "insert"
            elif event.key == "h":
                self.action_cursor_left()
            elif event.key == "l":
                self.action_cursor_right()
            elif event.key == "j":
                self.action_cursor_down()
            elif event.key == "k":
                self.action_cursor_up()
            elif event.key == "o":
                self.action_cursor_line_end()
                self.insert("\n")
                self.cursor_location = [
                    self.cursor_pos[0] + 1,
                    self.cursor_pos[1] + 1,
                ]
                self.vim_mode = "insert"
            elif event.key == "O":
                self.action_cursor_line_start()
                self.insert("\n")
                self.cursor_location = [
                    self.cursor_pos[0] - 1,
                    self.cursor_pos[1],
                ]
                self.vim_mode = "insert"
            elif event.key == "dollar_sign":
                self.action_cursor_line_end()
            elif event.key == "0":
                self.action_cursor_line_start()
            elif event.key == "u":
                self.undo()
            elif event.key == "r":
                self.redo()
            elif event.key == "x":
                self.action_delete_right()
            elif event.key == "w":
                directory = self.app.query_one("#directory_tree", KmDirectoryTree)
                markdown = self.app.query_one("#preview", Markdown)
                self.add_class("hidden")
                self.remove_class("markdown_preview")
                markdown.remove_class("hidden")
                markdown.add_class("markdown_preview")
                directory.focus()
            else:
                return
        elif self.vim_mode == "insert":
            if event.key == "escape":
                self.vim_mode = "normal"
            elif event.key == "ctrl+h":
                self.action_cursor_left()
            elif event.key == "ctrl+l":
                self.action_cursor_right()
            elif event.key == "ctrl+j":
                self.action_cursor_down()
            elif event.key == "ctrl+k":
                event.prevent_default()
                self.action_cursor_up()
            else:
                return event.key

        footer = self.app.query_one("#footer", Static)
        footer.content = self.vim_mode

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        # Actualiza el widget Markdown según lo que se escribe
        file_path = self.app.file_path
        file = open(file_path, "w")
        file.write(event.text_area.text)
