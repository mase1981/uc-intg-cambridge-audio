"""
Cambridge Audio sensor entities.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

from dataclasses import dataclass
from typing import Any, Callable

from ucapi import sensor
from ucapi_framework import SensorEntity

from uc_intg_cambridge_audio.config import CambridgeConfig
from uc_intg_cambridge_audio.device import CambridgeDevice


def label(value: Any) -> str | None:
    if value is None or value == "":
        return None
    return str(getattr(value, "value", value)).replace("_", " ").title()


def on_off(value: bool | None) -> str | None:
    return None if value is None else ("On" if value else "Off")


def _power_state(device: CambridgeDevice) -> str | None:
    state, play = device.sm_state, device.play_state
    if state is None or play is None:
        return None
    if not state.power or play.state == "NETWORK":
        return "Standby"
    return {"play": "Playing", "pause": "Paused", "connecting": "Buffering"}.get(play.state, "Idle")


def _source(device: CambridgeDevice) -> str | None:
    state = device.sm_state
    if state is None:
        return None
    return next((s.name for s in device.sources if s.id == state.source), None)


def _audio_output(device: CambridgeDevice) -> str | None:
    state, outputs = device.sm_state, device.audio_output
    if state is None or outputs is None or not state.audio_output:
        return None
    return next((o.name for o in outputs.outputs if o.id == state.audio_output), state.audio_output)


def _update_status(device: CambridgeDevice) -> str | None:
    update = device.update_info
    if update is None:
        return None
    if update.updating:
        return "Updating"
    return "Update Available" if update.update_available else "Up To Date"


def _meta(attr: str) -> Callable[[CambridgeDevice], Any]:
    def getter(device: CambridgeDevice) -> Any:
        play = device.play_state
        return getattr(play.metadata, attr, None) if play else None

    return getter


def _audio(attr: str) -> Callable[[CambridgeDevice], Any]:
    def getter(device: CambridgeDevice) -> Any:
        audio = device.audio
        return getattr(audio, attr, None) if audio else None

    return getter


def _sample_rate(device: CambridgeDevice) -> float | None:
    rate = _meta("sample_rate")(device)
    return round(rate / 1000, 1) if rate else None


def _auto_power_down(device: CambridgeDevice) -> int | None:
    state = device.sm_state
    return None if state is None else round(state.auto_power_down_time / 60)


def _yes_no(attr: str) -> Callable[[CambridgeDevice], str | None]:
    def getter(device: CambridgeDevice) -> str | None:
        value = _meta(attr)(device)
        return None if value is None else ("Yes" if value else "No")

    return getter


@dataclass(frozen=True)
class SensorSpec:
    key: str
    name: str
    getter: Callable[[CambridgeDevice], Any]
    unit: str = ""
    feature: str | None = None


def _state_attr(attr: str) -> Callable[[CambridgeDevice], Any]:
    def getter(device: CambridgeDevice) -> Any:
        state = device.sm_state
        return getattr(state, attr, None) if state else None

    return getter


SPECS: list[SensorSpec] = [
    SensorSpec("state", "State", _power_state),
    SensorSpec("source", "Source", _source),
    SensorSpec("volume", "Volume", _state_attr("volume_percent"), "%"),
    SensorSpec("volume_db", "Volume dB", _state_attr("volume_db"), "dB"),
    SensorSpec("audio_output", "Audio Output", _audio_output),
    SensorSpec("model", "Model", lambda d: d.info.model if d.info else None),
    SensorSpec("api_version", "API Version", lambda d: d.info.api_version if d.info else None),
    SensorSpec("update_status", "Firmware Update", _update_status),
    SensorSpec("pre_amp", "Pre-Amp Mode", lambda d: on_off(_state_attr("pre_amp_mode")(d))),
    SensorSpec("control_bus", "Control Bus", lambda d: label(_state_attr("control_bus")(d))),
    SensorSpec("standby_mode", "Standby Mode", lambda d: label(_state_attr("standby_mode")(d))),
    SensorSpec("auto_power_down", "Auto Power Down", _auto_power_down, "min"),
    SensorSpec("display_brightness", "Display Brightness", lambda d: label(d.display.brightness) if d.display else None),
    SensorSpec("equalizer", "Equalizer", lambda d: on_off(d.audio.user_eq.enabled) if d.audio and d.audio.user_eq else None, feature="eq"),
    SensorSpec("eq_preset", "EQ Preset", lambda d: label(d.eq_preset) or "Custom", feature="eq"),
    SensorSpec("room_correction", "Room Correction", lambda d: on_off(d.audio.tilt_eq.enabled) if d.audio and d.audio.tilt_eq else None, feature="room_correction"),
    SensorSpec("room_correction_intensity", "Room Correction Intensity", lambda d: d.audio.tilt_eq.intensity if d.audio and d.audio.tilt_eq else None, feature="room_correction"),
    SensorSpec("balance", "Balance", _audio("balance"), feature="balance"),
    SensorSpec("volume_limit", "Volume Limit", _audio("volume_limit_percent"), "%", feature="volume_limit"),
    SensorSpec("digital_filter", "Digital Filter", lambda d: label(_audio("digital_filter")(d)), feature="digital_filter"),
    SensorSpec("pipeline", "Audio Pipeline", lambda d: label(_audio("pipeline")(d)), feature="pipeline"),
    SensorSpec("phase_invert", "Phase Invert", lambda d: on_off(_audio("phase_invert")(d)), feature="phase_invert"),
    SensorSpec("codec", "Codec", _meta("codec")),
    SensorSpec("sample_rate", "Sample Rate", _sample_rate, "kHz"),
    SensorSpec("sample_format", "Sample Format", _meta("sample_format")),
    SensorSpec("bitrate", "Bitrate", _meta("bitrate")),
    SensorSpec("lossless", "Lossless", _yes_no("lossless")),
    SensorSpec("mqa", "MQA", _meta("mqa")),
    SensorSpec("signal", "Signal", _yes_no("signal")),
    SensorSpec("station", "Station", _meta("station")),
]


class CambridgeSensor(SensorEntity):
    def __init__(self, spec: SensorSpec, device_config: CambridgeConfig, device: CambridgeDevice) -> None:
        self._device = device
        self._spec = spec
        super().__init__(
            f"sensor.{device_config.identifier}.{spec.key}",
            f"{device_config.name} {spec.name}",
            [],
            {sensor.Attributes.STATE: sensor.States.UNKNOWN, sensor.Attributes.VALUE: ""},
            device_class=sensor.DeviceClasses.CUSTOM,
            options={sensor.Options.CUSTOM_UNIT: spec.unit},
        )
        self.subscribe_to_device(device)

    async def sync_state(self) -> None:
        if not self._device.available:
            self.update({sensor.Attributes.STATE: sensor.States.UNAVAILABLE})
            return
        value = self._spec.getter(self._device)
        if value is None or value == "":
            self.update({sensor.Attributes.STATE: sensor.States.UNKNOWN, sensor.Attributes.VALUE: ""})
            return
        attributes = {sensor.Attributes.STATE: sensor.States.ON, sensor.Attributes.VALUE: value}
        if self._spec.unit:
            attributes[sensor.Attributes.UNIT] = self._spec.unit
        self.update(attributes)


def create_sensors(device_config: CambridgeConfig, device: CambridgeDevice) -> list[CambridgeSensor]:
    features = device_config.features
    return [
        CambridgeSensor(spec, device_config, device)
        for spec in SPECS
        if spec.feature is None or features is None or spec.feature in features
    ]
