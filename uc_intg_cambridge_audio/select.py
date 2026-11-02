"""
Cambridge Audio select entities.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from dataclasses import dataclass
from typing import Any, Callable

from aiostreammagic.models import EQ_PRESETS, ControlBusMode, DisplayBrightness, StandbyMode
from ucapi import StatusCodes, select
from ucapi_framework import SelectEntity

from uc_intg_cambridge_audio.config import CambridgeConfig
from uc_intg_cambridge_audio.device import CambridgeDevice
from uc_intg_cambridge_audio.sensor import label

_LOG = logging.getLogger(__name__)


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    options: dict[str, Any] = {}
    for text, value in pairs:
        candidate, count = text, 2
        while candidate in options:
            candidate = f"{text} ({count})"
            count += 1
        options[candidate] = value
    return options


def _enum_options(enum_cls: type, skip: tuple = ()) -> Callable[[CambridgeDevice], dict[str, Any]]:
    def options(device: CambridgeDevice) -> dict[str, Any]:
        return {label(m): m for m in enum_cls if m not in skip}

    return options


def _source_options(device: CambridgeDevice) -> dict[str, Any]:
    return _unique([(s.name, s.id) for s in device.sources])


def _source_current(device: CambridgeDevice) -> str | None:
    state = device.sm_state
    return next((s.name for s in device.sources if state and s.id == state.source), None)


def _output_options(device: CambridgeDevice) -> dict[str, Any]:
    outputs = device.audio_output
    return _unique([(o.name, o.id) for o in outputs.outputs]) if outputs else {}


def _output_current(device: CambridgeDevice) -> str | None:
    state, outputs = device.sm_state, device.audio_output
    if not state or not outputs:
        return None
    return next((o.name for o in outputs.outputs if o.id == state.audio_output), None)


def _eq_options(device: CambridgeDevice) -> dict[str, Any]:
    return {label(name): name for name in EQ_PRESETS}


def _preset_options(device: CambridgeDevice) -> dict[str, Any]:
    presets = device.preset_list
    if not presets:
        return {}
    return _unique([(f"{p.preset_id}. {p.name}", p.preset_id) for p in presets.presets])


def _preset_current(device: CambridgeDevice) -> str | None:
    presets = device.preset_list
    if not presets:
        return None
    return next((f"{p.preset_id}. {p.name}" for p in presets.presets if p.is_playing), None)


@dataclass(frozen=True)
class SelectSpec:
    key: str
    name: str
    options: Callable[[CambridgeDevice], dict[str, Any]]
    current: Callable[[CambridgeDevice], str | None]
    method: str
    feature: str | None = None


SPECS: list[SelectSpec] = [
    SelectSpec("source", "Source", _source_options, _source_current, "set_source_by_id"),
    SelectSpec("audio_output", "Audio Output", _output_options, _output_current, "set_audio_output"),
    SelectSpec(
        "display_brightness",
        "Display Brightness",
        _enum_options(DisplayBrightness, skip=(DisplayBrightness.NONE,)),
        lambda d: label(d.display.brightness) if d.display else None,
        "set_display_brightness",
    ),
    SelectSpec(
        "control_bus",
        "Control Bus",
        _enum_options(ControlBusMode),
        lambda d: label(d.sm_state.control_bus) if d.sm_state else None,
        "set_control_bus_mode",
    ),
    SelectSpec(
        "standby_mode",
        "Standby Mode",
        lambda d: {"Network": StandbyMode.NETWORK, "Eco": StandbyMode.ECO},
        lambda d: {StandbyMode.NETWORK: "Network", StandbyMode.ECO: "Eco"}.get(d.sm_state.standby_mode) if d.sm_state else None,
        "set_standby_mode",
    ),
    SelectSpec("eq_preset", "EQ Preset", _eq_options, lambda d: label(d.eq_preset), "set_equalizer_preset", feature="eq"),
    SelectSpec("preset", "Preset", _preset_options, _preset_current, "recall_preset"),
]


class CambridgeSelect(SelectEntity):
    def __init__(self, spec: SelectSpec, device_config: CambridgeConfig, device: CambridgeDevice) -> None:
        self._device = device
        self._spec = spec
        super().__init__(
            f"select.{device_config.identifier}.{spec.key}",
            f"{device_config.name} {spec.name}",
            {
                select.Attributes.STATE: select.States.UNKNOWN,
                select.Attributes.OPTIONS: [],
                select.Attributes.CURRENT_OPTION: "",
            },
            cmd_handler=self._handle_command,
        )
        self.subscribe_to_device(device)

    async def sync_state(self) -> None:
        if not self._device.available:
            self.update({select.Attributes.STATE: select.States.UNAVAILABLE})
            return
        options = list(self._spec.options(self._device))
        current = self._spec.current(self._device)
        self.update(
            {
                select.Attributes.STATE: select.States.ON,
                select.Attributes.OPTIONS: options,
                select.Attributes.CURRENT_OPTION: current if current in options else "",
            }
        )

    async def _handle_command(self, entity: Any, cmd_id: str, params: dict[str, Any] | None) -> StatusCodes:
        mapping = self._spec.options(self._device)
        options = list(mapping)
        if not options:
            return StatusCodes.NOT_FOUND
        current = self._spec.current(self._device)
        index = options.index(current) if current in options else -1

        if cmd_id == select.Commands.SELECT_OPTION:
            option = (params or {}).get("option", "")
            if option not in mapping:
                return StatusCodes.BAD_REQUEST
        elif cmd_id == select.Commands.SELECT_FIRST:
            option = options[0]
        elif cmd_id == select.Commands.SELECT_LAST:
            option = options[-1]
        elif cmd_id == select.Commands.SELECT_NEXT:
            option = options[(index + 1) % len(options)]
        elif cmd_id == select.Commands.SELECT_PREVIOUS:
            option = options[(index - 1) % len(options)]
        else:
            return StatusCodes.NOT_IMPLEMENTED

        try:
            await self._device.send(self._spec.method, mapping[option])
        except Exception as err:  # pylint: disable=broad-exception-caught
            _LOG.error("[%s] Select %s failed: %s", self.id, option, err)
            return StatusCodes.SERVER_ERROR
        return StatusCodes.OK


def create_selects(device_config: CambridgeConfig, device: CambridgeDevice) -> list[CambridgeSelect]:
    features = device_config.features
    return [
        CambridgeSelect(spec, device_config, device)
        for spec in SPECS
        if spec.feature is None or features is None or spec.feature in features
    ]
