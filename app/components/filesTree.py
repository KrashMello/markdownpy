from textual.widgets import DirectoryTree, Static, Input
from textual.containers import Horizontal, Vertical
from app.components.dialog import Dialog
import os
import shutil

class KmInput(Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs.get('placeholder'))
        self.path = kwargs.get('path')

    async def on_input_submitted(self, event) -> None:
        tree = self.app.query_one('#directory_tree', KmDirectoryTree)
        filename = event.value
        container = self.app.query_one('#input_container',Horizontal)
        current_path = os.getcwd()
        file_path = os.path.join(current_path, '' if self.path is None else self.path, filename)
        with open(file_path, "w") as f:
            f.write("")
        container.remove()
        await tree.reload()
        self.app.notify(f"{current_path}{'' if self.path is None else self.path }\{filename}",title="File created")

class KmDirectoryTree(DirectoryTree):
    aux_path = None
    BINDINGS = [
       ("ctrl+n", "create_file", "Create a new file"),
       ("ctrl+d", "delete_file", "Delete a new file"),
       ('j', "cursor_down", "Move down"),
       ('k', "cursor_up", "Move up"),
       ('l', "select_cursor", "Select cursor"),
    ]
    def on_directory_tree_file_selected(self, event) -> None:
        self.aux_path = event.path

    def on_directory_tree_directory_selected(self, event) -> None:
        self.aux_path = event.path

    def handler_delete_file(self, variant):
        if variant == 'success':
            if self.cursor_node and self.cursor_node.data:
                path = self.cursor_node.data.path
                if os.path.exists(path) and str(path) != '.':
                    try:
                        if os.path.isfile(path):
                            os.remove(path)
                            self.app.notify(f"Archivo eliminado: {path}")
                        elif os.path.isdir(path):
                            shutil.rmtree(path)
                            self.app.notify(f"Directorio eliminado: {path}")
                        tree = self.app.query_one('#directory_tree', KmDirectoryTree)
                        tree.reload()
                    except Exception as e:
                        self.app.notify(f"Error al eliminar: {e}")
                else:
                    self.app.notify("No se puede eliminar esta archivo o directorio")
            else:
                self.app.notify("No hay archivo o directorio seleccionado")

    async def action_delete_file(self) -> None:
        sidebar = self.app.query_one("#sidebar", Vertical)
        container = Dialog(Text = 'Desea eliminar este archivo', on_result=self.handler_delete_file, id="dialog")
        sidebar.mount(container)
        sidebar.refresh(repaint= True, layout=True)
        

    async def action_create_file(self) -> None:
        # Mostrar input para nombre de archivo
        await self.prompt("Ingrese el nombre del archivo:")


    async def prompt(self, prompt_text: str) -> str:
        # Función para mostrar input modal para nombre de archivo
        sidebar = self.app.query_one('#sidebar',Vertical)
        input_widget = KmInput(placeholder=prompt_text, path=self.aux_path)
        container = Horizontal(input_widget)
        container.id = "input_container"
        sidebar.mount(container)
        sidebar.refresh(repaint= True, layout=True)
        input_widget.focus()
