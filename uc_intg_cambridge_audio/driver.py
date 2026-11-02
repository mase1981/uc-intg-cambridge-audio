"""
Cambridge Audio integration driver.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

from ucapi_framework import BaseIntegrationDriver

from uc_intg_cambridge_audio.config import CambridgeConfig
from uc_intg_cambridge_audio.device import CambridgeDevice
from uc_intg_cambridge_audio.media_player import CambridgeMediaPlayer
from uc_intg_cambridge_audio.remote import CambridgeRemote
from uc_intg_cambridge_audio.select import create_selects
from uc_intg_cambridge_audio.sensor import create_sensors
from uc_intg_cambridge_audio.switch import create_switches


class CambridgeDriver(BaseIntegrationDriver[CambridgeDevice, CambridgeConfig]):
    def __init__(self) -> None:
        super().__init__(
            device_class=CambridgeDevice,
            entity_classes=[
                CambridgeMediaPlayer,
                CambridgeRemote,
                create_sensors,
                create_selects,
                create_switches,
            ],
            driver_id="cambridge_audio",
        )
