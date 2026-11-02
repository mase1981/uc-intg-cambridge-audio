# Cambridge Audio Integration for Unfolded Circle Remote 2/3

Control your Cambridge Audio streamers, receivers, and pre-amps (Evo, CXN, CXR, Edge NQ, AXN10 series) directly from your Unfolded Circle Remote 2 or Remote 3 with comprehensive media player control, **complete multi-device support**, **dynamic source management**, and **full playback control**.

![Cambridge Audio](https://img.shields.io/badge/Cambridge%20Audio-Streamers-blue)
[![GitHub Release](https://img.shields.io/github/v/release/mase1981/uc-intg-cambridge-audio?style=flat-square)](https://github.com/mase1981/uc-intg-cambridge-audio/releases)
![License](https://img.shields.io/badge/license-MPL--2.0-blue?style=flat-square)
[![GitHub issues](https://img.shields.io/github/issues/mase1981/uc-intg-cambridge-audio?style=flat-square)](https://github.com/mase1981/uc-intg-cambridge-audio/issues)
[![Community Forum](https://img.shields.io/badge/community-forum-blue?style=flat-square)](https://unfolded.community/)
[![Discord](https://badgen.net/discord/online-members/zGVYf58)](https://discord.gg/zGVYf58)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/mase1981/uc-intg-cambridge-audio/total?style=flat-square)
[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=flat-square)](https://buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-donate-blue.svg?style=flat-square)](https://paypal.me/mmiyara)
[![Github Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-30363D?&logo=GitHub-Sponsors&logoColor=EA4AAA&style=flat-square)](https://github.com/sponsors/mase1981)


## Features

This integration provides comprehensive control of Cambridge Audio network streamers through the StreamMagic WebSocket API, delivering seamless integration with your Unfolded Circle Remote for complete music streaming control.

---
## ❤️ Support Development ❤️

If you find this integration useful, consider supporting development:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-pink?style=for-the-badge&logo=github)](https://github.com/sponsors/mase1981)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/mmiyara)

Your support helps maintain this integration. Thank you! ❤️
---

### 🎵 **Media Player**

Power, volume (slider, up/down, mute), playback (play/pause, stop, next, previous, seek), shuffle, repeat (off / all / one), dynamic source list, and now-playing info with artwork, duration and position.

### 🎮 **Remote Entity**

Physical button mapping, simple commands for activities (`send_cmd` and `send_cmd_sequence`), and UI pages for main controls, sources and settings. Commands include `POWER_ON`, `POWER_OFF`, `SOURCE_<id>`, display brightness, pre-amp and control bus modes.

### 📊 **Sensors**

State, source, volume (% and dB), audio output, model, API version, firmware update status, pre-amp mode, control bus, standby mode, auto power-down, display brightness, equalizer and EQ preset, room correction (and intensity), balance, volume limit, digital filter, audio pipeline, phase invert, plus stream details: codec, sample rate, sample format, bitrate, lossless, MQA, signal and radio station.

Sensors for features your unit does not have (for example equalizer or room correction) are not created.

### 🎛️ **Selects**

Source, audio output, display brightness, control bus mode, standby mode, EQ preset and preset recall.

### 🔘 **Switches**

Pre-amp mode, equalizer, room correction and early firmware updates.

### 🔌 **Multi-Device Support**

Run setup again to add another device. Each device gets its own full set of entities.

### **Protocol Requirements**

- **Protocol**: StreamMagic WebSocket API
- **Connection**: WebSocket (ws://)
- **Port**: 80 (HTTP/WebSocket)
- **Network Access**: Device must be on same local network
- **Real-time Updates**: Automatic state synchronization via WebSocket callbacks

### **Network Requirements**

- **Local Network Access** - Integration requires same network as Cambridge Audio device
- **WebSocket Support** - Device must support StreamMagic WebSocket API
- **Static IP Recommended** - Device should have static IP or DHCP reservation
- **Standby** - Keep the unit in Network standby mode; in Eco standby the unit is unreachable until powered on at the unit

## Installation

### Option 1: Remote Web Interface (Recommended)
1. Navigate to the [**Releases**](https://github.com/mase1981/uc-intg-cambridge-audio/releases) page
2. Download the latest `uc-intg-cambridge-audio-<version>-aarch64.tar.gz` file
3. Open your remote's web interface (`http://your-remote-ip`)
4. Go to **Settings** → **Integrations** → **Add Integration**
5. Click **Upload** and select the downloaded `.tar.gz` file

### Option 2: Docker (Advanced Users)

The integration is available as a pre-built Docker image from GitHub Container Registry:

**Image**: `ghcr.io/mase1981/uc-intg-cambridge-audio:latest`

**Docker Compose:**
```yaml
services:
  uc-intg-cambridge-audio:
    image: ghcr.io/mase1981/uc-intg-cambridge-audio:latest
    container_name: uc-intg-cambridge-audio
    network_mode: host
    volumes:
      - </local/path>:/data
    environment:
      - UC_CONFIG_HOME=/data
      - UC_INTEGRATION_HTTP_PORT=9090
      - UC_INTEGRATION_INTERFACE=0.0.0.0
      - PYTHONPATH=/app
    restart: unless-stopped
```

**Docker Run:**
```bash
docker run -d --name uc-cambridge-audio --restart unless-stopped --network host -v cambridge-config:/app/config -e UC_CONFIG_HOME=/app/config -e UC_INTEGRATION_INTERFACE=0.0.0.0 -e UC_INTEGRATION_HTTP_PORT=9090 -e PYTHONPATH=/app ghcr.io/mase1981/uc-intg-cambridge-audio:latest
```

## Configuration

### Step 1: Prepare Your Cambridge Audio Device

**IMPORTANT**: Cambridge Audio device must be powered on and connected to your network before adding the integration.

#### Verify Network Connection:
1. Check that device is connected to network (Ethernet or Wi-Fi)
2. Note the IP address from device's network settings or router
3. Ensure device firmware is up to date
4. Verify device is accessible on your network

#### Network Setup:
- **Wired Connection**: Recommended for stability and best audio quality
- **Static IP**: Recommended via DHCP reservation
- **Network Isolation**: Must be on same subnet as Remote
- **WebSocket Access**: Device must be accessible on port 80

### Step 2: Setup Integration

1. After installation, go to **Settings** → **Integrations**
2. The Cambridge Audio integration should appear in **Available Integrations**
3. Click **"Configure"** and enter:
   - **Device Name**: Friendly name (optional, defaults to the name set on the device)
   - **IP Address**: Device IP (e.g., 192.168.1.100)
4. The integration connects to the device, reads its model, sources and capabilities, and creates the entities.

To add another device, run setup again. Existing entity IDs are preserved when upgrading from 1.x.

## Using the Integration

### Media Player Entity

Each device's media player entity provides complete control:

- **Power Control**: On/Off/Toggle with state feedback
- **Volume Control**: Volume slider (0-100) with real-time updates
- **Volume Buttons**: Up/Down with immediate feedback
- **Mute Control**: Toggle, Mute, Unmute
- **Playback Control**: Play, Pause, Stop, Next, Previous
- **Source Selection**: Dropdown with all available sources (dynamically populated)
- **Media Info**: Title, artist, album, cover art, duration, position
- **Playback Modes**: Shuffle and repeat control
- **Seek Control**: Position slider for track navigation

### Remote Control Entity

Each device's remote entity provides:

- **Physical Button Mappings**: Pre-configured for optimal control
- **Simple Commands**: All commands available for activities
- **Custom UI Pages**:
  - Main control page with power, volume, playback
  - Sources page with grid layout for quick selection
  - Settings page for display brightness, pre-amp and control bus
- **Activity Integration**: Commands can be used in UC activities

## Credits

- **Developer**: Meir Miyara
- **Cambridge Audio**: High-quality audio streamers and players
- **Unfolded Circle**: Remote 2/3 integration framework (ucapi)
- **StreamMagic API**: Cambridge Audio's WebSocket control protocol
- **aiostreammagic**: Python library by Noah Husby
- **ucapi-framework**: Framework by Jack Powell
- **Community**: Testing and feedback from UC community

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0) - see LICENSE file for details.

## Support & Community

- **GitHub Issues**: [Report bugs and request features](https://github.com/mase1981/uc-intg-cambridge-audio/issues)
- **UC Community Forum**: [General discussion and support](https://unfolded.community/)
- **Developer**: [Meir Miyara](https://www.linkedin.com/in/meirmiyara)
- **Cambridge Audio Support**: [Official Cambridge Audio Support](https://www.cambridgeaudio.com/row/en/support)

---

**Made with ❤️ for the Unfolded Circle and Cambridge Audio Communities**

**Thank You**: Meir Miyara
