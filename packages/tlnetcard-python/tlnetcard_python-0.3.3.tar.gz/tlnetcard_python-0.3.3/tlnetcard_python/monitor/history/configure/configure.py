"""
tlnetcard_python.monitor.history.configure.configure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``Configure`` object to provide the functionality of TLNET Supervisor ->
Monitor -> History -> Configure.
"""

# Required internal classes/functions.
from tlnetcard_python.login import Login

class Configure:
    """
    A TLNET Supervisor ``Configure`` object. Provides the functionality of the equivalent webpage
    TLNET Supervisor -> Monitor -> History -> Configure.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.monitor.history import Configure
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.monitor.history.Configure object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_configure = Configure(card)
    >>> # Now that the Configure object has been created, functions belonging to the Configure class
    >>> # can be used. For example, clearing the event log:
    >>> card_configure.clear_event_log()
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``Configure`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._post_url = self._login_object.get_base_url + "/delta/hist_config"
    def clear_data_log(self) -> None:
        """
        Clears the data log. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        config_data = {
            "CLEAR_DATA": "Clear Data Log"
        }

        # Uploading FTP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=config_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def clear_event_log(self) -> None:
        """
        Clears the data log. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        config_data = {
            "CLEAR_LOG": "Clear Event Log"
        }

        # Uploading FTP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=config_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def set_data_interval(self, interval: int = 10) -> None:
        """
        Sets the interval in minutes at which information is saved to the data log. Returns
        ``None``.

        :param interval: The number of minutes between saves of the data log. This number must be
        between ``0`` and ``10``. A value of ``0`` will result in the data log never being saved.
        :rtype: ``None``
        """
        # Generating payload.
        config_data = {
            "HCG_INTERVAL": str(interval),
            "HCG_APPLY": "Apply"
        }

        # Uploading FTP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=config_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
