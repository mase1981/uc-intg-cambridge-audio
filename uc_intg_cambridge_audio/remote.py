"""
Cambridge Audio remote entity.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import asyncio
import logging
from typing import Any

from aiostreammagic.models import ControlBusMode, DisplayBrightness
from ucapi import StatusCodes, remote
from ucapi.ui import Buttons, Size, UiPage, create_btn_mapping, create_ui_icon
from ucapi_framework import RemoteEntity

from uc_intg_cambridge_audio.config import CambridgeConfig
from uc_intg_cambridge_audio.device import CambridgeDevice

_LOG = logging.getLogger(__name__)

BASE_COMMANDS = [
    "POWER_ON",
    "POWER_OFF",
    "POWER_TOGGLE",
    "PLAY",
    "PAUSE",
    "PLAY_PAUSE",
    "STOP",
    "NEXT",
    "PREVIOUS",
    "VOLUME_UP",
    "VOLUME_DOWN",
    "MUTE",
    "UNMUTE",
    "MUTE_TOGGLE",
    "DISPLAY_BRIGHT",
    "DISPLAY_DIM",
    "DISPLAY_OFF",
    "PREAMP_ON",
    "PREAMP_OFF",
    "CONTROL_BUS_AMPLIFIER",
    "CONTROL_BUS_RECEIVER",
    "CONTROL_BUS_OFF",
]

_DISPLAY = {
    "DISPLAY_BRIGHT": DisplayBrightness.BRIGHT,
    "DISPLAY_DIM": DisplayBrightness.DIM,
    "DISPLAY_OFF": DisplayBrightness.OFF,
}
_CONTROL_BUS = {
    "CONTROL_BUS_AMPLIFIER": ControlBusMode.AMPLIFIER,
    "CONTROL_BUS_RECEIVER": ControlBusMode.RECEIVER,
    "CONTROL_BUS_OFF": ControlBusMode.OFF,
}
_SIMPLE = {
    "POWER_ON": ("power_on",),
    "POWER_OFF": ("power_off",),
    "PLAY": ("play",),
    "PAUSE": ("pause",),
    "PLAY_PAUSE": ("play_pause",),
    "STOP": ("stop",),
    "NEXT": ("next_track",),
    "PREVIOUS": ("previous_track",),
    "VOLUME_UP": ("volume_up",),
    "VOLUME_DOWN": ("volume_down",),
    "MUTE": ("set_mute", True),
    "UNMUTE": ("set_mute", False),
    "PREAMP_ON": ("set_pre_amp_mode", True),
    "PREAMP_OFF": ("set_pre_amp_mode", False),
}


def _ui_pages(source_ids: list[str]) -> list[UiPage]:
    main_page = UiPage("main", "Cambridge Audio", grid=Size(4, 6))
    for icon, col, row, cmd, size in (
        ("uc:power-on", 0, 0, "POWER_ON", None),
        ("uc:power-off", 1, 0, "POWER_OFF", None),
        ("uc:up-arrow", 2, 0, "VOLUME_UP", None),
        ("uc:down-arrow", 3, 0, "VOLUME_DOWN", None),
        ("uc:play", 0, 1, "PLAY", None),
        ("uc:pause", 1, 1, "PAUSE", None),
        ("uc:stop", 2, 1, "STOP", None),
        ("uc:speaker-mute", 3, 1, "MUTE_TOGGLE", None),
        ("uc:prev", 0, 2, "PREVIOUS", None),
        ("uc:play-pause", 1, 2, "PLAY_PAUSE", Size(2, 1)),
        ("uc:next", 3, 2, "NEXT", None),
    ):
        main_page.add(create_ui_icon(icon, col, row, size=size, cmd=cmd))
    pages = [main_page]

    if source_ids:
        sources_page = UiPage("sources", "Sources", grid=Size(4, 6))
        for index, source_id in enumerate(source_ids[:24]):
            sources_page.add(create_ui_icon("uc:input", index % 4, index // 4, cmd=f"SOURCE_{source_id.upper()}"))
        pages.append(sources_page)

    settings_page = UiPage("settings", "Settings", grid=Size(4, 6))
    for icon, col, row, cmd in (
        ("uc:brightness-high", 0, 0, "DISPLAY_BRIGHT"),
        ("uc:brightness-medium", 1, 0, "DISPLAY_DIM"),
        ("uc:brightness-off", 2, 0, "DISPLAY_OFF"),
        ("uc:pre-amplifier", 0, 1, "PREAMP_ON"),
        ("uc:amplifier-off", 1, 1, "PREAMP_OFF"),
        ("uc:amplifier", 0, 2, "CONTROL_BUS_AMPLIFIER"),
        ("uc:receiver", 1, 2, "CONTROL_BUS_RECEIVER"),
        ("uc:control-off", 2, 2, "CONTROL_BUS_OFF"),
    ):
        settings_page.add(create_ui_icon(icon, col, row, cmd=cmd))
    pages.append(settings_page)
    return pages


class CambridgeRemote(RemoteEntity):
    def __init__(self, device_config: CambridgeConfig, device: CambridgeDevice) -> None:
        self._device = device
        self._source_commands = [f"SOURCE_{s.upper()}" for s in device_config.source_ids]
        super().__init__(
            f"remote.{device_config.identifier}",
            f"{device_config.name} Remote",
            [remote.Features.ON_OFF, remote.Features.TOGGLE, remote.Features.SEND_CMD],
            {remote.Attributes.STATE: remote.States.UNKNOWN},
            simple_commands=BASE_COMMANDS + self._source_commands,
            button_mapping=[
                create_btn_mapping(Buttons.POWER, short="POWER_TOGGLE"),
                create_btn_mapping(Buttons.VOLUME_UP, short="VOLUME_UP"),
                create_btn_mapping(Buttons.VOLUME_DOWN, short="VOLUME_DOWN"),
                create_btn_mapping(Buttons.MUTE, short="MUTE_TOGGLE"),
                create_btn_mapping(Buttons.PLAY, short="PLAY_PAUSE"),
                create_btn_mapping(Buttons.NEXT, short="NEXT"),
                create_btn_mapping(Buttons.PREV, short="PREVIOUS"),
            ],
            ui_pages=_ui_pages(device_config.source_ids),
            cmd_handler=self._handle_command,
        )
        self.subscribe_to_device(device)

    async def sync_state(self) -> None:
        state = self._device.sm_state
        if not self._device.available or state is None:
            self.update({remote.Attributes.STATE: remote.States.UNAVAILABLE})
            return
        self.update({remote.Attributes.STATE: remote.States.ON if state.power else remote.States.OFF})

    async def _handle_command(self, entity: Any, cmd_id: str, params: dict[str, Any] | None) -> StatusCodes:
        params = params or {}
        if cmd_id == remote.Commands.ON:
            return await self._run("POWER_ON")
        if cmd_id == remote.Commands.OFF:
            return await self._run("POWER_OFF")
        if cmd_id == remote.Commands.TOGGLE:
            return await self._run("POWER_TOGGLE")

        try:
            delay = int(params.get("delay", 0) or 0) / 1000
            if cmd_id == remote.Commands.SEND_CMD:
                commands = [str(params.get("command", ""))] * max(1, int(params.get("repeat", 1) or 1))
            elif cmd_id == remote.Commands.SEND_CMD_SEQUENCE:
                sequence = params.get("sequence", [])
                commands = sequence.split(",") if isinstance(sequence, str) else list(sequence or [])
            else:
                return StatusCodes.NOT_IMPLEMENTED
        except (ValueError, TypeError):
            return StatusCodes.BAD_REQUEST

        for index, command in enumerate(commands):
            status = await self._run(str(command).strip())
            if status != StatusCodes.OK:
                return status
            if delay and index < len(commands) - 1:
                await asyncio.sleep(delay)
        return StatusCodes.OK

    async def _run(self, command: str) -> StatusCodes:
        command = command.upper()
        device = self._device
        try:
            if command in _SIMPLE:
                await device.send(*_SIMPLE[command])
            elif command == "POWER_TOGGLE":
                state = device.sm_state
                await device.send("power_off" if state and state.power else "power_on")
            elif command == "MUTE_TOGGLE":
                state = device.sm_state
                await device.send("set_mute", not (state.mute if state else False))
            elif command in _DISPLAY:
                await device.send("set_display_brightness", _DISPLAY[command])
            elif command in _CONTROL_BUS:
                await device.send("set_control_bus_mode", _CONTROL_BUS[command])
            elif command.startswith("SOURCE_"):
                source = next((s for s in device.sources if s.id.upper() == command[len("SOURCE_"):]), None)
                if source is None:
                    return StatusCodes.BAD_REQUEST
                await device.send("set_source_by_id", source.id)
            else:
                return StatusCodes.BAD_REQUEST
        except Exception as err:  # pylint: disable=broad-exception-caught
            _LOG.error("[%s] Command %s failed: %s", self.id, command, err)
            return StatusCodes.SERVER_ERROR
        return StatusCodes.OK
