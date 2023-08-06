


from napari_arnheim.registries.napari import get_current_viewer
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QWidget
from grunnlag.schema import Representation
from napari.viewer import Viewer

class RepresentationItemWidget(QWidget):
    def __init__(self, rep: Representation, viewer: Viewer = None, parent=None, napari=None):
        super(RepresentationItemWidget, self).__init__(parent)
        self.rep = rep
        self.viewer: Viewer = viewer


        self.row = QHBoxLayout()


        self.row.addWidget(QLabel(self.rep.name))


        self.open2DButton = QPushButton("Open")
        self.open2DButton.clicked.connect(self.open2D)
        self.row.addWidget(self.open2DButton)

        #self.open3DButton = QPushButton("3D")
        #self.open3DButton.clicked.connect(self.open3D)
        #self.row.addWidget(self.open3DButton)

        self.setLayout(self.row)


    def open2D(self):
        print(self.rep.name)
        print(self.rep.id)
        self.viewer.add_image(self.rep.data.sel(c=0).data, name=self.rep.name, metadata={"rep": self.rep})



        