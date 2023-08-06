from abc import abstractmethod

from PyQt5 import QtCore
from oauthlib.oauth2.rfc6749.clients.mobile_application import MobileApplicationClient
from requests_oauthlib.oauth2_session import OAuth2Session
from napari_arnheim.auths.implicit.widgets.login import LoginDialog
from bergen.auths.base import BaseAuthBackend
from bergen.enums import ClientType

class ImplicitError(Exception):
    pass


class ImplicitApplication(BaseAuthBackend):


    def __init__(self, client_id = None, redirect_uri = "http://localhost:3000/callback", host="localhost", port= 8000, protocol = "http", scopes= ["read"], parent=None) -> None:
        self.client_id = client_id
        assert self.client_id is not None, "Please provide a client_id argument"
        # TESTED, just redirecting to Google works in normal browsers
        # the token string appears in the url of the address bar
        self.redirect_uri = redirect_uri

        # Generate correct URLs
        self.base_url = f"{protocol}://{host}:{port}/o/"
        self.auth_url = self.base_url + "authorize"
        self.token_url = self.base_url + "token"

        # If you want to have a hosting QtWidget
        self.parent = parent

        self.token = None

        self.mobile_app_client = MobileApplicationClient(client_id)

        # Create an OAuth2 session for the OSF
        self.session = OAuth2Session(
            client_id, 
            self.mobile_app_client,
            scope=" ".join(scopes), 
            redirect_uri=self.redirect_uri,
        )


        super().__init__()

    def getToken(self) -> str:
        if not self.token:
            token, result = LoginDialog.getToken(backend=self, parent=self.parent)
            if result:
                self.token = token
            else:
                raise ImplicitError("Couldn't return a proper token")

        
        return self.token


    def getClientType(self):
        return ClientType.EXTERNAL

    def getProtocol(self):
        return "http"