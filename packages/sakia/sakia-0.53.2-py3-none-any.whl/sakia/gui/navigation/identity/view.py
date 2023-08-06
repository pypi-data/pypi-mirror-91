from PyQt5.QtWidgets import QWidget, QMessageBox, QAbstractItemView, QHeaderView
from PyQt5.QtCore import (
    QEvent,
    QLocale,
    pyqtSignal,
    Qt,
    QDateTime,
    QCoreApplication,
    QObject,
)

from sakia.app import Application
from .identity_uic import Ui_IdentityWidget
from enum import Enum
from sakia.helpers import timestamp_to_dhms
from sakia.gui.widgets.dialogs import dialog_async_exec
from ...sub.certification.view import CertificationView


class IdentityView(QWidget, Ui_IdentityWidget):
    """
    The view of navigation panel
    """

    retranslate_required = pyqtSignal()

    class CommunityState(Enum):
        NOT_INIT = 0
        OFFLINE = 1
        READY = 2

    def __init__(
        self, parent: QObject, certification_view: CertificationView, app: Application
    ):
        """
        Init IdentityView
        :param parent: QObject instance
        :param certification_view: CertificationView instance
        :param app: Application instance
        """
        super().__init__(parent)
        self.app = app
        self.certification_view = certification_view
        self.setupUi(self)
        self.stacked_widget.insertWidget(1, certification_view)
        self.button_certify.clicked.connect(
            lambda c: self.stacked_widget.setCurrentWidget(self.certification_view)
        )

    def set_table_identities_model(self, model):
        """
        Set the model of the table view
        :param PyQt5.QtCore.QAbstractItemModel model: the model of the table view
        """
        self.table_certifiers.setModel(model)
        self.table_certifiers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_certifiers.setSortingEnabled(True)
        self.table_certifiers.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )
        self.table_certifiers.resizeRowsToContents()
        self.table_certifiers.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.table_certifiers.setContextMenuPolicy(Qt.CustomContextMenu)

    def clear(self):
        self.stacked_widget.setCurrentWidget(self.page_empty)

    def set_simple_informations(self, data, state):
        if state in (
            IdentityView.CommunityState.NOT_INIT,
            IdentityView.CommunityState.OFFLINE,
        ):
            self.label_currency.setText(
                """<html>
                <body>
                <p>
                <span style=" font-size:16pt; font-weight:600;">{currency}</span>
                </p>
                <p>{message}</p>
                </body>
                </html>""".format(
                    currency=data["currency"],
                    message=IdentityView.simple_message[state],
                )
            )
            self.button_membership.hide()
        else:
            if data["written"]:
                written_value = QCoreApplication.translate(
                    "IdentityView", "Identity written in blockchain"
                )
                pass
            else:
                expiration_text = QLocale.toString(
                    QLocale(),
                    QDateTime.fromTime_t(data["idty_expiration"]),
                    QLocale.dateTimeFormat(QLocale(), QLocale.ShortFormat),
                )
                written_value = (
                    QCoreApplication.translate(
                        "IdentityView", "Identity not written in blockchain"
                    )
                    + " ("
                    + QCoreApplication.translate(
                        "IdentityView", "Expires on: {0}"
                    ).format(expiration_text)
                    + " BAT)"
                )

            status_value = (
                QCoreApplication.translate("IdentityView", "Member")
                if data["membership_state"]
                else QCoreApplication.translate("IdentityView", "Not a member")
            )
            if data["mstime"] > 0:
                membership_action_value = QCoreApplication.translate(
                    "IdentityView", "Renew membership"
                )
                status_info = ""
                membership_action_enabled = True
            elif data["membership_state"]:
                membership_action_value = QCoreApplication.translate(
                    "IdentityView", "Renew membership"
                )
                status_info = "Your membership expired"
                membership_action_enabled = True
            else:
                membership_action_value = QCoreApplication.translate(
                    "IdentityView", "Request membership"
                )
                if data["nb_certs"] > data["nb_certs_required"]:
                    status_info = QCoreApplication.translate(
                        "IdentityView", "Identity registration ready"
                    )
                    membership_action_enabled = True
                else:
                    status_info = QCoreApplication.translate(
                        "IdentityView", "{0} more certifications required"
                    ).format(data["nb_certs_required"] - data["nb_certs"])
                    membership_action_enabled = True

            if data["mstime"] > 0:
                days, hours, minutes, seconds = timestamp_to_dhms(data["mstime"])
                mstime_remaining_text = QCoreApplication.translate(
                    "IdentityView", "Expires in "
                )
                if days > 0:
                    mstime_remaining_text += QCoreApplication.translate(
                        "IdentityView", "{days} days"
                    ).format(days=days)
                else:
                    mstime_remaining_text += QCoreApplication.translate(
                        "IdentityView", "{hours} hours and {min} min."
                    ).format(hours=hours, min=minutes)
            else:
                mstime_remaining_text = QCoreApplication.translate(
                    "IdentityView", "Expired or never published"
                )

            ms_status_color = "#00AA00" if data["membership_state"] else "#FF0000"
            outdistanced_status_color = (
                "#FF0000" if data["is_outdistanced"] else "#00AA00"
            )
            if data["written"]:
                written_status_color = "#00AA00"
            elif data["idty_expired"]:
                written_status_color = "#FF0000"
            else:
                written_status_color = "#FF6347"

            description_membership = """<html>
<body>
    <p><span style="font-weight:600;">{status_label}</span>
     : <span style="color:{ms_status_color};">{status}</span>
    <span>{status_info}</span></p>
</body>
</html>""".format(
                ms_status_color=ms_status_color,
                status_label=QCoreApplication.translate("IdentityView", "Status"),
                status=status_value,
                status_info=status_info,
            )
            description_identity = """<html>
<body>
    <p><span style="font-weight:600;">{nb_certs_label}</span> : {nb_certs} <span style="color:{outdistanced_status_color};">({outdistanced_text})</span></p>
    <p><span style="font-weight:600;">{mstime_remaining_label}</span> : {mstime_remaining}</p>
</body>
</html>""".format(
                nb_certs_label=QCoreApplication.translate(
                    "IdentityView", "Certs. received"
                ),
                nb_certs=data["nb_certs"],
                outdistanced_text=data["outdistanced"],
                outdistanced_status_color=outdistanced_status_color,
                mstime_remaining_label=QCoreApplication.translate(
                    "IdentityView", "Membership"
                ),
                mstime_remaining=mstime_remaining_text,
            )

            self.label_written.setText(
                """
<html>
<body>
    <p><span style="font-weight:450; color:{written_status_color};">{written_label}</span></p>
</body>
</html>
""".format(
                    written_label=written_value,
                    written_status_color=written_status_color,
                )
            )

            if data["is_identity"]:
                self.label_membership.setText(description_membership)
                self.label_identity.setText(description_identity)
                self.button_membership.setText(membership_action_value)
                self.button_membership.setEnabled(membership_action_enabled)
            else:
                self.label_membership.hide()
                self.label_identity.hide()
                self.button_membership.hide()

    async def licence_dialog(self, currency, params):
        dt_dhms = timestamp_to_dhms(params.dt)
        if dt_dhms[0] > 0:
            dt_as_str = QCoreApplication.translate(
                "IdentityView", "{:} day(s) {:} hour(s)"
            ).format(*dt_dhms)
        else:
            dt_as_str = QCoreApplication.translate(
                "IdentityView", "{:} hour(s)"
            ).format(dt_dhms[1])
        if dt_dhms[2] > 0 or dt_dhms[3] > 0:
            dt_dhms += ", {:} minute(s) and {:} second(s)".format(*dt_dhms[1:])
        dt_reeval_dhms = timestamp_to_dhms(params.dt_reeval)
        dt_reeval_as_str = QCoreApplication.translate(
            "IdentityView", "{:} day(s) {:} hour(s)"
        ).format(*dt_reeval_dhms)

        message_box = QMessageBox(self)

        message_box.setText("Do you recognize the terms of the following licence :")
        message_box.setInformativeText(
            """
{:} is being produced by a Universal Dividend (UD) for any human member, which is :<br/>
<br/>
<table cellpadding="5">
 <tr><td align="right"><b>{:2.0%} / {:} days</b></td><td>{:}</td></tr>
 <tr><td align="right"><b>{:}</b></td><td>{:} {:}</td></tr>
 <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
 <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
</table>
<br/>
<br/>

The parameters of the Web of Trust of {:} are :<br/>
<table cellpadding="5">
 <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
 <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
 <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
 <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
 <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
 <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
 <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
 <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
</table>
<br/>
<br/>

<b>By asking to join as member, you recognize that this is your unique account,
and that you will only certify persons that you know well enough.</b>
 """.format(
                self.app.root_servers[currency]["display"],
                params.c,
                QLocale().toString(params.dt / 86400, "f", 2),
                QCoreApplication.translate("IdentityView", "Fundamental growth (c)"),
                params.ud0,
                QCoreApplication.translate(
                    "IdentityView", "Initial Universal Dividend UD(0) in"
                ),
                self.app.root_servers[currency]["display"],
                dt_as_str,
                QCoreApplication.translate(
                    "IdentityView", "Time period between two UD"
                ),
                dt_reeval_as_str,
                QCoreApplication.translate(
                    "IdentityView", "Time period between two UD reevaluation"
                ),
                self.app.root_servers[currency]["display"],
                QLocale().toString(params.sig_period / 86400, "f", 2),
                QCoreApplication.translate(
                    "IdentityView", "Minimum delay between 2 certifications (in days)"
                ),
                QLocale().toString(params.sig_validity / 86400, "f", 2),
                QCoreApplication.translate(
                    "IdentityView", "Maximum validity time of a certification (in days)"
                ),
                params.sig_qty,
                QCoreApplication.translate(
                    "IdentityView",
                    "Minimum quantity of certifications to be part of the WoT",
                ),
                params.sig_stock,
                QCoreApplication.translate(
                    "IdentityView",
                    "Maximum quantity of active certifications per member",
                ),
                params.sig_window,
                QCoreApplication.translate(
                    "IdentityView", "Maximum time before a pending certification expire"
                ),
                params.xpercent,
                QCoreApplication.translate(
                    "IdentityView",
                    "Minimum percent of sentries to reach to match the distance rule",
                ),
                params.ms_validity / 86400,
                QCoreApplication.translate(
                    "IdentityView", "Maximum validity time of a membership (in days)"
                ),
                params.step_max,
                QCoreApplication.translate(
                    "IdentityView",
                    "Maximum distance between each WoT member and a newcomer",
                ),
            )
        )
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.setDefaultButton(QMessageBox.No)
        return await dialog_async_exec(message_box)

    def changeEvent(self, event):
        """
        Intercepte LanguageChange event to translate UI
        :param QEvent QEvent: Event
        :return:
        """
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi(self)
        return super().changeEvent(event)
