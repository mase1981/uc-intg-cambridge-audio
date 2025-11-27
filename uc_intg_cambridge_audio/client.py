"""
Cambridge Audio client implementation.

:copyright: (c) 2025 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import asyncio
import logging
from typing import Any, Callable, Optional

import aiohttp
from aiostreammagic import StreamMagicClient
from aiostreammagic.models import CallbackType

from uc_intg_cambridge_audio.config import DeviceConfig

_LOG = logging.getLogger(__name__)

ERROR_OS_WAIT = 0.5


class CambridgeClient:
    
    def __init__(self, device_config: DeviceConfig, session=None):
        self._device_config = device_config
        self._client: Optional[StreamMagicClient] = None
        self._connected = False
        self._callbacks: list[Callable] = []
        self._session = session
        self._owns_session = False
        
    async def connect(self) -> bool:
        try:
            if not self._session:
                self._session = aiohttp.ClientSession()
                self._owns_session = True
            
            if not self._client:
                self._client = StreamMagicClient(
                    self._device_config.ip_address,
                    session=self._session
                )
            
            async with asyncio.timeout(self._device_config.timeout):
                await self._client.connect()
            
            self._connected = True
            _LOG.info(f"Connected to Cambridge Audio at {self._device_config.ip_address}")
            
            for callback in self._callbacks:
                await self._client.register_state_update_callbacks(callback)
            
            return True
            
        except asyncio.TimeoutError:
            _LOG.error(f"Connection timeout for {self._device_config.ip_address}")
            self._connected = False
            return False
        except Exception as e:
            _LOG.error(f"Connection failed for {self._device_config.ip_address}: {e}", exc_info=True)
            self._connected = False
            return False
    
    async def disconnect(self):
        if self._client:
            try:
                await self._client.disconnect()
                _LOG.info(f"Disconnected from {self._device_config.ip_address}")
            except Exception as e:
                _LOG.error(f"Error during disconnect: {e}")
            finally:
                self._connected = False
    
    async def close(self):
        await self.disconnect()
        if self._owns_session and self._session:
            await self._session.close()
            self._session = None
        self._client = None
    
    def is_connected(self) -> bool:
        if self._client:
            return self._client.is_connected()
        return False
    
    def register_callback(self, callback: Callable):
        if callback not in self._callbacks:
            self._callbacks.append(callback)
        if self._client:
            asyncio.create_task(self._client.register_state_update_callbacks(callback))
    
    def unregister_callback(self, callback: Callable):
        if callback in self._callbacks:
            self._callbacks.remove(callback)
        if self._client:
            self._client.unregister_state_update_callbacks(callback)
    
    @property
    def client(self) -> Optional[StreamMagicClient]:
        return self._client
    
    @property
    def device_config(self) -> DeviceConfig:
        return self._device_config
    
    async def get_info(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        return self._client.info
    
    async def get_state(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        return self._client.state
    
    async def get_sources(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        return self._client.sources
    
    async def get_play_state(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        return self._client.play_state
    
    async def get_now_playing(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        return self._client.now_playing
    
    async def power_on(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.power_on()
        except Exception as ex:
            _LOG.error(f"Power on failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.power_on()
    
    async def power_off(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.power_off()
        except Exception as ex:
            _LOG.error(f"Power off failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.power_off()
    
    async def play(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.play()
        except Exception as ex:
            _LOG.error(f"Play failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.play()
    
    async def pause(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.pause()
        except Exception as ex:
            _LOG.error(f"Pause failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.pause()
    
    async def play_pause(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.play_pause()
        except Exception as ex:
            _LOG.error(f"Play/pause failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.play_pause()
    
    async def stop(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.stop()
        except Exception as ex:
            _LOG.error(f"Stop failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.stop()
    
    async def next_track(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.next_track()
        except Exception as ex:
            _LOG.error(f"Next track failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.next_track()
    
    async def previous_track(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.previous_track()
        except Exception as ex:
            _LOG.error(f"Previous track failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.previous_track()
    
    async def volume_up(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.volume_up()
        except Exception as ex:
            _LOG.error(f"Volume up failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.volume_up()
    
    async def volume_down(self):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.volume_down()
        except Exception as ex:
            _LOG.error(f"Volume down failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.volume_down()
    
    async def set_volume(self, volume: int):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.set_volume(volume)
        except Exception as ex:
            _LOG.error(f"Set volume failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.set_volume(volume)
    
    async def set_mute(self, mute: bool):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.set_mute(mute)
        except Exception as ex:
            _LOG.error(f"Set mute failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.set_mute(mute)
    
    async def set_source_by_id(self, source_id: str):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.set_source_by_id(source_id)
        except Exception as ex:
            _LOG.error(f"Set source failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.set_source_by_id(source_id)
    
    async def media_seek(self, position: int):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.media_seek(position)
        except Exception as ex:
            _LOG.error(f"Media seek failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.media_seek(position)
    
    async def set_shuffle(self, shuffle_mode):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.set_shuffle(shuffle_mode)
        except Exception as ex:
            _LOG.error(f"Set shuffle failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.set_shuffle(shuffle_mode)
    
    async def set_repeat(self, repeat_mode):
        if not self._client:
            raise RuntimeError("Client not initialized")
        try:
            await self._client.set_repeat(repeat_mode)
        except Exception as ex:
            _LOG.error(f"Set repeat failed: {ex}")
            await asyncio.sleep(ERROR_OS_WAIT)
            await self._client.set_repeat(repeat_mode)