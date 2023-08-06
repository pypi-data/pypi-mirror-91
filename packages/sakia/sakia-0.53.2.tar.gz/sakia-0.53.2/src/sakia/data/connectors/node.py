import asyncio
import logging
import time
import re
from asyncio import TimeoutError
from socket import gaierror
from typing import Union

import aiohttp
import jsonschema
from PyQt5.QtCore import QObject, pyqtSignal
from aiohttp import ClientError

from duniterpy.api import bma, errors
from duniterpy.api.client import Client
from duniterpy.constants import HOST_REGEX, IPV4_REGEX, IPV6_REGEX
from duniterpy.api.endpoint import BMAEndpoint, SecuredBMAEndpoint
from duniterpy.documents import BlockUID, MalformedDocumentError
from duniterpy.documents.peer import Peer
from sakia.decorators import asyncify
from sakia.errors import InvalidNodeCurrency
from ..entities.node import Node


class NodeConnectorLoggerAdapter(logging.LoggerAdapter):
    """
    This example adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """

    def process(self, msg, kwargs):
        return "[%s] %s" % (self.extra["pubkey"][:5], msg), kwargs


class NodeConnector(QObject):
    """
    A node is a peer send from the client point of view.
    """

    changed = pyqtSignal()
    success = pyqtSignal()
    failure = pyqtSignal(int)
    identity_changed = pyqtSignal()
    neighbour_found = pyqtSignal(Peer)
    block_found = pyqtSignal(BlockUID)

    def __init__(self, node, user_parameters, session=None):
        """
        Constructor
        """
        super().__init__()
        self.node = node
        self.failure_count = 0
        self._ws_tasks = {"block": None, "peer": None}
        self._connected = {"block": False, "peer": False}
        self._user_parameters = user_parameters
        self._raw_logger = logging.getLogger("sakia")
        self._logger = NodeConnectorLoggerAdapter(
            self._raw_logger, {"pubkey": self.node.pubkey}
        )

    def __del__(self):
        for ws in self._ws_tasks.values():
            if ws:
                ws.cancel()

    @classmethod
    async def from_address(cls, currency, secured, address, port, user_parameters):
        """
        Factory method to get a node from a given address
        :param str currency: The node currency. None if we don't know\
         the currency it should have, for example if its the first one we add
        :param bool secured: True if the node uses https
        :param str address: The node address
        :param int port: The node port
        :return: A new node
        :rtype: sakia.core.net.Node
        """
        endpoint = get_bma_endpoint_from_server_address(address, port, secured)

        async with aiohttp.ClientSession() as session:
            # Create Client from endpoint string in Duniter format
            client = Client(endpoint, session, proxy=user_parameters.proxy())
            peer_data = client(bma.network.peering)

        peer = Peer.from_signed_raw(
            "{0}{1}\n".format(peer_data["raw"], peer_data["signature"])
        )

        if currency and peer.currency != currency:
            raise InvalidNodeCurrency(currency, peer.currency)

        node = Node(
            peer.currency,
            peer.pubkey,
            peer.endpoints,
            peer.blockUID,
            last_state_change=time.time(),
        )
        logging.getLogger("sakia").debug("Node from address: {:}".format(str(node)))

        return cls(node, user_parameters)

    @classmethod
    def from_peer(cls, currency, peer, user_parameters):
        """
        Factory method to get a node from a peer document.

        :param str currency: The node currency. None if we don't know\
         the currency it should have, for example if its the first one we add
        :param peer: The peer document
        :return: A new node
        :rtype: sakia.core.net.Node
        """
        if currency and peer.currency != currency:
            raise InvalidNodeCurrency(currency, peer.currency)

        node = Node(
            peer.currency,
            peer.pubkey,
            peer.endpoints,
            peer.blockUID,
            current_buid=peer.blockUID,
            last_state_change=time.time(),
        )
        logging.getLogger("sakia").debug("Node from peer: {:}".format(str(node)))

        return cls(node, user_parameters, session=None)

    async def safe_request(self, endpoint, request, proxy, req_args={}):
        async with aiohttp.ClientSession() as session:
            try:
                client = Client(endpoint, session, proxy)
                data = await client(request, **req_args)
                return data
            except errors.DuniterError as e:
                if e.ucode == 1006:
                    self._logger.debug("{0}".format(str(e)))
                else:
                    raise
            except (
                ClientError,
                gaierror,
                TimeoutError,
                ConnectionRefusedError,
                ValueError,
            ) as e:
                self._logger.debug("{:}:{:}".format(str(e.__class__.__name__), str(e)))
                self.handle_failure()
            except jsonschema.ValidationError as e:
                self._logger.debug("{:}:{:}".format(str(e.__class__.__name__), str(e)))
                self.handle_failure(weight=3)
            except RuntimeError as e:
                self._logger.error(str(e))
            except AttributeError as e:
                if "feed_appdata" in str(e) or "do_handshake" in str(e):
                    self._logger.debug(str(e))
                else:
                    raise

    async def close_ws(self):
        for ws in self._ws_tasks.values():
            if ws:
                ws.cancel()
        closed = False
        while not closed:
            for ws in self._ws_tasks.values():
                if ws:
                    closed = False
                    break
            else:
                closed = True
            await asyncio.sleep(0)
        await asyncio.sleep(0)

    def refresh(self, manual=False):
        """
        Refresh all data of this node
        :param bool manual: True if the refresh was manually initiated
        """
        if not self._ws_tasks["block"]:
            self._ws_tasks["block"] = asyncio.ensure_future(
                self.connect_current_block()
            )

        if not self._ws_tasks["peer"]:
            self._ws_tasks["peer"] = asyncio.ensure_future(self.connect_peers())

        if manual:
            asyncio.ensure_future(self.request_peers())

    async def connect_current_block(self):
        """
        Connects to the websocket entry point of the node
        If the connection fails, it tries the fallback mode on HTTP GET
        """
        for endpoint in [e for e in self.node.endpoints if isinstance(e, BMAEndpoint)]:
            if not self._connected["block"]:
                async with aiohttp.ClientSession() as session:
                    try:
                        client = Client(
                            endpoint, session, self._user_parameters.proxy()
                        )

                        # Create Web Socket connection on block path (async method)
                        ws = await client(bma.ws.block)  # Type: WSConnection
                        self._connected["block"] = True
                        self._logger.debug("Connected successfully to block ws")

                        loop = True
                        # Iterate on each message received...
                        while loop:
                            # Wait and capture next message
                            try:
                                block_data = await ws.receive_json()
                                jsonschema.validate(block_data, bma.ws.WS_BLOCK_SCHEMA)
                                self._logger.debug("Received a block")
                                self.block_found.emit(
                                    BlockUID(block_data["number"], block_data["hash"])
                                )
                            except TypeError as exception:
                                self._logger.debug(exception)
                                self.handle_failure()
                                break

                    except (aiohttp.WSServerHandshakeError, ValueError) as e:
                        self._logger.debug(
                            "Websocket block {0}: {1}".format(type(e).__name__, str(e))
                        )
                        self.handle_failure()
                    except (ClientError, gaierror, TimeoutError) as e:
                        self._logger.debug(
                            "{0}: {1}".format(str(e), self.node.pubkey[:5])
                        )
                        self.handle_failure()
                    except jsonschema.ValidationError as e:
                        self._logger.debug(
                            "{:}:{:}".format(str(e.__class__.__name__), str(e))
                        )
                        self.handle_failure(weight=3)
                    except RuntimeError as e:
                        self._logger.error(str(e))
                    except AttributeError as e:
                        if "feed_appdata" in str(e) or "do_handshake" in str(e):
                            self._logger.debug(str(e))
                        else:
                            raise
                    finally:
                        self._connected["block"] = False
                        self._ws_tasks["block"] = None

    async def connect_peers(self):
        """
        Connects to the peer websocket entry point
        If the connection fails, it tries the fallback mode on HTTP GET
        """
        for endpoint in [e for e in self.node.endpoints if isinstance(e, BMAEndpoint)]:
            if not self._connected["peer"]:
                async with aiohttp.ClientSession() as session:
                    try:
                        client = Client(
                            endpoint, session, self._user_parameters.proxy()
                        )

                        # Create Web Socket connection on peer path (async method)
                        ws = await client(bma.ws.peer)  # Type: WSConnection
                        self._connected["peer"] = True
                        self._logger.debug("Connected successfully to peer ws")

                        loop = True
                        # Iterate on each message received...
                        while loop:
                            try:
                                # Wait and capture next message
                                peer_data = await ws.receive_json()
                                jsonschema.validate(peer_data, bma.ws.WS_PEER_SCHEMA)
                                self._logger.debug("Received a peer")
                                self.refresh_peer_data(peer_data)
                            except TypeError as exception:
                                self._logger.debug(exception)
                                break

                        # Close session
                        await client.close()

                    except (aiohttp.WSServerHandshakeError, ValueError) as e:
                        self._logger.debug(
                            "Websocket peer {0}: {1}".format(type(e).__name__, str(e))
                        )
                        await self.request_peers()
                    except (ClientError, gaierror, TimeoutError) as e:
                        self._logger.debug(
                            "{:}:{:}".format(str(e.__class__.__name__), str(e))
                        )
                        self.handle_failure()
                    except jsonschema.ValidationError as e:
                        self._logger.debug(
                            "{:}:{:}".format(str(e.__class__.__name__), str(e))
                        )
                        self.handle_failure(weight=3)
                    except RuntimeError as e:
                        self._logger.error(str(e))
                    except AttributeError as e:
                        if "feed_appdata" in str(e) or "do_handshake" in str(e):
                            self._logger.debug(str(e))
                        else:
                            raise
                    finally:
                        self._connected["peer"] = False
                        self._ws_tasks["peer"] = None

    async def request_peers(self):
        """
        Refresh the list of peers knew by this node
        """
        found_peer_data = False
        for endpoint in [e for e in self.node.endpoints if isinstance(e, BMAEndpoint)]:
            try:
                peers_data = await self.safe_request(
                    endpoint,
                    bma.network.peers,
                    req_args={"leaves": "true"},
                    proxy=self._user_parameters.proxy(),
                )
                if not peers_data:
                    continue
                if peers_data["root"] != self.node.merkle_peers_root:
                    leaves = [
                        leaf
                        for leaf in peers_data["leaves"]
                        if leaf not in self.node.merkle_peers_leaves
                    ]
                    for leaf_hash in leaves:
                        try:
                            leaf_data = await self.safe_request(
                                endpoint,
                                bma.network.peers,
                                proxy=self._user_parameters.proxy(),
                                req_args={"leaf": leaf_hash},
                            )
                            if not leaf_data:
                                break
                            self.refresh_peer_data(leaf_data["leaf"]["value"])
                            found_peer_data = True
                        except (AttributeError, ValueError) as e:
                            if "feed_appdata" in str(e) or "do_handshake" in str(e):
                                self._logger.debug(str(e))
                            else:
                                self._logger.debug(
                                    "Incorrect peer data in {leaf}: {err}".format(
                                        leaf=leaf_hash, err=str(e)
                                    )
                                )
                                self.handle_failure()
                        except errors.DuniterError as e:
                            if e.ucode == 2012:
                                # Since with multinodes, peers or not the same on all nodes, sometimes this request results
                                # in peer not found error
                                self._logger.debug(
                                    "{:}:{:}".format(str(e.__class__.__name__), str(e))
                                )
                            else:
                                self.handle_failure()
                                self._logger.debug(
                                    "Incorrect peer data in {leaf}: {err}".format(
                                        leaf=leaf_hash, err=str(e)
                                    )
                                )
                    else:
                        self.node.merkle_peers_root = peers_data["root"]
                        self.node.merkle_peers_leaves = tuple(peers_data["leaves"])
                return  # Break endpoints loop
            except errors.DuniterError as e:
                self._logger.debug("Error in peers reply: {0}".format(str(e)))
                self.handle_failure()
        else:
            if not found_peer_data:
                self._logger.debug("Could not connect to any BMA endpoint")
                self.handle_failure()

    def refresh_peer_data(self, peer_data):
        if "raw" in peer_data:
            try:
                str_doc = "{0}{1}\n".format(peer_data["raw"], peer_data["signature"])
                peer_doc = Peer.from_signed_raw(str_doc)
                self.neighbour_found.emit(peer_doc)
            except MalformedDocumentError as e:
                self._logger.debug("{:}:{:}".format(str(e.__class__.__name__), str(e)))
        else:
            self._logger.debug("Incorrect leaf reply")

    async def request_ws2p_heads(self):
        """
        Refresh the list of peers knew by this node
        """
        for endpoint in [e for e in self.node.endpoints if isinstance(e, BMAEndpoint)]:
            try:
                heads_data = await self.safe_request(
                    endpoint,
                    bma.network.ws2p_heads,
                    proxy=self._user_parameters.proxy(),
                )
                if not heads_data:
                    continue
                self.handle_success()
                self._logger.debug(
                    "Connection to BMA succeeded (%s,%s,%s)",
                    endpoint.server,
                    endpoint.port,
                    endpoint.API,
                )
                return heads_data  # Break endpoints loop
            except errors.DuniterError as e:
                self._logger.debug("Error in peers reply: {0}".format(str(e)))
                self.handle_failure()
        else:
            self._logger.debug("Could not connect to any BMA endpoint")
            self.handle_failure()

    def handle_success(self):
        self.success.emit()

    def handle_failure(self, weight=1):
        self.failure.emit(weight)


def get_bma_endpoint_from_server_address(
    address: str, port: int, secured: bool
) -> Union[BMAEndpoint, SecuredBMAEndpoint]:
    """
    Return a BMA Endpoint from server address parameters

    :param address: Domain Name or IPV4 ou IPV6
    :param port: Port number
    :param secured: True if SSL secured
    :return:
    """
    server = ""
    ipv4 = ""
    ipv6 = ""
    if re.compile(HOST_REGEX).match(address):
        server = address
    elif re.compile(IPV4_REGEX).match(address):
        ipv4 = address
    elif re.compile(IPV6_REGEX).match(address):
        ipv6 = address

    if secured:
        endpoint = SecuredBMAEndpoint(server, ipv4, ipv6, port, "")
    else:
        endpoint = BMAEndpoint(server, ipv4, ipv6, port)

    return endpoint
