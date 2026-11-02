"""
Cambridge Audio integration for Unfolded Circle Remote.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import asyncio
import json
import logging
import os
from pathlib import Path

try:
    _driver_path = Path(__file__).parent.parent / "driver.json"
    with open(_driver_path, "r", encoding="utf-8") as f:
        __version__ = json.load(f).get("version", "0.0.0")
except (FileNotFoundError, json.JSONDecodeError):
    __version__ = "0.0.0"

__all__ = ["__version__", "main"]
_LOG = logging.getLogger(__name__)


async def main():
    from ucapi import DeviceStates
    from ucapi_framework import get_config_path

    from uc_intg_cambridge_audio.config import (
        CambridgeConfig,
        CambridgeConfigManager,
        migrate_legacy_config,
    )
    from uc_intg_cambridge_audio.driver import CambridgeDriver
    from uc_intg_cambridge_audio.setup_flow import CambridgeSetupFlow

    level = os.getenv("UC_LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)-22s | %(message)s",
    )
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("aiostreammagic").setLevel(logging.WARNING)
    logging.getLogger("websockets.server").setLevel(logging.CRITICAL)
    _LOG.info("Starting Cambridge Audio Integration v%s", __version__)

    driver = CambridgeDriver()
    config_path = get_config_path(driver.api.config_dir_path or "")
    migrate_legacy_config(config_path)
    config_manager = CambridgeConfigManager(
        config_path,
        add_handler=driver.on_device_added,
        remove_handler=driver.on_device_removed,
        config_class=CambridgeConfig,
    )
    driver.config_manager = config_manager

    setup_handler = CambridgeSetupFlow.create_handler(driver)
    driver_json = os.path.join(os.path.dirname(__file__), "..", "driver.json")
    await driver.api.init(os.path.abspath(driver_json), setup_handler)
    await driver.register_all_device_instances(connect=False)

    count = len(list(config_manager.all()))
    await driver.api.set_device_state(DeviceStates.CONNECTED if count > 0 else DeviceStates.DISCONNECTED)
    _LOG.info("Cambridge Audio integration started - %d device(s) configured", count)
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
