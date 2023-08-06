import attr
from PyQt5.QtCore import QObject
from sakia.data.processors import (
    BlockchainProcessor,
    SourcesProcessor,
    ConnectionsProcessor,
    ContactsProcessor,
)
from sakia.money.base_referential import BaseReferential


@attr.s()
class TransferModel(QObject):
    """
    The model of transfer component

    :param sakia.app.Application app:
    :param sakia.data.entities.Connection connection:
    :param sakia.data.processors.BlockchainProcessor _blockchain_processor:
    """

    app = attr.ib()
    connection = attr.ib(default=None)
    resent_transfer = attr.ib(default=None)
    current_source = attr.ib(default=None)
    _blockchain_processor = attr.ib(default=None)
    _sources_processor = attr.ib(default=None)
    _connections_processor = attr.ib(default=None)

    def __attrs_post_init__(self):
        super().__init__()
        self._blockchain_processor = BlockchainProcessor.instanciate(self.app)
        self._sources_processor = SourcesProcessor.instanciate(self.app)
        self._connections_processor = ConnectionsProcessor.instanciate(self.app)
        self._contacts_processor = ContactsProcessor.instanciate(self.app)

    def referential_to_quantitative(self, value):
        """
        Get the quantitative value of a referential amount
        :param float value:
        :rtype: int
        """
        referential = self.app.current_ref(
            0, self.app.currency, self.app
        )  # type: BaseReferential
        referential.set_diff_referential(value)
        # amount is rounded to the nearest power of 10 depending of last ud base
        # rounded = int(pow(10, base) * round(float(amount) / pow(10, base)))
        return int(referential.amount)

    def quantitative_to_referential(self, value):
        """
        Get the referential value of a given amount
        :param int value:
        :rtype: float
        """
        referential = self.app.current_ref(
            value * 100, self.app.currency, self.app
        )  # type: BaseReferential
        return referential.differential()

    def wallet_value(self):
        """
        Get the value of the current wallet in the current community
        """
        return self._sources_processor.amount(
            self.connection.currency, self.connection.pubkey
        )

    def current_base(self):
        """
        Get the current base of the network
        """
        dividend, base = self._blockchain_processor.last_ud(self.connection.currency)
        return base

    def localized_amount(self, amount):
        """
        Get the value of the current referential
        """
        localized = self.app.current_ref.instance(
            amount, self.connection.currency, self.app
        ).diff_localized(False, True)
        return localized

    def cancel_previous(self):
        if self.resent_transfer:
            self.resent_transfer.cancel()

    def available_connections(self):
        return self._connections_processor.connections()

    def set_connection(self, index):
        connections = self._connections_processor.connections()
        self.connection = connections[index]

    async def send_money(
        self,
        recipient,
        secret_key,
        password,
        amount,
        amount_base,
        comment,
        lock_mode,
        source,
    ):
        """
        Send money to given recipient using the account
        :param lock_mode:
        :param str recipient:
        :param str password:
        :param str secret_key:
        :param int amount:
        :param int amount_base:
        :param str comment:
        :param int lock_mode:
        :param Source source:
        :return: the result of the send
        """

        result, transactions = await self.app.documents_service.send_money(
            self.connection,
            secret_key,
            password,
            recipient,
            amount,
            amount_base,
            comment,
            lock_mode,
            source,
        )
        for transaction in transactions:
            self.app.sources_service.parse_transaction_outputs(
                self.connection.pubkey, transaction
            )
            for conn in self._connections_processor.connections():
                if conn.pubkey == recipient:
                    self.app.sources_service.consume_sources_from_transaction_inputs(
                        recipient, transaction
                    )
                    new_tx = self.app.transactions_service.parse_sent_transaction(
                        recipient, transaction
                    )
                    # Not all connections are concerned by chained tx
                    if new_tx:
                        self.app.new_transfer.emit(conn, new_tx)
            self.app.sources_refreshed.emit()
            self.app.db.commit()
        return result, transactions

    def notifications(self):
        return self.app.parameters.notifications

    def connection_pubkey(self, index):
        return self.available_connections()[index].pubkey

    def contacts(self):
        return self._contacts_processor.contacts()
