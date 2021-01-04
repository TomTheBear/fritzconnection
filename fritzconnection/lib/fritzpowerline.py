"""
Module to get informations about Powerline devices based on
https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/x_homeplugSCPD.pdf
"""
# This module is part of the FritzConnection package.
# https://github.com/kbr/fritzconnection
# License: MIT (https://opensource.org/licenses/MIT)
# Author: Thomas Gruber


import itertools
from ..core.exceptions import FritzServiceError
from .fritzbase import AbstractLibraryBase


# important: don't set an extension number here:
SERVICE = 'X_AVM-DE_Homeplug'


class FritzPowerline(AbstractLibraryBase):
    """
    Class to list all known powerline devices.
    """
    def __init__(self, *args, service=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service
    def _action(self, actionname, **kwargs):
        service = f'{SERVICE}{self.service}'
        return self.fc.call_action(service, actionname, **kwargs)
    
    @property
    def device_number(self):
        """
        Number of registered powerline devices for the active
        X_AVM-DE_Homeplug configuration.
        """
        result = self._action('GetNumberOfDeviceEntries')
        return result['NewNumberOfEntries']
        
    def get_generic_device_entry(self, index):
        """
        Return a dictionary with informations about the device
        internally stored at the position 'index'.
        """
        result = self._action(
            'GetGenericDeviceEntry',
            NewIndex=index
        )
        return result
    
    def get_specific_device_entry(self, mac_address):
        """
        Return a dictionary with informations about the device
        with the given 'mac_address'.
        """
        result = self._action(
            'GetSpecificDeviceEntry',
            NewMACAddress=mac_address
        )
        return result

    def run_device_update(self, mac_address):
        """
        Triggers the device with the given `mac_address` to run an
        update. The method returns immediately, but for the device it
        take some time to do the OS update. All vendor warnings about running
        an update apply, like not turning power off during an
        update. So run this command with caution.
        """
        result = self._action(
            'DeviceDoUpdate',
            NewMACAddress=mac_address
        )

    def get_device_info(self):
        """
        Returns a list of dictionaries with information about the known devices.
        The dict-keys are: 'service', 'index', 'active', 'mac', 'name', 'model',
        'updateAvailable' and 'updateSuccess'
        """
        informations = []
        for index in itertools.count():
            try:
                host = self.get_generic_host_entry(index)
            except IndexError:
                break
            informations.append({
                'service': self.service,
                'index': index,
                'active': host['NewActive'],
                'mac': host['NewMACAddress'],
                'name': host['NewName'],
                'model': host['NewModel'],
                'updateAvailable': host['NewUpdateAvailable'],
                'updateSuccess': host['NewUpdateSuccessful'],
            })
        return informations
