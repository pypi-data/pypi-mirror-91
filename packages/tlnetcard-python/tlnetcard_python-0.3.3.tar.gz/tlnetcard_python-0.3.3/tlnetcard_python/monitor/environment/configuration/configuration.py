"""
tlnetcard_python.monitor.environment.configuration.configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``Configuration`` object to provide the functionality of TLNET Supervisor ->
Monitor -> Environment -> Information.
"""

# Standard library.
from typing import Any, Dict
# Required internal classes/functions.
from tlnetcard_python.login import Login

class Configuration:
    """
    A TLNET Supervisor ``Configuration`` object. Provides the functionality of the equivalent
    webpage TLNET Supervisor -> Monitor -> Environment -> Information.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.monitor.environment import Configuration
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.monitor.environment.information object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_env_configuration = Configuration(card)
    >>> # Now that the Configuration object has been created, functions belonging to the
    >>> # Configuration class can be used. For example, changing the temperature range:
    >>> card_env_configuration.set_temperature_limits(55, 100)
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``Configuration`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._get_url = self._login_object.get_base_url() + "/en/ups/env_config.asp"
        self._post_url = self._login_object.get_base_url() + "/delta/env_config"
    def add_input_contact(self, title: str, is_open: bool = True,
                          smart_shutdown: bool = False) -> bool:
        """
        Adds a new input contact with the specified attributes. If there are already 4 contacts
        configured, this method does nothing and returns ``False``. Otherwise the contact is added
        and ``True`` is returned.

        :param title: The title of the contact.
        :param is_open: Whether the contact is of type Normal Open or not (i.e. Normal Closed).
        :param smart_shutdown: Whether this contact is capable of initiating a smart shutdown.
        :rtype: ``bool``
        """
        # Checking if all contacts are already in use and finding first empty contact.
        system_config = self._login_object.get_system_config()
        contact_titles = [system_config["Title Input" + str(i)] for i in range(1, 5)]
        if "" not in contact_titles:
            return False
        first_empty = str(contact_titles.index("") + 1)

        # Generating payload.
        config_data = {
            "ENV_TITLE_R" + first_empty: title,
            "ENV_NCNO_R" + first_empty: str(int(not is_open)),
            "ENV_R" + first_empty + "_SSHUT": str(int(smart_shutdown)),
        }

        # Uploading environment configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=config_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
        return True
    def clear_input_contacts(self) -> None:
        """
        Clears all input contacts. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        config_data = {}
        for i in range(1, 5):
            config_data["ENV_TITLE_R" + str(i)] = ""
            config_data["ENV_NCNO_R" + str(i)] = "0"
            config_data["ENV_R" + str(i) + "_SSHUT"] = "0"

        # Uploading environment configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=config_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def get_humidity_configuration(self) -> Dict[str, Any]:
        """
        Returns info for how humidity limits are configured as a dictionary.

        :rtype: ``Dict[str, Any]``
        """

    def get_input_contact_configuration(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns info on how input contacts are configured as a dictionary of dictionaries (one
        dictionary per contact).

        :rtype: ``Dict[str, Dict[str, Any]]``
        """
    def get_temperature_configuration(self) -> Dict[str, Any]:
        """
        Returns info for how temperature limits are configured as a dictionary.

        :rtype: ``Dict[str, Any]``
        """
    def remove_input_contact(self, title: str) -> bool:
        """
        Removes the input contact with the specified title. If no input contact has the specified
        title, this function does nothing and returns ``False``. Otherwise the contact is removed
        and ``True`` is returned.

        :param title: The Input Contact title.
        :rtype: ``bool``
        """
    def set_humidity_configuration(self) -> None:
        """
        Sets info for how humidity limits are configured as a dictionary. Returns ``None``.

        :rtype: ``None``
        """
    def set_temperature_configuration(self) -> None:
        """
        Returns info for how temperature limits are configured as a dictionary.

        :rtype: ``None``
        """
