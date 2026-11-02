"""
Cambridge Audio configuration.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import json
import logging
import os
from dataclasses import dataclass, field

from ucapi_framework import BaseConfigManager

_LOG = logging.getLogger(__name__)

CONFIG_FILENAME = "config.json"


@dataclass
class CambridgeConfig:
    identifier: str = ""
    name: str = ""
    host: str = ""
    model: str = ""
    timeout: int = 10
    source_ids: list[str] = field(default_factory=list)
    features: list[str] | None = None


class CambridgeConfigManager(BaseConfigManager[CambridgeConfig]):
    pass


def migrate_legacy_config(config_dir: str) -> bool:
    """Convert the pre-2.0 ``{"devices": [...]}`` file into the framework's list format.

    Identifiers become ``cambridge_<old device_id>`` so entity IDs
    (``media_player.cambridge_<device_id>``) stay identical to 1.x.
    """
    path = os.path.join(config_dir, CONFIG_FILENAME)
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as err:
        _LOG.error("Cannot read legacy config %s: %s", path, err)
        return False
    if not isinstance(data, dict) or "devices" not in data:
        return False

    migrated = []
    for item in data.get("devices", []):
        try:
            if not item.get("enabled", True):
                continue
            migrated.append(
                {
                    "identifier": f"cambridge_{item['device_id']}",
                    "name": item["name"],
                    "host": item["ip_address"],
                    "model": item.get("model", ""),
                    "timeout": item.get("timeout", 10),
                }
            )
        except (KeyError, AttributeError, TypeError) as err:
            _LOG.warning("Skipping unreadable legacy device entry %s: %s", item, err)

    backup = f"{path}.v1.bak"
    try:
        if not os.path.exists(backup):
            os.replace(path, backup)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(migrated, file, ensure_ascii=False, indent=2)
    except OSError as err:
        _LOG.error("Cannot write migrated config: %s", err)
        return False
    _LOG.info("Migrated %d device(s) from legacy config format", len(migrated))
    return True
