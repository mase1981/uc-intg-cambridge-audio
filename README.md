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

### 🎵 **Media Player Control**

#### **Power Management**
- **Power On/Off** - Complete power control
- **Power Toggle** - Quick power state switching
- **State Feedback** - Real-time power state monitoring
- **Standby Mode** - Network standby support

#### **Playback Control**
- **Play/Pause** - Playback control with state feedback
- **Stop** - Stop playback
- **Next Track** - Skip to next track
- **Previous Track** - Skip to previous track
- **Seek** - Position control within current media
- **Shuffle Control** - Toggle shuffle mode
- **Repeat Control** - Toggle repeat mode

#### **Volume Control**
- **Volume Up/Down** - Precise volume adjustment
- **Set Volume** - Direct volume control (0-100 scale)
- **Volume Slider** - Visual volume control
- **Mute Toggle** - Quick mute/unmute
- **Mute/Unmute** - Explicit mute control
- **Pre-Amp Mode** - Full volume control in pre-amp mode

#### **Source Selection**
Control all available input sources dynamically:
- **Spotify** - Spotify Connect streaming
- **Tidal** - Tidal HiFi streaming
- **USB** - USB audio input
- **Optical** - Optical digital input
- **Coaxial** - Coaxial digital input
- **Analog** - Analog audio input
- **Internet Radio** - Built-in radio stations
- **AirPlay** - Apple AirPlay support
- **Bluetooth** - Bluetooth audio streaming
- **Network Sources** - Network streaming services

#### **Media Information**
- **Now Playing** - Current track title, artist, album
- **Album Art** - High-resolution cover art display
- **Media Duration** - Total track length
- **Media Position** - Current playback position with live updates
- **Media Type** - Content type identification
- **Station Info** - Internet radio station details

### 🔌 **Multi-Device Support**

- **Multiple Streamers** - Control up to 4 Cambridge Audio devices
- **Individual Configuration** - Each device gets dedicated media player and remote entities
- **Manual Configuration** - Direct IP address entry
- **Model Detection** - Automatic model identification
- **Custom Naming** - Personalized device names

### 🎮 **Remote Control Entity**

Each device includes a comprehensive remote control entity with:

#### **Simple Commands**
- Power control (ON, OFF, TOGGLE)
- Transport controls (PLAY, PAUSE, STOP, NEXT, PREVIOUS)
- Volume controls (UP, DOWN, MUTE)
- Source selection commands
- All commands available for activity integration

#### **Physical Button Mapping**
- Power button → Power toggle
- Volume buttons → Volume control
- Mute button → Mute toggle
- Play button → Play/Pause
- Next/Previous buttons → Track navigation

#### **Custom UI Pages**
- **Main Page**: Power, volume, playback controls
- **Sources Page**: Quick source selection grid
- Beautiful icon-based interface
- Optimized for Remote 2/3 display

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
- **Network Discovery** - Devices must be accessible via IP address

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
3. Click **"Configure"** and select setup mode:

#### **Single Device Setup:**

   **Configuration:**
   - **IP Address**: Enter device IP (e.g., 192.168.1.100)
   - **Device Name**: Friendly name (e.g., "Living Room Cambridge")
   - Click **Complete Setup**

   **Connection Test:**
   - Integration verifies device connectivity via WebSocket
   - Model information retrieved automatically
   - Setup fails if device unreachable

#### **Multi-Device Setup:**

   **Configuration:**
   - Select number of devices (2-4)
   - For each device, provide:
     - IP address
     - Friendly name
   - Click **Complete Setup**

   **Connection Test:**
   - Integration tests all connections simultaneously
   - Only successfully connected devices added
   - Failed connections reported with error details

3. Integration will create **two entities per device**:
   - **Media Player**: `media_player.cambridge_[device_name]`
   - **Remote Control**: `remote.cambridge_[device_name]`

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
- **Activity Integration**: Commands can be used in UC activities

## Credits

- **Developer**: Meir Miyara
- **Cambridge Audio**: High-quality audio streamers and players
- **Unfolded Circle**: Remote 2/3 integration framework (ucapi)
- **StreamMagic API**: Cambridge Audio's WebSocket control protocol
- **aiostreammagic**: Python library by Noah Husby
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
