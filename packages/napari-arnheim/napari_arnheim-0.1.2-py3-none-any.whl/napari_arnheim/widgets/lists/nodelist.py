


from napari_arnheim.widgets.items.nodeitem import NodeItemWidget
from PyQt5.QtWidgets import QVBoxLayout
from bergen.schema import Node
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QSizePolicy, QWidget
from PyQt5 import QtCore
import typing

from grunnlag.schema import Representation

class NodeListWidget(QWidget):


    def __init__(self, nodes: typing.List[Node] , title=None,  viewer = None, **kwargs) -> None:
        super().__init__(**kwargs)

        self.list = QListWidget()

        for node in nodes:

            item = QListWidgetItem(self.list)
            self.list.addItem(item)
            nodewidget = NodeItemWidget(node, viewer=viewer)
            item.setSizeHint(nodewidget.minimumSizeHint())
            self.list.setItemWidget(item, nodewidget)

        self.layout = QVBoxLayout(self)
        if title:
            self.layout.addWidget(QLabel(title))
        self.layout.addWidget(self.list)





