"""
Cambridge Audio remote entity.

:copyright: (c) 2025 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from typing import Any

from aiostreammagic.models import ShuffleMode, RepeatMode as CambridgeRepeatMode
from ucapi import StatusCodes, Remote
from ucapi.remote import Attributes, Commands, Features, States
from ucapi.ui import create_btn_mapping, Buttons, create_ui_icon, UiPage, Size

from uc_intg_cambridge_audio.client import CambridgeClient
from uc_intg_cambridge_audio.config import DeviceConfig

_LOG = logging.getLogger(__name__)


class CambridgeRemote(Remote):
    
    def __init__(self, client: CambridgeClient, device_config: DeviceConfig, api):
        self._client = client
        self._device_config = device_config
        self._api = api
        
        entity_id = f"remote.cambridge_{device_config.device_id}"
        
        simple_commands = [
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
            "MUTE_TOGGLE"
        ]
        
        sources = []
        if client and client.client and client.client.sources:
            for source in client.client.sources:
                simple_commands.append(f"SOURCE_{source.id.upper()}")
                sources.append(source.id)
        
        button_mapping = [
            create_btn_mapping(Buttons.POWER, short="POWER_TOGGLE"),
            create_btn_mapping(Buttons.VOLUME_UP, short="VOLUME_UP"),
            create_btn_mapping(Buttons.VOLUME_DOWN, short="VOLUME_DOWN"),
            create_btn_mapping(Buttons.MUTE, short="MUTE_TOGGLE"),
            create_btn_mapping(Buttons.PLAY, short="PLAY_PAUSE"),
            create_btn_mapping(Buttons.NEXT, short="NEXT"),
            create_btn_mapping(Buttons.PREV, short="PREVIOUS"),
        ]
        
        main_page = UiPage("main", "Cambridge Audio")
        main_page.add(create_ui_icon("uc:power-on", 0, 0, cmd="POWER_ON"))
        main_page.add(create_ui_icon("uc:power-off", 1, 0, cmd="POWER_OFF"))
        main_page.add(create_ui_icon("uc:up-arrow", 2, 0, cmd="VOLUME_UP"))
        main_page.add(create_ui_icon("uc:down-arrow", 3, 0, cmd="VOLUME_DOWN"))
        
        main_page.add(create_ui_icon("uc:play", 0, 1, cmd="PLAY"))
        main_page.add(create_ui_icon("uc:pause", 1, 1, cmd="PAUSE"))
        main_page.add(create_ui_icon("uc:stop", 2, 1, cmd="STOP"))
        main_page.add(create_ui_icon("uc:speaker-mute", 3, 1, cmd="MUTE_TOGGLE"))
        
        main_page.add(create_ui_icon("uc:prev", 0, 2, cmd="PREVIOUS"))
        main_page.add(create_ui_icon("uc:play-pause", 1, 2, size=Size(2, 1), cmd="PLAY_PAUSE"))
        main_page.add(create_ui_icon("uc:next", 3, 2, cmd="NEXT"))
        
        ui_pages = [main_page]
        
        if sources:
            sources_page = UiPage("sources", "Sources")
            row = 0
            col = 0
            for source_id in sources[:12]:
                sources_page.add(create_ui_icon("uc:input", col, row, cmd=f"SOURCE_{source_id.upper()}"))
                col += 1
                if col >= 4:
                    col = 0
                    row += 1
            ui_pages.append(sources_page)
        
        attributes = {
            Attributes.STATE: States.UNAVAILABLE
        }
        
        super().__init__(
            identifier=entity_id,
            name=f"{device_config.name} Remote",
            features=[Features.ON_OFF, Features.TOGGLE, Features.SEND_CMD],
            attributes=attributes,
            simple_commands=simple_commands,
            button_mapping=button_mapping,
            ui_pages=ui_pages
        )
        
        if self._client and self._client.client:
            self._client.register_callback(self._state_update_callback)
    
    async def _state_update_callback(self, client, callback_type):
        await self.push_update()
    
    async def push_update(self):
        if not self._client or not self._client.is_connected():
            self.attributes[Attributes.STATE] = States.UNAVAILABLE
            if self._api:
                self._api.configured_entities.update_attributes(self.id, self.attributes)
            return
        
        try:
            state = self._client.client.state
            if state.power:
                self.attributes[Attributes.STATE] = States.ON
            else:
                self.attributes[Attributes.STATE] = States.OFF
            
            if self._api:
                self._api.configured_entities.update_attributes(self.id, self.attributes)
            
        except Exception as e:
            _LOG.error(f"Error updating remote state for {self.id}: {e}")
    
    async def command(self, cmd_id: str, params: dict[str, Any] | None = None) -> StatusCodes:
        _LOG.info(f"[{self.id}] Received command: {cmd_id}")
        
        try:
            if cmd_id == Commands.ON:
                await self._client.power_on()
            
            elif cmd_id == Commands.OFF:
                await self._client.power_off()
            
            elif cmd_id == Commands.TOGGLE:
                state = self.attributes.get(Attributes.STATE)
                if state == States.OFF:
                    await self._client.power_on()
                else:
                    await self._client.power_off()
            
            elif cmd_id == Commands.SEND_CMD:
                if params and "command" in params:
                    command = params["command"]
                    await self._handle_simple_command(command)
            
            elif cmd_id == Commands.SEND_CMD_SEQUENCE:
                if params and "sequence" in params:
                    sequence = params["sequence"]
                    delay = params.get("delay", 0) / 1000.0
                    repeat = params.get("repeat", 1)
                    
                    for _ in range(repeat):
                        for command in sequence:
                            await self._handle_simple_command(command)
                            if delay > 0:
                                import asyncio
                                await asyncio.sleep(delay)
            
            else:
                _LOG.warning(f"Unsupported command: {cmd_id}")
                return StatusCodes.NOT_IMPLEMENTED
            
            await self.push_update()
            return StatusCodes.OK
            
        except Exception as e:
            _LOG.error(f"Command execution failed for {cmd_id}: {e}")
            return StatusCodes.SERVER_ERROR
    
    async def _handle_simple_command(self, command: str):
        command_upper = command.upper()
        
        if command_upper == "POWER_ON":
            await self._client.power_on()
        
        elif command_upper == "POWER_OFF":
            await self._client.power_off()
        
        elif command_upper == "POWER_TOGGLE":
            state = self.attributes.get(Attributes.STATE)
            if state == States.OFF:
                await self._client.power_on()
            else:
                await self._client.power_off()
        
        elif command_upper == "PLAY":
            await self._client.play()
        
        elif command_upper == "PAUSE":
            await self._client.pause()
        
        elif command_upper == "PLAY_PAUSE":
            await self._client.play_pause()
        
        elif command_upper == "STOP":
            await self._client.stop()
        
        elif command_upper == "NEXT":
            await self._client.next_track()
        
        elif command_upper == "PREVIOUS":
            await self._client.previous_track()
        
        elif command_upper == "VOLUME_UP":
            await self._client.volume_up()
        
        elif command_upper == "VOLUME_DOWN":
            await self._client.volume_down()
        
        elif command_upper == "MUTE":
            await self._client.set_mute(True)
        
        elif command_upper == "UNMUTE":
            await self._client.set_mute(False)
        
        elif command_upper == "MUTE_TOGGLE":
            state = self._client.client.state
            await self._client.set_mute(not state.mute)
        
        elif command_upper.startswith("SOURCE_"):
            source_id = command_upper.replace("SOURCE_", "")
            sources = self._client.client.sources
            for src in sources:
                if src.id.upper() == source_id:
                    await self._client.set_source_by_id(src.id)
                    break
        
        else:
            _LOG.warning(f"Unknown simple command: {command}")