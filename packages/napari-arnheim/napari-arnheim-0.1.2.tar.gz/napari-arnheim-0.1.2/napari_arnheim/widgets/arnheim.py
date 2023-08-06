from napari_arnheim.widgets.lists.nodelist import NodeListWidget
from bergen.schema import Node, User
from napari_arnheim.widgets.lists.replist import RepresentationListWidget
from napari_arnheim.registries.napari import set_current_viewer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget
from bergen.clients.default import Bergen
from bergen.query import TypedGQL
from grunnlag.schema import Representation
import xarray as xr
from functools import partial
from bergen.enums import GrantType


class ArnheimWidget(QWidget):

    def __init__(self, bind_viewer=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout(self)
        self.status = QLabel(self)
        self.status.text = "Arnheim"
        self.layout.addWidget(self)

        self.bergen = None

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connectBergen)

        self.layout.addWidget(self.connect_button)


    def connectBergen(self):
        if not self.bergen:
            self.bergen = Bergen(host="p-tnagerl-lab1",
                client_id= "F7YSSjtQd3uQQHdDZ5kEMLEejRHgwjsWgkVBb7Zz",
                port=8000,
                name="karl",
                grant_type = GrantType.IMPLICIT
                # if we want to specifically only use pods on this innstance we would use that it in the selector
            )

            self.layout.addWidget(self.buildUserInfo())
            self.layout.addWidget(self.buildList())
            self.layout.addWidget(self.buildNodeHost())
            print(self.viewer.events)

        


    
    @property
    def viewer(self):
        if hasattr(self.parent(), "qt_viewer"):
            return self.parent().qt_viewer.viewer
        return None


    def buildList(self):

        it = TypedGQL("""
        query Representations {
            myrepresentations{
                id
                name
                store
            }
        }
        """, Representation).run({})


        widget = RepresentationListWidget(it, title="My latest Representations" , viewer=self.viewer)
        return widget

    def buildUserInfo(self):

        user = TypedGQL("""
        query {
                me {
                    id
                    username
                }
        }
        """, User).run({})


        widget = QLabel(user.username)
        return widget


    def buildNodeHost(self):

        it = TypedGQL("""
            query Nodes{
                nodesformodel(models: ["representation"]){
                    id
                    name
                }
            }
        """, Node).run({})


        widget = NodeListWidget(it, title="Available Nodes", viewer=self.viewer)
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