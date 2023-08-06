
from napari_arnheim.widgets import ArnheimWidget
import napari


def main():
    
    with napari.gui_qt():
        viewer = napari.Viewer()
        viewer.window.add_dock_widget(ArnheimWidget(), area="right")

