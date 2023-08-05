from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget
from bergen import Bergen
from bergen.query import TypedGQL
from grunnlag.schema import Representation
import xarray as xr
from functools import partial

class ArnheimWidget(QWidget):

    def __init__(self, *args, bergen: Bergen = None, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.status = QLabel(self)
        self.status.text = "Arnheim"
        layout.addWidget(self)
        self.upload_button = QPushButton("Upload")
        self.upload_button.clicked.connect(self.uploadImage)


        self.bergen = bergen or Bergen(host="p-tnagerl-lab1",
        port=8000,
        client_id="y1W8JK5OgpAexf68eqbHIx60228rTBc4moNlaKYN", 
        client_secret="ovChuVgIFFQcNT3buPbm5AVjGCJGHBQZOQTqhvzwP02IllfJRVj17efit6aGqPcd01AJPY1SCc8kTBM22pistp8A1BRQRmtgX9Nycd2LcN1YEduhjpSY9mq5Pm2nV0xi",
        name="karl",# if we want to specifically only use pods on this innstance we would use that it in the selector
        )

        layout.addWidget(self.upload_button)
        layout.addWidget(self.buildList())
    
    @property
    def viewer(self):
        if hasattr(self.parent(), "qt_viewer"):
            return self.parent().qt_viewer.viewer
        return None


    def buildList(self):

        it = TypedGQL("""
        query Representations {
            representations{
                id
                name
                store
            }
        }
        """, Representation).run({})


        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        for item in it[:5]:
            insert_item = QPushButton(item.name)
            insert_item.clicked.connect(partial(self.openRepresentation, item, threed=True))
            layout.addWidget(insert_item)

        return widget


    def uploadImage(self):

        active_image = self.viewer.active_layer
        
        array = active_image.data

        x = None
        if array.ndim == 2: x = array.reshape(array.shape + (1,1,1))
        if array.ndim == 3: x = array.reshape(array.shape + (1,1))
        if array.ndim == 4: x = array.reshape(array.shape + (1,))
        if array.ndim == 5: x = array.reshape(array.shape)
  
        assert x is not None
        therarray = xr.DataArray(x, dims=list("xyzct"))
        rep = Representation.objects.from_xarray(therarray, name="rama", sample=1)
        print(rep)
        return None


    def openRepresentation(self, item: Representation, threed=False):
        print(item.name)
        print(item.id)
        self.viewer.add_image(item.data.sel(c=0).data)