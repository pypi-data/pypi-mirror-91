from PyQt5.QtCore import QObject, QLocale, QDateTime, QCoreApplication
from sakia.data.processors import ConnectionsProcessor
import attr
import math
from sakia import __version__
from sakia.money import Referentials


@attr.s()
class ToolbarModel(QObject):
    """
    The model of Navigation component

    :param sakia.app.Application app: the application
    :param sakia.gui.navigation.model.NavigationModel navigation_model: The navigation model
    :param sakia.services.BlockchainService blockchain_service: The blockchain service
    """

    app = attr.ib()
    navigation_model = attr.ib()
    blockchain_service = attr.ib()
    blockchain_processor = attr.ib()

    def __attrs_post_init__(self):
        super().__init__()

    def notifications(self):
        return self.app.parameters.notifications

    def connections_with_uids(self):
        return ConnectionsProcessor.instanciate(self.app).connections_with_uids()

    def connections(self):
        return ConnectionsProcessor.instanciate(self.app).connections()

    def about_text(self):
        latest = self.app.available_version
        version_info = ""
        version_url = ""
        url_text = ""

        if not latest[0]:
            version_info = "Latest release: {version}".format(version=latest[1])
            version_url = latest[2]
            url_text = QCoreApplication.translate("ToolbarView", "Download page")

        new_version_text = """
            <p><b>{version_info}</b></p>
            <p><a href={version_url}>{url_text}</a></p>
            """.format(
            version_info=version_info, version_url=version_url, url_text=url_text
        )
        return """
        <h1>Sakia</h1>

        <p>Python/Qt Duniter client</p>

        <p>Version: {:}</p>
        {new_version_text}

        <p>License: GPLv3</p>

        <p><b>Authors</b></p>

        <p>inso</p>
        <p>vit</p>
        <p>canercandan</p>
        <p>Moul</p>
        """.format(
            __version__, new_version_text=new_version_text
        )

    def get_localized_data(self):
        localized_data = {}
        #  try to request money parameters
        params = self.blockchain_service.parameters()

        localized_data["currency"] = self.app.root_servers[self.app.currency]["display"]
        localized_data["growth"] = params.c
        localized_data["growth_per_dt"] = QLocale().toString(
            params.c / (params.dt_reeval / params.dt), "f", 8
        )
        localized_data["dt_reeval_in_days"] = QLocale().toString(
            params.dt_reeval / 86400, "f", 2
        )

        last_mass = self.blockchain_service.last_monetary_mass()
        last_ud, last_ud_base = self.blockchain_service.last_ud()
        last_members_count = self.blockchain_service.last_members_count()
        last_ud_time = self.blockchain_service.last_ud_time()

        localized_data["units"] = self.app.current_ref.instance(
            0, self.app.currency, self.app, None
        ).units
        localized_data["diff_units"] = self.app.current_ref.instance(
            0, self.app.currency, self.app, None
        ).diff_units

        if last_ud:
            # display float values
            localized_data["ud"] = self.app.current_ref.instance(
                last_ud * math.pow(10, last_ud_base), self.app.currency, self.app
            ).diff_localized(False, True)

            localized_data[
                "members_count"
            ] = self.blockchain_service.last_members_count()

            computed_dividend = self.blockchain_service.computed_dividend()
            # display float values
            localized_data["ud_plus_1"] = self.app.current_ref.instance(
                computed_dividend, self.app.currency, self.app
            ).diff_localized(False, True)

            localized_data["mass"] = self.app.current_ref.instance(
                self.blockchain_service.last_monetary_mass(),
                self.app.currency,
                self.app,
            ).localized(False, True)

            ud_median_time = self.blockchain_service.last_ud_time()
            ud_median_time = self.blockchain_processor.adjusted_ts(
                self.app.currency, ud_median_time
            )

            localized_data["ud_median_time"] = QLocale.toString(
                QLocale(),
                QDateTime.fromTime_t(ud_median_time),
                QLocale.dateTimeFormat(QLocale(), QLocale.ShortFormat),
            )

            next_ud_median_time = self.blockchain_service.last_ud_time() + params.dt
            next_ud_median_time = self.blockchain_processor.adjusted_ts(
                self.app.currency, next_ud_median_time
            )

            localized_data["next_ud_median_time"] = QLocale.toString(
                QLocale(),
                QDateTime.fromTime_t(next_ud_median_time),
                QLocale.dateTimeFormat(QLocale(), QLocale.ShortFormat),
            )

            next_ud_reeval = self.blockchain_service.next_ud_reeval()
            next_ud_reeval = self.blockchain_processor.adjusted_ts(
                self.app.currency, next_ud_reeval
            )
            localized_data["next_ud_reeval"] = QLocale.toString(
                QLocale(),
                QDateTime.fromTime_t(next_ud_reeval),
                QLocale.dateTimeFormat(QLocale(), QLocale.ShortFormat),
            )

            if last_ud:
                mass_per_member = (
                    float(0)
                    if last_ud == 0 or last_members_count == 0
                    else last_mass / last_members_count
                )
                localized_data["members_count"] = last_members_count
                localized_data["mass_per_member"] = self.app.current_ref.instance(
                    mass_per_member, self.app.currency, self.app
                ).localized(False, True)
                # avoid divide by zero !
                if last_members_count == 0:
                    localized_data["actual_growth"] = float(0)
                else:
                    localized_data["actual_growth"] = (
                        last_ud * math.pow(10, last_ud_base)
                    ) / (last_mass / last_members_count)

                last_ud_time = self.blockchain_processor.adjusted_ts(
                    self.app.currency, last_ud_time
                )
                localized_data["ud_median_time_minus_1"] = QLocale.toString(
                    QLocale(),
                    QDateTime.fromTime_t(last_ud_time),
                    QLocale.dateTimeFormat(QLocale(), QLocale.ShortFormat),
                )
        return localized_data

    def parameters(self):
        """
        Get community parameters
        """
        return self.blockchain_service.parameters()

    def referentials(self):
        """
        Get referentials
        :return: The list of instances of all referentials
        :rtype: list
        """
        refs_instances = []
        for ref_class in Referentials:
            refs_instances.append(ref_class(0, self.app.currency, self.app, None))
        return refs_instances
