"""
Cambridge Audio device (StreamMagic WebSocket API).

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import asyncio
import logging
from typing import Any

from aiostreammagic import StreamMagicClient
from aiostreammagic.exceptions import StreamMagicError
from aiostreammagic.models import (
    EQ_PRESETS,
    Audio,
    AudioOutput,
    CallbackType,
    Display,
    Info,
    NowPlaying,
    PlayState,
    PresetList,
    Source,
    State,
    Update,
)
from ucapi_framework import ExternalClientDevice

from uc_intg_cambridge_audio.config import CambridgeConfig

_LOG = logging.getLogger(__name__)

_RETRY_MIN, _RETRY_MAX = 30, 900


def detect_features(client: StreamMagicClient) -> list[str]:
    """Optional capabilities a connected unit reports."""
    features = []
    try:
        audio = client.audio
    except StreamMagicError:
        return features
    if audio.user_eq is not None:
        features.append("eq")
    if audio.tilt_eq is not None:
        features.append("room_correction")
    if audio.balance is not None:
        features.append("balance")
    if audio.volume_limit_percent is not None:
        features.append("volume_limit")
    if audio.digital_filter is not None:
        features.append("digital_filter")
    if audio.pipeline is not None:
        features.append("pipeline")
    if audio.phase_invert is not None:
        features.append("phase_invert")
    return features


class CambridgeDevice(ExternalClientDevice):
    def __init__(self, device_config: CambridgeConfig, **kwargs: Any) -> None:
        super().__init__(device_config, **kwargs)
        self._device_config = device_config
        self._connect_lock = asyncio.Lock()
        self._retry_task: asyncio.Task | None = None

    @property
    def identifier(self) -> str:
        return self._device_config.identifier

    @property
    def name(self) -> str:
        return self._device_config.name

    @property
    def address(self) -> str:
        return self._device_config.host

    @property
    def log_id(self) -> str:
        return f"{self.name} ({self.address})"

    @property
    def available(self) -> bool:
        return self.check_client_connected()

    def _safe(self, attr: str) -> Any:
        client = self._client
        if client is None:
            return None
        try:
            return getattr(client, attr)
        except StreamMagicError:
            return None

    @property
    def info(self) -> Info | None:
        return self._safe("info")

    @property
    def sm_state(self) -> State | None:
        return self._safe("state")

    @property
    def play_state(self) -> PlayState | None:
        return self._safe("play_state")

    @property
    def now_playing(self) -> NowPlaying | None:
        return self._safe("now_playing")

    @property
    def audio(self) -> Audio | None:
        return self._safe("audio")

    @property
    def audio_output(self) -> AudioOutput | None:
        return self._safe("audio_output")

    @property
    def display(self) -> Display | None:
        return self._safe("display")

    @property
    def update_info(self) -> Update | None:
        return self._safe("update")

    @property
    def preset_list(self) -> PresetList | None:
        return self._safe("preset_list")

    @property
    def sources(self) -> list[Source]:
        return list(self._safe("sources") or [])

    @property
    def position_updated_at(self) -> str | None:
        stamp = self._safe("position_last_updated")
        return stamp.astimezone().isoformat() if stamp else None

    @property
    def eq_preset(self) -> str | None:
        """Name of the built-in EQ preset the current band gains match."""
        audio = self.audio
        if audio is None or audio.user_eq is None or not audio.user_eq.bands:
            return None
        gains = {band.index: band.gain for band in audio.user_eq.bands}
        for name, preset in EQ_PRESETS.items():
            if all(
                gains.get(index) is not None and abs(gains[index] - gain) < 0.05
                for index, gain in enumerate(preset)
            ):
                return name
        return None

    async def connect(self) -> bool:
        async with self._connect_lock:
            connected = await super().connect()
        if not connected and (self._retry_task is None or self._retry_task.done()):
            self._retry_task = asyncio.create_task(self._retry_connect())
        return connected

    async def _retry_connect(self) -> None:
        delay = _RETRY_MIN
        while True:
            await asyncio.sleep(delay)
            async with self._connect_lock:
                if await super().connect():
                    return
            delay = min(delay * 2, _RETRY_MAX)

    async def disconnect(self) -> None:
        if self._retry_task:
            self._retry_task.cancel()
            self._retry_task = None
        async with self._connect_lock:
            await super().disconnect()

    async def create_client(self) -> StreamMagicClient:
        await self.disconnect_client()
        return StreamMagicClient(self._device_config.host)

    async def connect_client(self) -> None:
        client = self._client
        try:
            async with asyncio.timeout(self._device_config.timeout):
                await client.connect()
        except BaseException:
            await client.disconnect()
            raise
        await client.register_state_update_callbacks(self._on_library_update)
        self._remember_capabilities(client)
        self.push_update()

    async def disconnect_client(self) -> None:
        client = self._client
        if client is None:
            return
        client.unregister_state_update_callbacks(self._on_library_update)
        await client.disconnect()

    def check_client_connected(self) -> bool:
        return self._client is not None and self._client.is_connected()

    async def _on_library_update(
        self, client: StreamMagicClient, callback_type: CallbackType
    ) -> None:
        self.push_update()

    def _remember_capabilities(self, client: StreamMagicClient) -> None:
        changes: dict[str, Any] = {}
        features = detect_features(client)
        if self._device_config.features != features:
            changes["features"] = features
        source_ids = [source.id for source in client.sources]
        if source_ids and self._device_config.source_ids != source_ids:
            changes["source_ids"] = source_ids
        try:
            model = client.info.model
        except StreamMagicError:
            model = ""
        if model and self._device_config.model != model:
            changes["model"] = model
        if changes:
            self.update_config(**changes)

    async def send(self, method: str, *args: Any) -> None:
        """Call a StreamMagicClient command; raises when the unit is unreachable."""
        client = self._client
        if client is None or not client.is_connected():
            raise StreamMagicError("Not connected to device.")
        await getattr(client, method)(*args)
