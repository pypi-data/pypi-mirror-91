


from napari_arnheim.widgets.error.error import ErrorDialog
from bergen.schema import Node
from napari_arnheim.registries.napari import get_current_viewer
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QWidget
from grunnlag.schema import Representation
from napari.viewer import Viewer
import asyncio


class NodeItemWidget(QWidget):
    def __init__(self, node: Node, viewer: Viewer = None, parent=None, napari=None):
        super(NodeItemWidget, self).__init__(parent)
        self.node = node
        self.viewer: Viewer = viewer


        self.row = QHBoxLayout()


        self.row.addWidget(QLabel(self.node.name))


        self.open2DButton = QPushButton("Run")
        self.open2DButton.clicked.connect(self.run)
        self.row.addWidget(self.open2DButton)

        #self.open3DButton = QPushButton("3D")
        #self.open3DButton.clicked.connect(self.open3D)
        #self.row.addWidget(self.open3DButton)

        self.setLayout(self.row)


    def run(self):
        active_image = self.viewer.active_layer
        if active_image is None: return ErrorDialog.alert("No Layer selected")
        meta = active_image.metadata
        if "rep" in meta:
            # We are dealing with an Image
            print(asyncio.get_event_loop())
            try:

                result = print(self.node.assign({"rep": meta["rep"]}, nana=True))
            except Exception as e:
                ErrorDialog.alert(e)
        else:
            return ErrorDialog.alert("The Layer you selected is not a ArnheimModel")


        print(active_image)



        