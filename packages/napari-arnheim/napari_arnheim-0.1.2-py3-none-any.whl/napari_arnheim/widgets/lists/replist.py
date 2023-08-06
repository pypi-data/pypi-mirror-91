


from PyQt5.QtWidgets import QVBoxLayout
from napari_arnheim.widgets.items.representaiton import RepresentationItemWidget
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QSizePolicy, QWidget
from PyQt5 import QtCore
import typing

from grunnlag.schema import Representation

class RepresentationListWidget(QWidget):


    def __init__(self, representations: typing.List[Representation] , title=None,  viewer = None, **kwargs) -> None:
        super().__init__(**kwargs)

        self.list = QListWidget()

        for rep in representations:

            item = QListWidgetItem(self.list)
            self.list.addItem(item)
            repwidget = RepresentationItemWidget(rep, viewer=viewer)
            item.setSizeHint(repwidget.minimumSizeHint())
            self.list.setItemWidget(item, repwidget)

        self.layout = QVBoxLayout(self)
        if title:
            self.layout.addWidget(QLabel(title))
        self.layout.addWidget(self.list)





