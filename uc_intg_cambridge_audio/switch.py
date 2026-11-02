"""
Cambridge Audio switch entities.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from dataclasses import dataclass
from typing import Any, Callable

from ucapi import StatusCodes, switch
from ucapi_framework import SwitchEntity

from uc_intg_cambridge_audio.config import CambridgeConfig
from uc_intg_cambridge_audio.device import CambridgeDevice

_LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class SwitchSpec:
    key: str
    name: str
    getter: Callable[[CambridgeDevice], bool | None]
    method: str
    feature: str | None = None


SPECS: list[SwitchSpec] = [
    SwitchSpec("pre_amp", "Pre-Amp Mode", lambda d: d.sm_state.pre_amp_mode if d.sm_state else None, "set_pre_amp_mode"),
    SwitchSpec("equalizer", "Equalizer", lambda d: d.audio.user_eq.enabled if d.audio and d.audio.user_eq else None, "set_equalizer_mode", "eq"),
    SwitchSpec("room_correction", "Room Correction", lambda d: d.audio.tilt_eq.enabled if d.audio and d.audio.tilt_eq else None, "set_room_correction_mode", "room_correction"),
    SwitchSpec("early_update", "Early Updates", lambda d: d.update_info.early_update if d.update_info else None, "set_early_update"),
]


class CambridgeSwitch(SwitchEntity):
    def __init__(self, spec: SwitchSpec, device_config: CambridgeConfig, device: CambridgeDevice) -> None:
        self._device = device
        self._spec = spec
        super().__init__(
            f"switch.{device_config.identifier}.{spec.key}",
            f"{device_config.name} {spec.name}",
            [switch.Features.ON_OFF, switch.Features.TOGGLE],
            {switch.Attributes.STATE: switch.States.UNKNOWN},
            cmd_handler=self._handle_command,
        )
        self.subscribe_to_device(device)

    async def sync_state(self) -> None:
        if not self._device.available:
            self.update({switch.Attributes.STATE: switch.States.UNAVAILABLE})
            return
        value = self._spec.getter(self._device)
        if value is None:
            self.update({switch.Attributes.STATE: switch.States.UNKNOWN})
            return
        self.update({switch.Attributes.STATE: switch.States.ON if value else switch.States.OFF})

    async def _handle_command(self, entity: Any, cmd_id: str, params: dict[str, Any] | None) -> StatusCodes:
        current = bool(self._spec.getter(self._device))
        if cmd_id == switch.Commands.ON:
            target = True
        elif cmd_id == switch.Commands.OFF:
            target = False
        elif cmd_id == switch.Commands.TOGGLE:
            target = not current
        else:
            return StatusCodes.NOT_IMPLEMENTED
        try:
            await self._device.send(self._spec.method, target)
        except Exception as err:  # pylint: disable=broad-exception-caught
            _LOG.error("[%s] Switch command failed: %s", self.id, err)
            return StatusCodes.SERVER_ERROR
        return StatusCodes.OK


def create_switches(device_config: CambridgeConfig, device: CambridgeDevice) -> list[CambridgeSwitch]:
    features = device_config.features
    return [
        CambridgeSwitch(spec, device_config, device)
        for spec in SPECS
        if spec.feature is None or features is None or spec.feature in features
    ]
