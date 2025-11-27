# Cambridge Audio Integration for Unfolded Circle Remote 2/3

Control your Cambridge Audio streamers, receivers, and pre-amps (Evo, CXN, CXR, Edge NQ, AXN10 series) directly from your Unfolded Circle Remote 2 or Remote 3 with comprehensive media player control, **complete multi-device support**, **dynamic source management**, and **full playback control**.

![Cambridge Audio](https://img.shields.io/badge/Cambridge%20Audio-Streamers-blue)
[![GitHub Release](https://img.shields.io/github/v/release/mase1981/uc-intg-cambridge-audio?style=flat-square)](https://github.com/mase1981/uc-intg-cambridge-audio/releases)
![License](https://img.shields.io/badge/license-MPL--2.0-blue?style=flat-square)
[![GitHub issues](https://img.shields.io/github/issues/mase1981/uc-intg-cambridge-audio?style=flat-square)](https://github.com/mase1981/uc-intg-cambridge-audio/issues)
[![Community Forum](https://img.shields.io/badge/community-forum-blue?style=flat-square)](https://community.unfoldedcircle.com/)
[![Discord](https://badgen.net/discord/online-members/zGVYf58)](https://discord.gg/zGVYf58)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/mase1981/uc-intg-cambridge-audio/total?style=flat-square)
[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=flat-square)](https://buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-donate-blue.svg?style=flat-square)](https://paypal.me/mmiyara)
[![Github Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-30363D?&logo=GitHub-Sponsors&logoColor=EA4AAA&style=flat-square)](https://github.com/sponsors/mase1981)


## Features

This integration provides comprehensive control of Cambridge Audio network streamers through the StreamMagic WebSocket API, delivering seamless integration with your Unfolded Circle Remote for complete music streaming control.

---
## 💰 Support Development

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

### **Supported Models**

#### **Evo Series** - All-in-One Systems
- **Evo One** - Compact streaming system
- **Evo 75** - Powerful streaming amplifier
- **Evo 150** - Flagship streaming system

#### **CXN Series** - Network Streamers
- **CXN** - Original network streamer
- **CXN V2** - Enhanced network streamer
- **CXN100** - Latest generation streamer

#### **CXR Series** - Receivers
- **CXR120** - 7-channel receiver
- **CXR200** - 9-channel flagship receiver

#### **Other Models**
- **851N** - Premium network player
- **Edge NQ** - Reference-class network player
- **AXN10** - Network audio player

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

### Available Sources

Sources are dynamically discovered from your device configuration:

| Source Category | Examples |
|----------------|----------|
| Streaming Services | Spotify, Tidal, Qobuz |
| Digital Inputs | Optical, Coaxial |
| Analog Input | Stereo analog |
| USB | USB audio input |
| Network | DLNA, UPnP servers |
| Internet Radio | Built-in radio stations |
| AirPlay | Apple AirPlay |
| Bluetooth | Bluetooth audio |

**Note**: Only sources configured and available on your device will appear in the source list.

### Activity Integration

#### Creating Activities

Remote commands can be integrated into UC activities:

```yaml
Power On Sequence:
  1. POWER_ON
  2. Delay 2000ms
  3. SOURCE_SPOTIFY
  4. Delay 1000ms
  5. PLAY

Volume Control:
  - VOLUME_UP (repeatable)
  - VOLUME_DOWN (repeatable)
  - MUTE_TOGGLE

Source Selection:
  - SOURCE_SPOTIFY
  - SOURCE_TIDAL
  - SOURCE_USB
  - SOURCE_OPTICAL
  (dynamically generated from device sources)
```

## Troubleshooting

### Connection Issues

**Problem**: Integration cannot connect to device
- **Solution**: Verify device IP address is correct
- **Solution**: Ensure device is powered on and connected to network
- **Solution**: Check that device and Remote are on same subnet
- **Solution**: Restart device and try again
- **Solution**: Verify no firewall blocking port 80

**Problem**: Device disconnects frequently
- **Solution**: Use wired Ethernet connection instead of Wi-Fi
- **Solution**: Assign static IP or DHCP reservation
- **Solution**: Update device firmware to latest version
- **Solution**: Check network stability and router logs

### Control Issues

**Problem**: Commands not responding
- **Solution**: Check device state in web interface
- **Solution**: Verify WebSocket connection is active
- **Solution**: Enable "Keep WiFi connected in standby" in Remote settings
- **Solution**: Restart integration from web interface

**Problem**: Volume control not working
- **Solution**: Verify device is in correct mode (not in standby)
- **Solution**: Check if device supports volume control (some models are fixed output)
- **Solution**: Ensure pre-amp mode is enabled if available

**Problem**: Sources not appearing
- **Solution**: Configure sources in Cambridge Audio app first
- **Solution**: Restart integration to refresh source list
- **Solution**: Verify sources are enabled on device

### Reboot Survival

**Problem**: Entities unavailable after Remote reboot
- **Check**: This integration includes automatic reboot survival
- **Solution**: If entities still unavailable, remove and re-add integration
- **Prevention**: Always use latest version from releases

### Wake-Up Issues

**Problem**: Commands fail immediately after Remote wakes from sleep
- **Solution**: Enable "Keep WiFi connected in standby" in Remote power settings
- **Note**: Integration includes automatic retry logic for wake-up scenarios

### Getting Help

1. **Check Logs**: Enable debug logging in Remote web interface
2. **GitHub Issues**: [Report bugs and request features](https://github.com/mase1981/uc-intg-cambridge-audio/issues)
3. **Community Forum**: [Get help from community](https://community.unfoldedcircle.com/)
4. **Discord**: [Join real-time discussion](https://discord.gg/zGVYf58)

## Development

### Running Locally

```bash
# Clone repository
git clone https://github.com/mase1981/uc-intg-cambridge-audio.git
cd uc-intg-cambridge-audio

# Install dependencies
pip install -r requirements.txt

# Run integration
python -m uc_intg_cambridge_audio.driver
```

### Using the Simulator

For development without physical hardware:

```bash
# Start simulator (separate terminal)
python cambridge_audio_simulator.py

# Start integration (another terminal)
python -m uc_intg_cambridge_audio.driver

# Use localhost or 127.0.0.1 as device IP during setup
```

**Simulator Features:**
- Emulates Cambridge Audio CXN V2 with StreamMagic API
- Responds to all standard commands
- Realistic power, playback, volume, mute control
- Dynamic source management
- WebSocket connection handling
- State update broadcasting

### Project Structure

```
uc-intg-cambridge-audio/
├── uc_intg_cambridge_audio/   # Main package
│   ├── __init__.py            # Package info with dynamic versioning
│   ├── client.py              # StreamMagic WebSocket client
│   ├── config.py              # Configuration management
│   ├── driver.py              # Main integration driver
│   ├── media_player.py        # Media player entity
│   ├── remote.py              # Remote control entity
│   └── setup.py               # Setup flow handler
├── .github/workflows/         # GitHub Actions CI/CD
│   └── build.yml              # Automated build pipeline
├── .vscode/                   # VS Code configuration
│   └── launch.json            # Debug configuration
├── cambridge_audio_simulator.py  # Development simulator
├── docker-compose.yml         # Docker deployment
├── Dockerfile                 # Container build instructions
├── driver.json                # Integration metadata
├── requirements.txt           # Dependencies
├── pyproject.toml             # Python project config
└── README.md                  # This file
```

### Key Implementation Details

#### **StreamMagic WebSocket Protocol**
- Uses WebSocket for all communication (port 80)
- JSON-based message protocol
- Persistent connection with automatic reconnection
- Real-time state update callbacks
- Bidirectional communication

#### **Command Format**
```json
{
  "command": "power_on"
}

{
  "command": "set_volume",
  "volume": 50
}

{
  "command": "set_source",
  "source_id": "Spotify"
}
```

#### **State Update Format**
```json
{
  "type": "state_update",
  "data": {
    "state": {
      "power": true,
      "volume_percent": 50,
      "mute": false,
      "source": "Spotify"
    },
    "play_state": {
      "state": "play",
      "position": 45000,
      "metadata": {
        "title": "Track Name",
        "artist": "Artist Name",
        "album": "Album Name",
        "art_url": "https://...",
        "duration": 180000
      }
    }
  }
}
```

#### **Multi-Device Architecture**
- Each device = separate WebSocket client instance
- Independent connections per device
- Separate media_player and remote entity per device
- Device ID = `cambridge_{ip_with_underscores}`
- Entity IDs = `media_player.cambridge_{device_id}` and `remote.cambridge_{device_id}`

#### **Volume Scaling**
```python
# Device range: 0-100 (percentage from device)
# Remote range: 0-100 (percentage)
# Direct mapping with no conversion needed
volume_percent = device_volume
```

#### **Reboot Survival Pattern**
```python
# Pre-initialize entities if config exists
if config.is_configured():
    await _initialize_integration()

# Reload config on reconnect
async def on_connect():
    config.reload_from_disk()
    if not entities_ready:
        await _initialize_integration()

# Race condition protection
async def on_subscribe_entities(entity_ids):
    if not entities_ready:
        await _initialize_integration()
```

#### **Wake-Up Error Handling**
```python
# All network commands include retry logic
try:
    await client.power_on()
except Exception as ex:
    _LOG.error(f"Command failed: {ex}")
    await asyncio.sleep(ERROR_OS_WAIT)  # 500ms delay
    await client.power_on()  # Retry once
```

### StreamMagic API Reference

Essential API endpoints used by this integration:

```python
# Device Information
await client.get_info()          # Returns model, name, version
await client.get_state()         # Returns power, volume, mute, source
await client.get_sources()       # Returns available sources
await client.get_play_state()    # Returns playback state and metadata
await client.get_now_playing()   # Returns current media info

# Power Control
await client.power_on()          # Power on device
await client.power_off()         # Power off device

# Playback Control
await client.play()              # Start playback
await client.pause()             # Pause playback
await client.play_pause()        # Toggle play/pause
await client.stop()              # Stop playback
await client.next_track()        # Skip to next track
await client.previous_track()    # Skip to previous track
await client.media_seek(pos)     # Seek to position (ms)

# Volume Control
await client.volume_up()         # Increase volume
await client.volume_down()       # Decrease volume
await client.set_volume(vol)     # Set volume (0-100)
await client.set_mute(mute)      # Set mute state (bool)

# Source Control
await client.set_source_by_id(id)  # Switch to source by ID

# Playback Modes
await client.set_shuffle(mode)   # Set shuffle (ShuffleMode)
await client.set_repeat(mode)    # Set repeat (RepeatMode)

# State Callbacks
await client.register_state_update_callbacks(callback)
client.unregister_state_update_callbacks(callback)
```

### Testing Protocol

#### **Connection Testing**
```python
# Test WebSocket connection
client = CambridgeClient(device_config)
success = await client.connect()
assert success is True
assert client.is_connected()
```

#### **Command Testing**
```python
# Test power control
await client.power_on()
await asyncio.sleep(0.5)
assert client.client.state.power is True

# Test volume control
await client.set_volume(50)
await asyncio.sleep(0.5)
assert client.client.state.volume_percent == 50
```

#### **Multi-Device Testing**
```python
# Test independent device control
await client1.power_on()
await client2.power_off()
await asyncio.sleep(0.5)
assert client1.client.state.power is True
assert client2.client.state.power is False
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test with real Cambridge device or simulator
4. Commit changes: `git commit -m 'Add amazing feature'`
5. Push to branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

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