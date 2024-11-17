# create globel vars fro the image path 
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

settings = {
     "path"              : None ,
     "models_paths"      : BASE_DIR.parent/"models",
     "BASE_DIR"          : BASE_DIR,
}

def get_path():
     return settings['path']

def set_path(text:str=None):
     settings['path'] = text

def clear_layout(layout):
    """Recursively clear all widgets and sub-layouts from a layout."""
    if layout is not None:
        while layout.count():
            print("clearing layout: ", layout)
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                clear_layout(item.layout())