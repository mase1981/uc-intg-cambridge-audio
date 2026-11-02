"""
Cambridge Audio setup flow.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import asyncio
import logging
import re
from typing import Any

from aiostreammagic import StreamMagicClient
from ucapi import RequestUserInput
from ucapi_framework import BaseSetupFlow

from uc_intg_cambridge_audio.config import CambridgeConfig
from uc_intg_cambridge_audio.device import detect_features

_LOG = logging.getLogger(__name__)

_HOST_RE = re.compile(r"^[A-Za-z0-9]([A-Za-z0-9.\-]*[A-Za-z0-9])?(:\d{1,5})?$")


class CambridgeSetupFlow(BaseSetupFlow[CambridgeConfig]):
    def get_manual_entry_form(self, error: str = "") -> RequestUserInput:
        settings = []
        if error:
            settings.append(
                {"id": "error", "label": {"en": ""}, "field": {"label": {"value": {"en": f"⚠️ {error}"}}}}
            )
        settings += [
            {"id": "name", "label": {"en": "Device Name"}, "field": {"text": {"value": ""}}},
            {"id": "host", "label": {"en": "IP Address"}, "field": {"text": {"value": ""}}},
        ]
        return RequestUserInput({"en": "Cambridge Audio Setup"}, settings)

    async def query_device(self, input_values: dict[str, Any]) -> CambridgeConfig | RequestUserInput:
        host = str(input_values.get("host", "")).strip()
        name = str(input_values.get("name", "")).strip()
        if not host or not _HOST_RE.match(host):
            return self.get_manual_entry_form("Enter a valid IP address or host name.")

        client = StreamMagicClient(host)
        try:
            async with asyncio.timeout(15):
                await client.connect()
            info = client.info
            config = CambridgeConfig(
                identifier=self._identifier_for(host),
                name=name or info.name or f"Cambridge Audio ({host})",
                host=host,
                model=info.model,
                source_ids=[source.id for source in client.sources],
                features=detect_features(client),
            )
        except Exception as err:  # pylint: disable=broad-exception-caught
            _LOG.warning("Setup connection to %s failed: %s", host, err)
            return self.get_manual_entry_form(f"Cannot connect to {host}: {err or 'timeout'}")
        finally:
            await client.disconnect()
        return config

    def _identifier_for(self, host: str) -> str:
        for existing in self.config.all():
            if existing.host == host:
                return existing.identifier
        return "cambridge_" + re.sub(r"[^a-z0-9]", "_", host.lower())
