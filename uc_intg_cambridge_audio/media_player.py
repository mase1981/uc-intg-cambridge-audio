"""
Cambridge Audio media player entity.

:copyright: (c) 2025 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from datetime import datetime
from typing import Any

from aiostreammagic import TransportControl
from aiostreammagic.models import ShuffleMode, RepeatMode as CambridgeRepeatMode
from ucapi import StatusCodes, media_player
from ucapi.media_player import Attributes as MediaAttr, Features, MediaType, RepeatMode, States

from uc_intg_cambridge_audio.client import CambridgeClient
from uc_intg_cambridge_audio.config import DeviceConfig

_LOG = logging.getLogger(__name__)


class CambridgeMediaPlayer(media_player.MediaPlayer):
    
    def __init__(self, client: CambridgeClient, device_config: DeviceConfig, api):
        self._client = client
        self._device_config = device_config
        self._api = api
        
        entity_id = f"media_player.cambridge_{device_config.device_id}"
        
        features = [
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
            Features.REPEAT
        ]
        
        attributes = {
            MediaAttr.STATE: States.UNAVAILABLE,
            MediaAttr.VOLUME: 0,
            MediaAttr.MUTED: False,
            MediaAttr.SOURCE: "",
            MediaAttr.SOURCE_LIST: []
        }
        
        super().__init__(
            identifier=entity_id,
            name=device_config.name,
            features=features,
            attributes=attributes,
            device_class=media_player.DeviceClasses.RECEIVER
        )
        
        if self._client and self._client.client:
            self._client.register_callback(self._state_update_callback)
    
    async def _state_update_callback(self, client, callback_type):
        await self.push_update()
    
    async def push_update(self):
        if not self._client or not self._client.is_connected():
            self.attributes[MediaAttr.STATE] = States.UNAVAILABLE
            if self._api:
                self._api.configured_entities.update_attributes(self.id, self.attributes)
            return
        
        try:
            state = self._client.client.state
            play_state = self._client.client.play_state
            
            media_state = play_state.state
            if media_state == "NETWORK":
                self.attributes[MediaAttr.STATE] = States.OFF
            elif state.power:
                if media_state == "play":
                    self.attributes[MediaAttr.STATE] = States.PLAYING
                elif media_state == "pause":
                    self.attributes[MediaAttr.STATE] = States.PAUSED
                elif media_state == "connecting":
                    self.attributes[MediaAttr.STATE] = States.BUFFERING
                elif media_state in ("stop", "ready"):
                    self.attributes[MediaAttr.STATE] = States.IDLE
                else:
                    self.attributes[MediaAttr.STATE] = States.ON
            else:
                self.attributes[MediaAttr.STATE] = States.OFF
            
            volume_percent = state.volume_percent or 0
            self.attributes[MediaAttr.VOLUME] = volume_percent
            self.attributes[MediaAttr.MUTED] = state.mute
            
            sources = self._client.client.sources
            self.attributes[MediaAttr.SOURCE_LIST] = [item.name for item in sources]
            
            current_source = next(
                (item.name for item in sources if item.id == state.source),
                None
            )
            self.attributes[MediaAttr.SOURCE] = current_source or ""
            
            metadata = play_state.metadata
            self.attributes[MediaAttr.MEDIA_TITLE] = metadata.title or ""
            
            if not metadata.artist and state.source == "IR":
                self.attributes[MediaAttr.MEDIA_ARTIST] = metadata.station or ""
            else:
                self.attributes[MediaAttr.MEDIA_ARTIST] = metadata.artist or ""
            
            self.attributes[MediaAttr.MEDIA_ALBUM] = metadata.album or ""
            self.attributes[MediaAttr.MEDIA_IMAGE_URL] = metadata.art_url or ""
            self.attributes[MediaAttr.MEDIA_DURATION] = metadata.duration or 0
            self.attributes[MediaAttr.MEDIA_POSITION] = play_state.position or 0
            
            position_updated = self._client.client.position_last_updated
            if position_updated:
                self.attributes[MediaAttr.MEDIA_POSITION_UPDATED_AT] = position_updated.isoformat()
            
            self.attributes[MediaAttr.MEDIA_TYPE] = MediaType.MUSIC
            
            self.attributes[MediaAttr.SHUFFLE] = play_state.mode_shuffle != ShuffleMode.OFF
            
            if play_state.mode_repeat == CambridgeRepeatMode.ALL:
                self.attributes[MediaAttr.REPEAT] = RepeatMode.ALL
            else:
                self.attributes[MediaAttr.REPEAT] = RepeatMode.OFF
            
            if self._api:
                self._api.configured_entities.update_attributes(self.id, self.attributes)
            
        except Exception as e:
            _LOG.error(f"Error updating state for {self.id}: {e}")
    
    async def command(self, cmd_id: str, params: dict[str, Any] | None = None) -> StatusCodes:
        _LOG.info(f"[{self.id}] Received command: {cmd_id}")
        
        try:
            if cmd_id == media_player.Commands.ON:
                await self._client.power_on()
            
            elif cmd_id == media_player.Commands.OFF:
                await self._client.power_off()
            
            elif cmd_id == media_player.Commands.TOGGLE:
                state = self.attributes.get(MediaAttr.STATE)
                if state == States.OFF:
                    await self._client.power_on()
                else:
                    await self._client.power_off()
            
            elif cmd_id == media_player.Commands.PLAY_PAUSE:
                await self._client.play_pause()
            
            elif cmd_id == media_player.Commands.STOP:
                await self._client.stop()
            
            elif cmd_id == media_player.Commands.PREVIOUS:
                await self._client.previous_track()
            
            elif cmd_id == media_player.Commands.NEXT:
                await self._client.next_track()
            
            elif cmd_id == media_player.Commands.SEEK:
                if params and "media_position" in params:
                    position = int(params["media_position"])
                    await self._client.media_seek(position)
            
            elif cmd_id == media_player.Commands.VOLUME:
                if params and "volume" in params:
                    volume = int(params["volume"])
                    await self._client.set_volume(volume)
            
            elif cmd_id == media_player.Commands.VOLUME_UP:
                await self._client.volume_up()
            
            elif cmd_id == media_player.Commands.VOLUME_DOWN:
                await self._client.volume_down()
            
            elif cmd_id == media_player.Commands.MUTE_TOGGLE:
                current_mute = self.attributes.get(MediaAttr.MUTED, False)
                await self._client.set_mute(not current_mute)
            
            elif cmd_id == media_player.Commands.MUTE:
                await self._client.set_mute(True)
            
            elif cmd_id == media_player.Commands.UNMUTE:
                await self._client.set_mute(False)
            
            elif cmd_id == media_player.Commands.SELECT_SOURCE:
                if params and "source" in params:
                    source_name = params["source"]
                    sources = self._client.client.sources
                    for src in sources:
                        if src.name == source_name:
                            await self._client.set_source_by_id(src.id)
                            break
            
            elif cmd_id == media_player.Commands.SHUFFLE:
                if params and "shuffle" in params:
                    shuffle = params["shuffle"]
                    shuffle_mode = ShuffleMode.ALL if shuffle else ShuffleMode.OFF
                    await self._client.set_shuffle(shuffle_mode)
            
            elif cmd_id == media_player.Commands.REPEAT:
                if params and "repeat" in params:
                    repeat = params["repeat"]
                    if repeat in [RepeatMode.ALL, RepeatMode.ONE]:
                        repeat_mode = CambridgeRepeatMode.ALL
                    else:
                        repeat_mode = CambridgeRepeatMode.OFF
                    await self._client.set_repeat(repeat_mode)
            
            else:
                _LOG.warning(f"Unsupported command: {cmd_id}")
                return StatusCodes.NOT_IMPLEMENTED
            
            await self.push_update()
            return StatusCodes.OK
            
        except Exception as e:
            _LOG.error(f"Command execution failed for {cmd_id}: {e}")
            return StatusCodes.SERVER_ERROR