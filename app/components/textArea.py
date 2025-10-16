from textual.widgets import TextArea

class KmTextArea(TextArea):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        # Actualiza el widget Markdown según lo que se escribe
        file_path = self.app.file_path
        file = open(file_path, 'w')
        file.write(event.text_area.text)
