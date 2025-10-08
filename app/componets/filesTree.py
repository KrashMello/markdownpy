from textual.widgets import DirectoryTree, Static
from textual.widgets import Input
from textual.containers import Horizontal, Vertical
import os

class KmInput(Input):
    def on_input_submitted(self, event) -> None:
        container = self.app.query_one('#input_container',Horizontal)
        container.remove()
        message_panel = self.app.query_one("#message_panel", Static)
        message_panel.update(f"{event.value}")

class KmDirectoryTree(DirectoryTree):
    BINDINGS = [
       ("ctrl+n", "create_file", "Create a new file"),
       ('j', "cursor_down", "Move down"),
       ('k', "cursor_up", "Move up"),
       ('l', "select_cursor", "Select cursor"),
    ]
    def on_directory_tree_file_selected(self, event) -> None:
        message_panel = self.app.query_one("#message_panel", Static)
        message_panel.update(f"Selected file path: {event.path}")

    async def action_create_file(self) -> None:
        # Mostrar input para nombre de archivo
         await self.prompt("Ingrese el nombre del archivo:")

            # current_path = os.getcwd()  # O la ruta seleccionada, para ejemplo se usa cwd
            # file_path = os.path.join(current_path, filename)
            # # Crear archivo
            # with open(file_path, "w") as f:
            #     f.write("")  # Archivo vacío inicialmente
            # await self.app.message(f"Archivo '{filename}' creado en {current_path}")

    async def prompt(self, prompt_text: str) -> str:
        # Función para mostrar input modal para nombre de archivo
        sidebar = self.app.query_one('#sidebar',Vertical)
        input_widget = KmInput(placeholder=prompt_text)
        container = Horizontal(input_widget)
        container.id = "input_container"
        sidebar.mount(container)
        sidebar.refresh(repaint= True, layout=True)
        input_widget.focus()