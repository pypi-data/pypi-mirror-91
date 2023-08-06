from napari_arnheim.auths.implicit.backend import ImplicitApplication
import os
from bergen.clients.base import BaseBergen
from bergen.clients.mixins.querymixin import QueryMixIn
from bergen.clients.mixins.subscribemixin import SubscribeMixIn
from bergen.wards.graphql.subscription import SubscriptionGraphQLWard


class Bergen(BaseBergen, QueryMixIn, SubscribeMixIn):

    def __init__(self, client_id = None, host: str = "localhost", port: int = 8000, protocol="http", bind=True, allow_insecure=None, is_local=None, **kwargs) -> None:

        
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" if allow_insecure is not None else os.getenv("OAUTHLIB_INSECURE_TRANSPORT", "0")
        os.environ["ARNHEIM_LOCAL"] = "0" if is_local is not None else os.getenv("ARNHEIM_LOCAL", "0")


        auth = ImplicitApplication(client_id=client_id, host=host, port=port, protocol=protocol)
        main_ward = SubscriptionGraphQLWard(host=host, port=port, protocol=protocol, token=auth.getToken())

        super().__init__(auth, main_ward, auto_negotiate=True, bind=bind, **kwargs)