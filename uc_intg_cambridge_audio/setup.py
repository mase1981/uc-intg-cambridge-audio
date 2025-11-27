"""
Cambridge Audio setup flow implementation.

:copyright: (c) 2025 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from typing import Any, Dict

from ucapi import IntegrationSetupError, RequestUserInput, SetupComplete, SetupError

from uc_intg_cambridge_audio.client import CambridgeClient
from uc_intg_cambridge_audio.config import CambridgeConfig, DeviceConfig

_LOG = logging.getLogger(__name__)


class CambridgeSetup:
    
    def __init__(self, config: CambridgeConfig):
        self._config = config
        self._setup_state = {}
    
    async def handle_setup_request(self, setup_data: Dict[str, Any]) -> Any:
        device_count = int(setup_data.get("device_count", 1))
        host = setup_data.get("host", "").strip()
        
        if device_count == 1 and host:
            return await self._handle_single_device_setup(setup_data)
        else:
            return await self._request_device_configurations(device_count)
    
    async def _handle_single_device_setup(self, setup_data: Dict[str, Any]) -> Any:
        host_input = setup_data.get("host")
        if not host_input:
            _LOG.error("No host provided in setup data")
            return SetupError(IntegrationSetupError.OTHER)
        
        host = host_input.strip()
        name = setup_data.get("name", f"Cambridge Audio ({host})").strip()
        
        _LOG.info(f"Testing connection to Cambridge Audio at {host}")
        
        try:
            device_id = f"cambridge_{host.replace('.', '_')}"
            
            existing_device = self._config.get_device(device_id)
            if existing_device:
                _LOG.info(f"Device {device_id} already exists, removing for reconfiguration")
                self._config.remove_device(device_id)
            
            device_config = DeviceConfig(
                device_id=device_id,
                name=name,
                ip_address=host
            )
            
            test_client = CambridgeClient(device_config)
            
            try:
                _LOG.info("Testing connection...")
                connection_successful = await test_client.connect()
                
                if not connection_successful:
                    _LOG.error(f"Connection test failed for host: {host}")
                    return SetupError(IntegrationSetupError.CONNECTION_REFUSED)
                
                info = await test_client.get_info()
                device_config.model = info.model if info else "Unknown"
                _LOG.info(f"Detected Cambridge Audio model: {device_config.model}")
                
            finally:
                await test_client.close()
            
            self._config.add_device(device_config)
            _LOG.info(f"Successfully added device: {name}")
            return SetupComplete()
        
        except Exception as e:
            _LOG.error(f"Setup error: {e}", exc_info=True)
            return SetupError(IntegrationSetupError.OTHER)
    
    async def _request_device_configurations(self, device_count: int) -> RequestUserInput:
        settings = []
        
        for i in range(device_count):
            settings.extend([
                {
                    "id": f"device_{i}_ip",
                    "label": {"en": f"Device {i+1} IP Address"},
                    "description": {"en": f"IP address for Cambridge Audio device {i+1}"},
                    "field": {"text": {"value": f"192.168.1.{100+i}"}}
                },
                {
                    "id": f"device_{i}_name",
                    "label": {"en": f"Device {i+1} Name"},
                    "description": {"en": f"Friendly name for device {i+1}"},
                    "field": {"text": {"value": f"Cambridge Audio {i+1}"}}
                }
            ])
        
        return RequestUserInput(
            title={"en": f"Configure {device_count} Cambridge Audio Devices"},
            settings=settings
        )
    
    async def handle_user_data(self, input_values: Dict[str, Any]) -> Any:
        devices_to_test = []
        
        device_index = 0
        while f"device_{device_index}_ip" in input_values:
            ip_input = input_values[f"device_{device_index}_ip"]
            name = input_values[f"device_{device_index}_name"]
            
            host = ip_input.strip()
            if not host:
                _LOG.error(f"Invalid IP for device {device_index + 1}")
                return SetupError(IntegrationSetupError.OTHER)
            
            devices_to_test.append({
                "host": host,
                "name": name,
                "index": device_index
            })
            device_index += 1
        
        _LOG.info(f"Testing connections to {len(devices_to_test)} devices...")
        test_results = await self._test_multiple_devices(devices_to_test)
        
        successful_devices = 0
        for device_data, success in zip(devices_to_test, test_results):
            if success:
                device_id = f"cambridge_{device_data['host'].replace('.', '_')}"
                
                existing_device = self._config.get_device(device_id)
                if existing_device:
                    _LOG.info(f"Device {device_id} already exists, removing for reconfiguration")
                    self._config.remove_device(device_id)
                
                device_config = DeviceConfig(
                    device_id=device_id,
                    name=device_data['name'],
                    ip_address=device_data['host'],
                    model=device_data.get('model', 'Unknown')
                )
                self._config.add_device(device_config)
                successful_devices += 1
                _LOG.info(f"Device {device_data['index'] + 1} ({device_data['name']}) configured successfully")
            else:
                _LOG.error(f"Device {device_data['index'] + 1} ({device_data['name']}) connection failed")
        
        if successful_devices == 0:
            _LOG.error("No devices could be connected")
            return SetupError(IntegrationSetupError.CONNECTION_REFUSED)
        
        _LOG.info(f"Multi-device setup completed: {successful_devices}/{len(devices_to_test)} devices configured")
        return SetupComplete()
    
    async def _test_multiple_devices(self, devices: list) -> list[bool]:
        results = []
        
        for device in devices:
            device_config = DeviceConfig(
                device_id=f"test_{device['index']}",
                name=device['name'],
                ip_address=device['host']
            )
            
            client = CambridgeClient(device_config)
            
            try:
                success = await client.connect()
                if success:
                    info = await client.get_info()
                    device['model'] = info.model if info else "Unknown"
                results.append(success)
            except Exception as e:
                _LOG.error(f"Device {device['index'] + 1} test exception: {e}")
                results.append(False)
            finally:
                await client.close()
        
        return results