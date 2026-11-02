"""
Cambridge Audio media player entity.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from typing import Any

from aiostreammagic.models import RepeatMode as CambridgeRepeatMode
from aiostreammagic.models import ShuffleMode
from ucapi import StatusCodes, media_player
from ucapi.media_player import Attributes, Commands, Features, MediaContentType, RepeatMode, States
from ucapi_framework import MediaPlayerEntity

from uc_intg_cambridge_audio.config import CambridgeConfig
from uc_intg_cambridge_audio.device import CambridgeDevice

_LOG = logging.getLogger(__name__)

FEATURES = [
    Features.ON_OFF,
    Features.TOGGLE,
    Features.VOLUME,
    Features.VOLUME_UP_DOWN,
    Features.MUTE_TOGGLE,
    Features.MUTE,
    Features.UNMUTE,
    Features.PLAY_PAUSE,
    Features.STOP,
    Features.NEXT,
    Features.PREVIOUS,
    Features.SEEK,
    Features.MEDIA_DURATION,
    Features.MEDIA_POSITION,
    Features.MEDIA_TITLE,
    Features.MEDIA_ARTIST,
    Features.MEDIA_ALBUM,
    Features.MEDIA_IMAGE_URL,
    Features.MEDIA_TYPE,
    Features.SELECT_SOURCE,
    Features.SHUFFLE,
    Features.REPEAT,
]

_PLAY_STATES = {
    "play": States.PLAYING,
    "pause": States.PAUSED,
    "connecting": States.BUFFERING,
    "stop": States.ON,
    "ready": States.ON,
}

_REPEAT_FROM_DEVICE = {
    CambridgeRepeatMode.ALL: RepeatMode.ALL,
    CambridgeRepeatMode.ONE: RepeatMode.ONE,
}


class CambridgeMediaPlayer(MediaPlayerEntity):
    def __init__(self, device_config: CambridgeConfig, device: CambridgeDevice) -> None:
        self._device = device
        super().__init__(
            f"media_player.{device_config.identifier}",
            device_config.name,
            FEATURES,
            {
                Attributes.STATE: States.UNKNOWN,
                Attributes.VOLUME: 0,
                Attributes.MUTED: False,
                Attributes.SOURCE: "",
                Attributes.SOURCE_LIST: [],
            },
            device_class=media_player.DeviceClasses.RECEIVER,
            cmd_handler=self._handle_command,
        )
        self.subscribe_to_device(device)

    async def sync_state(self) -> None:
        device = self._device
        state, play_state = device.sm_state, device.play_state
        if not device.available or state is None or play_state is None:
            self.update({Attributes.STATE: States.UNAVAILABLE})
            return

        if not state.power or play_state.state == "NETWORK":
            media_state = States.OFF
        else:
            media_state = _PLAY_STATES.get(play_state.state, States.ON)

        sources = device.sources
        current_source = next((s.name for s in sources if s.id == state.source), "")
        metadata = play_state.metadata
        artist = metadata.artist or ""
        if not artist and state.source == "IR":
            artist = metadata.station or ""

        self.update(
            {
                Attributes.STATE: media_state,
                Attributes.VOLUME: state.volume_percent or 0,
                Attributes.MUTED: state.mute,
                Attributes.SOURCE: current_source,
                Attributes.SOURCE_LIST: [s.name for s in sources],
                Attributes.MEDIA_TITLE: metadata.title or "",
                Attributes.MEDIA_ARTIST: artist,
                Attributes.MEDIA_ALBUM: metadata.album or "",
                Attributes.MEDIA_IMAGE_URL: metadata.art_url or "",
                Attributes.MEDIA_DURATION: metadata.duration or 0,
                Attributes.MEDIA_POSITION: play_state.position or 0,
                Attributes.MEDIA_POSITION_UPDATED_AT: device.position_updated_at or "",
                Attributes.MEDIA_TYPE: MediaContentType.MUSIC,
                Attributes.SHUFFLE: play_state.mode_shuffle != ShuffleMode.OFF,
                Attributes.REPEAT: _REPEAT_FROM_DEVICE.get(play_state.mode_repeat, RepeatMode.OFF),
            }
        )

    async def _handle_command(self, entity: Any, cmd_id: str, params: dict[str, Any] | None) -> StatusCodes:
        params = params or {}
        device = self._device
        try:
            match cmd_id:
                case Commands.ON:
                    await device.send("power_on")
                case Commands.OFF:
                    await device.send("power_off")
                case Commands.TOGGLE:
                    state = device.sm_state
                    await device.send("power_off" if state and state.power else "power_on")
                case Commands.PLAY_PAUSE:
                    await device.send("play_pause")
                case Commands.STOP:
                    await device.send("stop")
                case Commands.NEXT:
                    await device.send("next_track")
                case Commands.PREVIOUS:
                    await device.send("previous_track")
                case Commands.SEEK:
                    await device.send("media_seek", int(params["media_position"]))
                case Commands.VOLUME:
                    await device.send("set_volume", max(0, min(100, int(params["volume"]))))
                case Commands.VOLUME_UP:
                    await device.send("volume_up")
                case Commands.VOLUME_DOWN:
                    await device.send("volume_down")
                case Commands.MUTE_TOGGLE:
                    state = device.sm_state
                    await device.send("set_mute", not (state.mute if state else False))
                case Commands.MUTE:
                    await device.send("set_mute", True)
                case Commands.UNMUTE:
                    await device.send("set_mute", False)
                case Commands.SELECT_SOURCE:
                    wanted = str(params["source"]).strip().lower()
                    source = next(
                        (s for s in device.sources if wanted in (s.name.lower(), s.id.lower())),
                        None,
                    )
                    if source is None:
                        return StatusCodes.BAD_REQUEST
                    await device.send("set_source_by_id", source.id)
                case Commands.SHUFFLE:
                    mode = ShuffleMode.ALL if params["shuffle"] else ShuffleMode.OFF
                    await device.send("set_shuffle", mode)
                case Commands.REPEAT:
                    mode = {
                        RepeatMode.ALL: CambridgeRepeatMode.ALL,
                        RepeatMode.ONE: CambridgeRepeatMode.ONE,
                    }.get(params["repeat"], CambridgeRepeatMode.OFF)
                    await device.send("set_repeat", mode)
                case _:
                    return StatusCodes.NOT_IMPLEMENTED
        except (KeyError, ValueError, TypeError):
            return StatusCodes.BAD_REQUEST
        except Exception as err:  # pylint: disable=broad-exception-caught
            _LOG.error("[%s] Command %s failed: %s", entity.id, cmd_id, err)
            return StatusCodes.SERVER_ERROR
        return StatusCodes.OK
