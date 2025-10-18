from app.components.dialog_input import DialogInput
from textual.widgets import DirectoryTree, Static, TextArea
from textual.containers import Horizontal, Vertical, Container
from app.components.dialog import Dialog
from app.components.input import KmInput
import os
import shutil


class KmDirectoryTree(DirectoryTree):
    aux_path = None
    BINDINGS = [
        ("ctrl+n", "create_file", "Create a new file"),
        ("ctrl+d", "delete_file", "Delete a new file"),
        ("j", "cursor_down", "Move down"),
        ("k", "cursor_up", "Move up"),
        ("l", "select_cursor", "Select cursor"),
    ]

    def on_directory_tree_file_selected(self, event) -> None:
        if os.path.exists(event.path):
            try:
                if os.path.isfile(event.path) and os.path.splitext(event.path)[1] in [
                    ".md"
                ]:
                    self.app.file_path = event.path
                    editor = self.app.query_one("#editor", TextArea)
                    editor.text = open(event.path, "r").read()
                    editor.focus()
            except Exception as e:
                self.app.notify(f"archivo no valido {e}")

    def on_directory_tree_directory_selected(self, event) -> None:
        self.aux_path = event.path

    def handler_delete_file(self, variant):
        if variant == "success":
            if self.cursor_node and self.cursor_node.data:
                path = self.cursor_node.data.path
                if os.path.exists(path) and str(path) != ".":
                    try:
                        if os.path.isfile(path):
                            os.remove(path)
                            self.app.notify(f"Archivo eliminado: {path}")
                        elif os.path.isdir(path):
                            shutil.rmtree(path)
                            self.app.notify(f"Directorio eliminado: {path}")
                        tree = self.app.query_one("#directory_tree", KmDirectoryTree)
                        tree.reload()
                    except Exception as e:
                        self.app.notify(f"Error al eliminar: {e}")
                else:
                    self.app.notify("No se puede eliminar esta archivo o directorio")
            else:
                self.app.notify("No hay archivo o directorio seleccionado")

    async def action_delete_file(self) -> None:
        sidebar = self.app.query_one("#sidebar", Vertical)
        container = Dialog(
            Text="Desea eliminar este archivo",
            on_result=self.handler_delete_file,
            id="dialog",
        )
        sidebar.mount(container)
        sidebar.refresh(repaint=True, layout=True)

    async def action_create_file(self) -> None:
        # Mostrar input para nombre de archivo
        sidebar = self.app.query_one("#sidebar", Vertical)
        container = DialogInput(
            placeholder="Ingrese el nombre del archivo:",
            on_summit=self.handler_create_file,
            id="dialog",
        )
        sidebar.mount(container)
        sidebar.refresh(repaint=True, layout=True)

    def handler_create_file(self, file_name: str) -> None:
        container = self.app.query_one("#dialog", Container)
        container.remove()
        current_path = os.getcwd()
        base_path = "" if self.aux_path is None else self.aux_path
        file_path = os.path.join(current_path, base_path, file_name)

        # Comprobar si termina en '/' -> crear directorio
        is_dir = file_name.endswith("/")

        # Ajustar ruta para directorio (sin '/')
        if is_dir:
            file_path = file_path.rstrip("/")

        # Validar existencia y manejar sufijo _x
        original_path = file_path
        count = 1
        while os.path.exists(file_path):
            if is_dir:
                file_path = f"{original_path}_{count}"
            else:
                # Para archivos separar nombre y extensión
                name, ext = os.path.splitext(original_path)
                file_path = f"{name}_{count}{ext}"
            count += 1

        # Crear carpeta o archivo según corresponda
        if is_dir:
            os.makedirs(file_path)
        else:
            with open(file_path, "w") as f:
                f.write("")

        self.reload()
        self.app.notify(
            f"{file_path}", title="Directory created" if is_dir else "File created"
        )
